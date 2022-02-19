from efidgy import exceptions
from efidgy import impl
from efidgy.env import Env


__all__ = [
    'geocode',
]


def geocode(address, env=None):
    if env is None:
        env = Env.current
    env = env.extend(code='efidgy')
    c = impl.client.SyncClient(env)
    data = c.get('/tools/geocode/?address={}'.format(address))

    lat = data.get('lat')
    lon = data.get('lon')
    if lat is None or lon is None:
        raise exceptions.GeocodeError(address)

    return lat, lon
