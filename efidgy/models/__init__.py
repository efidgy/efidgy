from efidgy import fields
from efidgy import impl


from . import idd_or


__all__ = [
    idd_or,
    'SharedMode',
    'ProjectTypeCode',
    'ProjectType',
    'Project',
]


class SharedMode:
    PRIVATE = 'private'
    READONLY = 'readonly'
    EDITABLE = 'editable'


class ProjectTypeCode:
    IDD_OR = 'idd_or'


class ProjectType(impl.Model):
    code = fields.CharField()
    name = fields.CharField()
    description = fields.CharField()

    class Meta:
        pass


class Project(impl.Model):
    pk = fields.CharField()
    name = fields.CharField()
    currency = fields.CharField()
    project_type = fields.ObjectField(model=ProjectType)
    shared_mode = fields.CharField()
    demo = fields.BooleanField()

    class Meta:
        path = '/projects'
