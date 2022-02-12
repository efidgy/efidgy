from efidgy import impl


__all__ = [
    'Store',
]


class IStore(impl.ProjectModel):
    pk = impl.fields.CharField()
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


class Store(impl.SyncChangeMixin, IStore):
    pass
