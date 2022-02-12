import json
import httpx


class Client:
    def __init__(self, env):
        self.env = env

    def _url(self, path):
        return 'https://{host}/api/{code}{path}/'.format(
            host=self.env.host,
            code=self.env.code,
            path=path,
        )

    def _auth(self):
        return {
            'Authorization': 'Token {}'.format(self.env.token),
        }


class SyncClient(Client):
    def get(self, path):
        with httpx.Client(verify=not self.env.insecure) as client:
            url = self._url(path)
            response = client.get(
                url,
                headers=self._auth(),
            )
            return json.load(response)

    def post(self, path, data):
        with httpx.Client(verify=not self.env.insecure) as client:
            url = self._url(path)
            response = client.post(
                url,
                content=json.dumps(data),
                headers={
                    'Content-Type': 'application/json',
                    **self._auth(),
                }
            )
            return json.load(response)

    def put(self, path, data):
        with httpx.Client(verify=not self.env.insecure) as client:
            url = self._url(path)
            response = client.put(
                url,
                content=json.dumps(data),
                headers={
                    'Content-Type': 'application/json',
                    **self._auth(),
                }
            )
            return json.load(response)

    def delete(self, path):
        with httpx.Client(verify=not self.env.insecure) as client:
            url = self._url(path)
            client.delete(
                url,
                headers={
                    'Content-Type': 'application/json',
                    **self._auth(),
                }
            )


class AsyncClient(Client):
    async def get(self, path):
        async with httpx.AsyncClient(verify=not self.env.insecure) as client:
            url = self._url(path)
            response = await client.get(
                url,
                headers=self._auth(),
            )
            return json.load(response)

    async def post(self, path, data):
        async with httpx.AsyncClient(verify=not self.env.insecure) as client:
            url = self._url(path)
            response = await client.post(
                url,
                content=json.dumps(data),
                headers={
                    'Content-Type': 'application/json',
                    **self._auth(),
                }
            )
            return json.load(response)

    async def put(self, path, data):
        async with httpx.AsyncClient(verify=not self.env.insecure) as client:
            url = self._url(path)
            response = await client.put(
                url,
                content=json.dumps(data),
                headers={
                    'Content-Type': 'application/json',
                    **self._auth(),
                }
            )
            return json.load(response)

    async def delete(self, path):
        async with httpx.AsyncClient(verify=not self.env.insecure) as client:
            url = self._url(path)
            await client.delete(
                url,
                headers={
                    'Content-Type': 'application/json',
                    **self._auth(),
                }
            )
