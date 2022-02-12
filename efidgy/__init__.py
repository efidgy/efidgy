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
