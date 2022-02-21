import os


class Env:
    default = None

    def __init__(
            self, host=None, token=None, code=None, unit_system=None,
            insecure=False):
        self.host = host
        self.token = token
        self.code = code
        self.unit_system = unit_system
        self.insecure = insecure

    def override(self, **kwargs):
        return Env(**{
            'host': self.host,
            'token': self.token,
            'code': self.code,
            'unit_system': self.unit_system,
            'insecure': self.insecure,
            **kwargs,
        })


Env.default = Env(
    host=os.environ.get('EFIDGY_HOST', 'console.efidgy.com'),
    token=os.environ.get('EFIDGY_ACCESS_TOKEN', None),
    code=os.environ.get('EFIDGY_CUSTOMER_CODE', None),
    insecure=os.environ.get('EFIDGY_INSECURE', '0') != '0',
)
