from efidgy import impl
from efidgy import models
from efidgy.models import ProjectState
from efidgy.models import ProjectTypeCode
from efidgy.models import SharedMode

from . import idd_or


__all__ = [
    idd_or,
    'Project',
    ProjectState,
    'ProjectType',
    ProjectTypeCode,
    SharedMode,
]


class ProjectType(impl.AsyncViewMixin, models.IProjectType):
    pass


class Member(models.IMember):
    pass


class Project(impl.AsyncChangeMixin, models.IProject):
    project_type = impl.fields.ObjectField(model=ProjectType)
    member = impl.fields.ObjectField(model=Member)


class Solution(impl.AsyncViewMixin, models.ISolution):
    pass
