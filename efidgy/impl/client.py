import json
import httpx
from urllib.parse import urlparse
import re

import efidgy
from efidgy import exceptions


class Client:
    _verified = False

    def __init__(self, env):
        self.env = env

    def _compare_version(self, data):
        version = data.get('version') if data else None
        assert version, (
            'Unable to fetch server version.'
        )
        if version == 'dev':
            return
        m = re.match(r'([^-]+)(?:-.+)?', efidgy.__version__)
        local_version = m[1] if m else efidgy.__version
        if version != local_version:
            raise exceptions.VersionError(version)

    def _url(self, path):
        args = ['time_format=clock_24']
        if self.env.unit_system is not None:
            args.append('unit_system={}'.format(self.env.unit_system))
        o = urlparse(path)
        path = o.path
        if path.endswith('/'):
            path = path[:-1]
        args.append(o.query)
        return 'https://{host}/api/{code}{path}/?{args}'.format(
            host=self.env.host,
            code=self.env.code,
            path=path,
            args='&'.join(args),
        )

    def _auth(self):
        ret = {}
        if self.env.token:
            ret['Authorization'] = 'Token {}'.format(self.env.token)
        return ret

    def _handle_errors(self, data, status_code):
        if data is None:
            data = {}
        if status_code == 400:
            detail = data.get('detail')
            if detail is not None:
                raise exceptions.BadRequest(detail)
            raise exceptions.ValidationError(data)
        if status_code == 401:
            detail = data.get(
                'detail',
                'Authentication failed.',
            )
            raise exceptions.AuthenticationFailed(detail)
        if status_code == 403:
            detail = data.get(
                'detail',
                'Permission denied.',
            )
            raise exceptions.PermissionDenied(detail)
        if status_code == 404:
            detail = data.get('detail', 'Not found.')
            raise exceptions.NotFound(detail)
        if status_code == 405:
            detail = data.get('detail', 'Method not allowed.')
            raise exceptions.MethodNotAllowed(detail)
        if status_code >= 500 and status_code < 600:
            raise exceptions.InternalServerError()
        raise RuntimeError(
            'Unhandled response code: {}'.format(status_code),
        )


class SyncClient(Client):
    def _client(self):
        return httpx.Client(
            verify=not self.env.insecure,
            event_hooks={'response': [self._handle_response]}
        )

    def _load_response(self, response):
        try:
            return json.load(response)
        except json.decoder.JSONDecodeError:
            return None

    def _check_version(self, client):
        if self._verified:
            return

        response = client.get(
            'https://{}/efidgy_version.json'.format(self.env.host),
        )
        self._compare_version(self._load_response(response))

        type(self)._verified = True

    def _handle_response(self, response):
        if response.status_code >= 200 and response.status_code < 300:
            return
        data = self._load_response(response)
        self._handle_errors(data, response.status_code)

    def get(self, path):
        with self._client() as client:
            self._check_version(client)
            url = self._url(path)
            response = client.get(
                url,
                headers=self._auth(),
            )
            return self._load_response(response)

    def post(self, path, data):
        with self._client() as client:
            self._check_version(client)
            url = self._url(path)
            data = json.dumps(data) if data is not None else None
            response = client.post(
                url,
                content=data,
                headers={
                    'Content-Type': 'application/json',
                    **self._auth(),
                }
            )
            return self._load_response(response)

    def put(self, path, data):
        with self._client() as client:
            self._check_version(client)
            url = self._url(path)
            data = json.dumps(data) if data is not None else None
            response = client.put(
                url,
                content=data,
                headers={
                    'Content-Type': 'application/json',
                    **self._auth(),
                }
            )
            return self._load_response(response)

    def delete(self, path):
        with self._client() as client:
            self._check_version(client)
            url = self._url(path)
            client.delete(
                url,
                headers={
                    'Content-Type': 'application/json',
                    **self._auth(),
                }
            )


class AsyncClient(Client):
    def _client(self):
        return httpx.AsyncClient(
            verify=not self.env.insecure,
            event_hooks={'response': [self._handle_response]}
        )

    async def _load_response(self, response):
        try:
            return json.loads(await response.aread())
        except json.decoder.JSONDecodeError:
            return None

    async def _check_version(self, client):
        if self._verified:
            return

        response = await client.get(
            'https://{}/efidgy_version.json'.format(self.env.host),
        )
        self._compare_version(await self._load_response(response))

        type(self)._verified = True

    async def _handle_response(self, response):
        if response.status_code >= 200 and response.status_code < 300:
            return
        data = await self._load_response(response)
        self._handle_errors(data, response.status_code)

    async def get(self, path):
        async with self._client() as client:
            await self._check_version(client)
            url = self._url(path)
            response = await client.get(
                url,
                headers=self._auth(),
            )
            return await self._load_response(response)

    async def post(self, path, data):
        async with self._client() as client:
            await self._check_version(client)
            url = self._url(path)
            response = await client.post(
                url,
                content=json.dumps(data),
                headers={
                    'Content-Type': 'application/json',
                    **self._auth(),
                }
            )
            return await self._load_response(response)

    async def put(self, path, data):
        async with self._client() as client:
            await self._check_version(client)
            url = self._url(path)
            response = await client.put(
                url,
                content=json.dumps(data),
                headers={
                    'Content-Type': 'application/json',
                    **self._auth(),
                }
            )
            return await self._load_response(response)

    async def delete(self, path):
        async with self._client() as client:
            await self._check_version(client)
            url = self._url(path)
            await client.delete(
                url,
                headers={
                    'Content-Type': 'application/json',
                    **self._auth(),
                }
            )
