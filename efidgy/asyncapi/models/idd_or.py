from efidgy import impl
from efidgy import models
from efidgy.models.idd_or import PointType


__all__ = [
    'Order',
    'OrderRoute',
    'OrderSchedule',
    'Path',
    'Point',
    PointType,
    'Store',
    'Vehicle',
    'VehicleRoute',
    'VehicleSchedule',
]


class Point(models.idd_or.IPoint):
    pass


class Store(models.idd_or.IStore):
    class service(impl.service.AsyncChangeMixin, impl.service.ProjectService):
        path = '/stores'


class Path(models.idd_or.IPath):
    pass


class Order(models.idd_or.IOrder):
    store = impl.fields.ObjectField(model=Store)

    class service(impl.service.AsyncChangeMixin, impl.service.SolutionService):
        path = '/orders'


class OrderSchedule(models.idd_or.IOrderSchedule):
    start_point = impl.fields.PolymorphObjectField(
        lookup_field='point_type',
        models={
            PointType.STORE: Store,
            PointType.ORDER: Order,
        },
    )
    end_point = impl.fields.PolymorphObjectField(
        lookup_field='point_type',
        models={
            PointType.STORE: Store,
            PointType.ORDER: Order,
        },
    )
    path = impl.fields.ObjectField(model=Path)


class VehicleSchedule(models.idd_or.IVehicleSchedule):
    start_point = impl.fields.PolymorphObjectField(
        lookup_field='point_type',
        models={
            PointType.STORE: Store,
            PointType.ORDER: Order,
        },
    )
    end_point = impl.fields.PolymorphObjectField(
        lookup_field='point_type',
        models={
            PointType.STORE: Store,
            PointType.ORDER: Order,
        },
    )
    path = impl.fields.ObjectField(model=Path)
    orders = impl.fields.ListField(item=Order)


class OrderRoute(models.idd_or.IOrderRoute):
    vehicle = impl.fields.ObjectField(
        model='efidgy.asyncapi.models.idd_or.Vehicle',
    )
    schedule = impl.fields.ListField(item=OrderSchedule)


class VehicleRoute(models.idd_or.IVehicleRoute):
    pass


class Vehicle(models.idd_or.IVehicle):
    store = impl.fields.ObjectField(model=Store)
    route = impl.fields.ObjectField(model=VehicleRoute)

    class service(impl.service.AsyncChangeMixin, impl.service.SolutionService):
        path = '/vehicles'
