from efidgy import impl
from efidgy import models


__all__ = [
    'Store',
]


class Store(impl.SyncChangeMixin, models.idd_or.Store):
    pass
