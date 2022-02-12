from efidgy import impl
from efidgy import models


__all__ = [
    'Store',
]


class Store(impl.AsyncChangeMixin, models.idd_or.Store):
    pass
