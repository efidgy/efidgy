from efidgy import impl

from . import idd_or


__all__ = [
    idd_or,
    'Project',
    'ProjectType',
    'ProjectTypeCode',
    'SharedMode',
]


class ProjectTypeCode:
    IDD_OR = 'idd_or'


class SharedMode:
    PRIVATE = 'private'
    READONLY = 'readonly'
    EDITABLE = 'editable'


class IProjectType(impl.EfidgyModel):
    code = impl.fields.CharField()
    name = impl.fields.CharField()
    description = impl.fields.CharField()

    class Meta:
        path = '/refs/project_types'


class IProject(impl.CustomerModel):
    pk = impl.fields.CharField()
    name = impl.fields.CharField()
    currency = impl.fields.CharField()
    project_type = impl.fields.ObjectField(model=IProjectType)
    shared_mode = impl.fields.CharField()
    demo = impl.fields.BooleanField()

    class Meta:
        path = '/projects'


class ProjectType(impl.SyncViewMixin, IProjectType):
    pass


class Project(impl.SyncChangeMixin, IProject):
    project_type = impl.fields.ObjectField(model=ProjectType)
