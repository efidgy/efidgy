import unittest

import datetime

import asyncio

import efidgy
from efidgy import models
from efidgy import exceptions
from efidgy.asyncapi import models as amodels

import logging


HOST = 'console.efidgy-dev.com'
EFIDGY_TOKEN = 'myqCTue4jyouzzFty4SfxTst9Z0N5DQD'
CUSTOMER_CODE = 'demo'


def async_test(coro):
    def wrapper(*args, **kwargs):
        loop = asyncio.new_event_loop()
        try:
            return loop.run_until_complete(coro(*args, **kwargs))
        finally:
            loop.close()
    return wrapper


class TestImpl(unittest.TestCase):
    PROJECT_NAME = 'Test Project'

    def setUp(self):
        self.env = efidgy.Env(
            host=HOST,
            token=EFIDGY_TOKEN,
            code=CUSTOMER_CODE,
            insecure=True,
        )
        self.env.use()

    def test_client_errors(self):
        with self.assertRaises(AssertionError):
            models.ProjectType.get(pk='XXX')
        with self.assertRaises(AssertionError):
            models.Project.get(foo='XXX')

    def test_authentication(self):
        env = self.env.extend(token='XXX')
        env.use()
        with self.assertRaises(exceptions.AuthenticationFailed):
            models.Project.get(pk='XXX')

    def test_not_found(self):
        with self.assertRaises(exceptions.NotFound):
            models.Project.get(pk='XXX')

    def test_validation(self):
        with self.assertRaises(exceptions.ValidationError):
            models.Project.create(
                name='Test Project',
                currency='USD',
                project_type=amodels.ProjectType(
                    code='XXX',
                ),
                shared_mode=amodels.SharedMode.PRIVATE,
            )

    def test_sync(self):
        project = models.Project.create(
            name=self.PROJECT_NAME,
            currency='USD',
            project_type=models.ProjectType(
                code=models.ProjectTypeCode.IDD_OR,
            ),
            shared_mode=models.SharedMode.PRIVATE,
        )
        project.delete()

    @async_test
    async def test_async(self):
        project = await amodels.Project.create(
            name=self.PROJECT_NAME,
            currency='USD',
            project_type=amodels.ProjectType(
                code=amodels.ProjectTypeCode.IDD_OR,
            ),
            shared_mode=amodels.SharedMode.PRIVATE,
        )
        await project.delete()


class TestModels(unittest.TestCase):
    PROJECT_NAME = 'Test Project'

    def setUp(self):
        # logging.basicConfig(
        #     format='%(asctime)s %(message)s',
        #     level=logging.DEBUG,
        # )
        self.env = efidgy.Env(
            host=HOST,
            token=EFIDGY_TOKEN,
            code=CUSTOMER_CODE,
            insecure=True,
        )
        self.env.use()

        for project in models.Project.all():
            if project.name == self.PROJECT_NAME:
                project.delete()

    def test_solve(self):
        project = models.Project.create(
            name=self.PROJECT_NAME,
            currency='USD',
            project_type=models.ProjectType(
                code=models.ProjectTypeCode.IDD_OR,
            ),
            shared_mode=models.SharedMode.PRIVATE,
        )

        store = models.idd_or.Store.create(
            project=project,
            address='6133 Broadway Terr., Oakland, CA 94618, USA',
            lat=37.842551,
            lon=-122.2331699,
            name='Delivery Inc.',
            open_time=datetime.time(8, 0),
            close_time=datetime.time(18, 0),
        )

        vehicle = models.idd_or.Vehicle.create(
            project=project,
            store=store,
            name='Gary Bailey',
            fuel_consumption=11.76,
            fuel_price=3.25,
            salary_per_duration=21,
            duration_limit=datetime.timedelta(hours=8),
        )
