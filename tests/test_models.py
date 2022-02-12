import unittest

import asyncio

import efidgy
from efidgy import models
from efidgy.asyncapi import models as amodels

import logging


def async_test(coro):
    def wrapper(*args, **kwargs):
        loop = asyncio.new_event_loop()
        try:
            return loop.run_until_complete(coro(*args, **kwargs))
        finally:
            loop.close()
    return wrapper


class TestModels(unittest.TestCase):
    HOST = 'console.efidgy-dev.com'
    EFIDGY_TOKEN = 'myqCTue4jyouzzFty4SfxTst9Z0N5DQD'
    CUSTOMER_CODE = 'demo'
    PROJECT_NAME = 'Test Project'

    def setUp(self):
        # logging.basicConfig(
        #     format='%(asctime)s %(message)s',
        #     level=logging.DEBUG,
        # )
        env = efidgy.Env(
            host=self.HOST,
            token=self.EFIDGY_TOKEN,
            code=self.CUSTOMER_CODE,
            insecure=True,
        )
        env.use()

    #     for project in models.Project.all():
    #         if project.name == self.PROJECT_NAME:
    #             project.delete()

    # def test_sync(self):
    #     project = models.Project.create(
    #         name=self.PROJECT_NAME,
    #         currency='USD',
    #         project_type=models.ProjectType(
    #             code=models.ProjectTypeCode.IDD_OR,
    #         ),
    #         shared_mode=models.SharedMode.PRIVATE,
    #         demo=False,
    #     )

    #     store = models.idd_or.Store.create(
    #         project=project,
    #         address='6133 Broadway Terr., Oakland, CA 94618, USA',
    #         lat=37.842551,
    #         lon=-122.2331699,
    #         name='Delivery Inc.',
    #     )

    #     store.name = 'Delivery Inc. 2'
    #     store.save()
    #     store.delete()

    #     store = models.idd_or.Store.create(
    #         project=project,
    #         address='6133 Broadway Terr., Oakland, CA 94618, USA',
    #         lat=37.842551,
    #         lon=-122.2331699,
    #         name='Delivery Inc.',
    #     )
    #     for store in models.idd_or.Store.all(project=project):
    #         store.delete()

    # @async_test
    # async def test_async(self):
    #     project = await amodels.Project.create(
    #         name=self.PROJECT_NAME,
    #         currency='USD',
    #         project_type=amodels.ProjectType(
    #             code=amodels.ProjectTypeCode.IDD_OR,
    #         ),
    #         shared_mode=amodels.SharedMode.PRIVATE,
    #         demo=False,
    #     )

    #     store = await amodels.idd_or.Store.create(
    #         project=project,
    #         address='6133 Broadway Terr., Oakland, CA 94618, USA',
    #         lat=37.842551,
    #         lon=-122.2331699,
    #         name='Delivery Inc.',
    #     )

    #     print(store)

    #     store.name = 'Delivery Inc. 2'
    #     await store.save()
    #     await store.delete()

    def test_solution(self):
        project_type = models.ProjectType.get(code='idd_or')
        print(project_type)
        project = models.Project.get(pk='MS1X74D8qE4')
        solutions = models.Solution.all(project=project)
        solution = solutions[0]

        vehicles = models.idd_or.Vehicle.all(project=project)
        for vehicle in vehicles:
            print(vehicle)

        vehicles = models.idd_or.Vehicle.all(project=project, solution=solution)
        for vehicle in vehicles:
            print(vehicle)
