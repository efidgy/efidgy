from efidgy import impl
from efidgy import models
from efidgy.models.idd_or import PointType


__all__ = [
    PointType,
    'Store',
]


class Store(impl.AsyncChangeMixin, models.idd_or.IStore):
    pass


class VehicleRoute(models.idd_or.IVehicleRoute):
    pass


class Vehicle(impl.AsyncChangeMixin, models.idd_or.IVehicle):
    store = impl.fields.ObjectField(model=Store)
    route = impl.fields.ObjectField(model=VehicleRoute)
