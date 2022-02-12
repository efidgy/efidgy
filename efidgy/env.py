class Env:
    current = None

    HOST = 'console.efidgy.com'

    def __init__(self, host=None, token=None, code=None, insecure=False):
        self.host = host if host is not None else self.HOST
        self.token = token
        self.code = code
        self.insecure = insecure

    def use(self):
        Env.current = self

    @classmethod
    def extend(cls, env, **kwargs):
        return Env(
            host=kwargs.get('host', env.host),
            token=kwargs.get('token', env.token),
            code=kwargs.get('code', env.code),
            insecure=kwargs.get('insecure', env.insecure),
        )
