from efidgy import exceptions
from efidgy import impl
from efidgy.env import Env

import urllib.parse


__all__ = [
    'geocode',
]


def geocode(address, env=None):
    if env is None:
        env = Env.default
    env = env.override(code='efidgy')
    c = impl.client.SyncClient(env)
    data = c.get(
        '/tools/geocode/?address={}'.format(urllib.parse.quote(address)),
    )

    lat = data.get('lat')
    lon = data.get('lon')
    if lat is None or lon is None:
        raise exceptions.GeocodeError(address)

    return lat, lon
