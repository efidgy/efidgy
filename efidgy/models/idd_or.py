from efidgy import impl


__all__ = [
    'Store',
]


class IStore(impl.ProjectModel):
    pk = impl.fields.CharField(primary_key=True)
    address = impl.fields.CharField()
    enabled = impl.fields.BooleanField()
    lat = impl.fields.FloatField()
    lon = impl.fields.FloatField()
    point_type = impl.fields.CharField()
    name = impl.fields.CharField()
    description = impl.fields.CharField()
    open_time = impl.fields.CharField()
    close_time = impl.fields.CharField()

    class Meta:
        path = '/stores'


class IVehicleRoute(impl.Model):
    distance = impl.fields.FloatField()
    duration = impl.fields.CharField()

    class Meta:
        path = None


class IVehicle(impl.SolutionModel):
    pk = impl.fields.CharField(primary_key=True)
    name = impl.fields.CharField()
    route = impl.fields.ObjectField(model=IVehicleRoute)

    class Meta:
        path = '/vehicles'


class Store(impl.SyncChangeMixin, IStore):
    pass


class VehicleRoute(IVehicleRoute):
    pass


class Vehicle(impl.SyncChangeMixin, IVehicle):
    route = impl.fields.ObjectField(model=VehicleRoute)
