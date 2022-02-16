from efidgy import impl

from . import idd_or


__all__ = [
    idd_or,
    'Project',
    'ProjectType',
    'ProjectTypeCode',
    'SharedMode',
    'Solution',
]


class UnitSystem:
    METRIC = 'metric'
    IMPERIAL = 'imperial'


class ProjectTypeCode:
    IDD_OR = 'idd_or'


class SharedMode:
    PRIVATE = 'private'
    READONLY = 'readonly'
    EDITABLE = 'editable'


class ProjectState:
    IDLE = 'idle'
    COMPUTATING = 'computating'
    IMPORTING = 'importing'


class IProjectType(impl.EfidgyModel):
    code = impl.fields.PrimaryKey()
    name = impl.fields.CharField()
    description = impl.fields.CharField()

    class Meta:
        path = '/refs/project_types'


class IMember(impl.Model):
    pk = impl.fields.PrimaryKey()
    email = impl.fields.CharField()
    first_name = impl.fields.CharField()
    last_name = impl.fields.CharField()
    role = impl.fields.CharField()


class IProject(impl.CustomerModel):
    pk = impl.fields.PrimaryKey()
    name = impl.fields.CharField()
    currency = impl.fields.CharField()
    project_type = impl.fields.ObjectField(model=IProjectType)
    shared_mode = impl.fields.CharField()
    owner = impl.fields.ObjectField(model=IMember)
    demo = impl.fields.BooleanField()
    state = impl.fields.CharField()
    outdated = impl.fields.BooleanField()
    progress = impl.fields.FloatField()
    issue_stats = impl.fields.DictField()
    summary = impl.fields.DictField()

    class Meta:
        path = '/projects'


class ISolution(impl.ProjectModel):
    pk = impl.fields.PrimaryKey()
    cost = impl.fields.FloatField()
    outdated = impl.fields.BooleanField()

    class Meta:
        path = '/solutions'


class ProjectType(impl.SyncViewMixin, IProjectType):
    pass


class Member(IMember):
    pass


class Project(impl.SyncChangeMixin, IProject):
    project_type = impl.fields.ObjectField(model=ProjectType)
    member = impl.fields.ObjectField(model=Member)


class Solution(impl.SyncViewMixin, ISolution):
    pass
