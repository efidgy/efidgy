from efidgy import impl


__all__ = [
    'Store',
]


class PointType:
    STORE = 'store'
    ORDER = 'order'


class IPoint(impl.ProjectModel):
    pk = impl.fields.PrimaryKey()
    address = impl.fields.CharField()
    enabled = impl.fields.BooleanField()
    lat = impl.fields.FloatField()
    lon = impl.fields.FloatField()
    point_type = impl.fields.CharField()


class IStore(IPoint):
    name = impl.fields.CharField()
    description = impl.fields.CharField()
    open_time = impl.fields.TimeField()
    close_time = impl.fields.TimeField()
    issues = impl.fields.DictField()

    class Meta:
        path = '/stores'


class IVehicleRoute(impl.Model):
    distance = impl.fields.FloatField()
    duration = impl.fields.CharField()

    class Meta:
        path = None


class IVehicle(impl.SolutionModel):
    pk = impl.fields.PrimaryKey()
    name = impl.fields.CharField()
    description = impl.fields.CharField()
    enabled = impl.fields.BooleanField()
    features = impl.fields.ListField(item=impl.fields.CharField())
    store = impl.fields.ObjectField(model=IStore)
    route = impl.fields.ObjectField(model=IVehicleRoute)

    class Meta:
        path = '/vehicles'


class Store(impl.SyncChangeMixin, IStore):
    pass


class VehicleRoute(IVehicleRoute):
    pass


class Vehicle(impl.SyncChangeMixin, IVehicle):
    store = impl.fields.ObjectField(model=Store)
    route = impl.fields.ObjectField(model=VehicleRoute)
