import json
import httpx

from efidgy import exceptions


class Client:
    def __init__(self, env):
        self.env = env

    def _url(self, path):
        args = ['time_format=clock_24']
        if self.env.unit_system is not None:
            args.append('unit_system={}'.format(self.env.unit_system))
        return 'https://{host}/api/{code}{path}/?{args}'.format(
            host=self.env.host,
            code=self.env.code,
            path=path,
            args='&'.join(args),
        )

    def _auth(self):
        return {
            'Authorization': 'Token {}'.format(self.env.token),
        }

    def _handle_errors(self, data, status_code):
        if status_code >= 200 and status_code < 300:
            return
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

    def _handle_response(self, response):
        try:
            data = json.load(response)
        except json.decoder.JSONDecodeError:
            data = {}
        self._handle_errors(data, response.status_code)

    def get(self, path):
        with self._client() as client:
            url = self._url(path)
            response = client.get(
                url,
                headers=self._auth(),
            )
            try:
                return json.load(response)
            except json.decoder.JSONDecodeError:
                return None

    def post(self, path, data):
        with self._client() as client:
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
            try:
                return json.load(response)
            except json.decoder.JSONDecodeError:
                return None

    def put(self, path, data):
        with self._client() as client:
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
            try:
                return json.load(response)
            except json.decoder.JSONDecodeError:
                return None

    def delete(self, path):
        with self._client() as client:
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

    async def _handle_response(self, response):
        try:
            data = json.loads(await response.aread())
        except json.decoder.JSONDecodeError:
            data = {}
        self._handle_errors(data, response.status_code)

    async def get(self, path):
        async with self._client() as client:
            url = self._url(path)
            response = await client.get(
                url,
                headers=self._auth(),
            )
            try:
                return json.load(response)
            except json.decoder.JSONDecodeError:
                return None

    async def post(self, path, data):
        async with self._client() as client:
            url = self._url(path)
            response = await client.post(
                url,
                content=json.dumps(data),
                headers={
                    'Content-Type': 'application/json',
                    **self._auth(),
                }
            )
            try:
                return json.load(response)
            except json.decoder.JSONDecodeError:
                return None

    async def put(self, path, data):
        async with self._client() as client:
            url = self._url(path)
            response = await client.put(
                url,
                content=json.dumps(data),
                headers={
                    'Content-Type': 'application/json',
                    **self._auth(),
                }
            )
            try:
                return json.load(response)
            except json.decoder.JSONDecodeError:
                return None

    async def delete(self, path):
        async with self._client() as client:
            url = self._url(path)
            await client.delete(
                url,
                headers={
                    'Content-Type': 'application/json',
                    **self._auth(),
                }
            )
