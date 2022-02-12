from efidgy import impl
from efidgy import fields


__all__ = [
    'Store',
]


class Store(impl.ProjectModel):
    pk = fields.CharField()
    address = fields.CharField()
    enabled = fields.BooleanField()
    lat = fields.FloatField()
    lon = fields.FloatField()
    point_type = fields.CharField()
    name = fields.CharField()
    description = fields.CharField()
    open_time = fields.CharField()
    close_time = fields.CharField()

    class Meta:
        path = '/stores'
