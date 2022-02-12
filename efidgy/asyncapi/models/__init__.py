from efidgy import impl
from efidgy import models
from efidgy.models import ProjectTypeCode
from efidgy.models import SharedMode

from . import idd_or


__all__ = [
    idd_or,
    'Project',
    'ProjectType',
    ProjectTypeCode,
    SharedMode,
]


class ProjectType(impl.AsyncViewMixin, models.IProjectType):
    pass


class Project(impl.AsyncChangeMixin, models.IProject):
    project_type = impl.fields.ObjectField(model=ProjectType)
