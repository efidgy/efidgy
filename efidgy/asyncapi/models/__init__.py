from asyncio import sleep

from efidgy import impl
from efidgy import models
from efidgy.models import ProjectState
from efidgy.models import JobState
from efidgy.models import ProjectTypeCode
from efidgy.models import SharedMode
from efidgy.models import UnitSystem

from . import idd_or


__all__ = [
    idd_or,
    # 'Computation',
    # 'Issue',
    # 'IssueStats',
    # 'IssueType',
    # 'Issues',
    # 'JobMessage',
    JobState,
    'Member',
    'Project',
    ProjectState,
    # 'ProjectSummary',
    'ProjectType',
    ProjectTypeCode,
    # 'Role',
    SharedMode,
    'Solution',
    # 'SolutionSummary',
    UnitSystem,
]


class ProjectType(impl.AsyncViewMixin, models.IProjectType):
    pass


class Member(models.IMember):
    pass


class Project(impl.AsyncChangeMixin, models.IProject):
    project_type = impl.fields.ObjectField(model=ProjectType)
    member = impl.fields.ObjectField(model=Member)

    async def start_computation(self):
        c = impl.client.AsyncClient(self.get_env())
        await c.post(self._get_computation_path(), None)

    async def stop_computation(self):
        c = impl.client.AsyncClient(self.get_env())
        await c.delete(self._get_computation_path())

    async def wait_computation(self):
        while True:
            c = impl.client.AsyncClient(self.get_env())
            response = await c.get(self._get_computation_path())
            self._log_messages(response['messages'])
            if response['state'] not in [JobState.PENDING, JobState.WORKING]:
                break
            await sleep(10)

    async def computate(self):
        await self.start_computation()
        await self.wait_computation()


class Solution(impl.AsyncViewMixin, models.ISolution):
    pass