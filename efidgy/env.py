class Env:
    current = None

    HOST = 'console.efidgy.com'

    def __init__(
            self, host=None, token=None, code=None, unit_system=None,
            insecure=False):
        self.host = host if host is not None else self.HOST
        self.token = token
        self.code = code
        self.unit_system = unit_system
        self.insecure = insecure

    def use(self):
        Env.current = self

    def extend(self, **kwargs):
        return Env(
            **{
                'host': self.host,
                'token': self.token,
                'code': self.code,
                'unit_system': self.unit_system,
                'insecure': self.insecure,
                **kwargs,
            }
        )
