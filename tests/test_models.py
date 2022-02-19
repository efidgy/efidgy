import unittest

import datetime

import asyncio

import os

import efidgy
from efidgy import models
from efidgy import tools
from efidgy import exceptions
from efidgy.asyncapi import models as amodels
from efidgy.asyncapi import tools as atools

import logging


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
            host=os.environ.get('EFIDGY_HOST', 'console.efidgy.com'),
            token=os.environ.get('EFIDGY_ACCESS_TOKEN', ''),
            code=os.environ.get('EFIDGY_CUSTOMER_CODE', 'demo'),
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
                project_type=models.ProjectType(
                    code='XXX',
                ),
                shared_mode=models.SharedMode.PRIVATE,
            )

    @async_test
    async def test_avalidation(self):
        with self.assertRaises(exceptions.ValidationError):
            await amodels.Project.create(
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
        #     format='%(asctime)s %(name)s %(message)s',
        #     level=logging.DEBUG,
        # )
        self.env = efidgy.Env(
            host=os.environ.get('EFIDGY_HOST', 'console.efidgy.com'),
            token=os.environ.get('EFIDGY_ACCESS_TOKEN', ''),
            code=os.environ.get('EFIDGY_CUSTOMER_CODE', 'demo'),
            insecure=True,
        )
        self.env.use()

        for project in models.Project.all():
            if project.name == self.PROJECT_NAME:
                project.delete()

        self.stores = [
            {
                'address': '6133 Broadway Terr., Oakland, CA 94618, USA',
                'name': 'Delivery Inc.',
                'open_time': datetime.time(8, 0),
                'close_time': datetime.time(18, 0),
            },
        ]

        self.vehicles = [
            {
                'store': 'Delivery Inc.',
                'name': 'Gary Bailey',
                'fuel_consumption': 11.76,
                'fuel_price': 3.25,
                'salary_per_duration': 21,
                'duration_limit': datetime.timedelta(hours=9),
            },
        ]

        self.orders = [
            {
                'store': 'Delivery Inc.',
                'name': '#00001',
                'address': '1 Downey Pl, Oakland, CA 94610, USA',
                'ready_time': datetime.time(8, 0),
                'delivery_time_from': datetime.time(12, 0),
                'delivery_time_to': datetime.time(16, 0),
                'load_duration': datetime.timedelta(minutes=1),
                'unload_duration': datetime.timedelta(minutes=5),
                'boxes': 1,
                'volume': 3.53,
                'weight': 22.05,
            },
        ]

    def _repr_point(self, point):
        return point.name

    def _print_vehicle(self, vehicle):
        print(vehicle.name)
        if vehicle.route is None:
            return
        prev_schedule = None
        for schedule in vehicle.route.schedule:
            print('{at}\t{arr}\t{dep}'.format(
                at=self._repr_point(schedule.start_point),
                arr=prev_schedule.arrival_time if prev_schedule else None,
                dep=schedule.departure_time,
            ))
            prev_schedule = schedule
        if prev_schedule:
            print('{at}\t{arr}\t{dep}'.format(
                at=self._repr_point(prev_schedule.end_point),
                arr=prev_schedule.arrival_time,
                dep=None,
            ))

    def _print_order(self, order):
        print(order.name)
        if order.route is None:
            return
        prev_schedule = None
        for schedule in order.route.schedule:
            print('{at}\t{arr}\t{dep}'.format(
                at=self._repr_point(schedule.start_point),
                arr=prev_schedule.arrival_time if prev_schedule else None,
                dep=schedule.departure_time,
            ))
            prev_schedule = schedule
        if prev_schedule:
            print('{at}\t{arr}\t{dep}'.format(
                at=self._repr_point(prev_schedule.end_point),
                arr=prev_schedule.arrival_time,
                dep=None,
            ))

    def test_solve(self):
        return
        project = models.Project.create(
            name=self.PROJECT_NAME,
            currency='USD',
            project_type=models.ProjectType(
                code=models.ProjectTypeCode.IDD_OR,
            ),
            shared_mode=models.SharedMode.PRIVATE,
        )

        stores = {}
        for data in self.stores:
            lat, lon = tools.geocode(data['address'])
            store = models.idd_or.Store.create(
                project=project,
                lat=lat,
                lon=lon,
                **data,
            )
            stores[store.name] = store

        vehicles = {}
        for data in self.vehicles:
            data['store'] = stores[data['store']]
            vehicle = models.idd_or.Vehicle.create(
                project=project,
                **data,
            )
            vehicles[vehicle.name] = vehicle

        orders = {}
        for data in self.orders:
            lat, lon = tools.geocode(data['address'])
            data['store'] = stores[data['store']]
            order = models.idd_or.Order.create(
                project=project,
                lat=lat,
                lon=lon,
                **data,
            )
            orders[order.name] = order

        project.computate()

        solutions = models.Solution.all(
            project=project,
        )
        self.assertTrue(len(solutions) > 0)
        solution = solutions[0]

        vehicles = models.idd_or.Vehicle.all(
            project=project,
            solution=solution,
        )
        for vehicle in vehicles:
            self._print_vehicle(vehicle)

        orders = models.idd_or.Order.all(
            project=project,
            solution=solution,
        )
        for order in orders:
            self._print_order(order)

    @async_test
    async def test_asolve(self):
        project = await amodels.Project.create(
            name=self.PROJECT_NAME,
            currency='USD',
            project_type=amodels.ProjectType(
                code=amodels.ProjectTypeCode.IDD_OR,
            ),
            shared_mode=amodels.SharedMode.PRIVATE,
        )

        stores = {}
        for data in self.stores:
            lat, lon = await atools.geocode(data['address'])
            store = await amodels.idd_or.Store.create(
                project=project,
                lat=lat,
                lon=lon,
                **data,
            )
            stores[store.name] = store

        vehicles = {}
        for data in self.vehicles:
            data['store'] = stores[data['store']]
            vehicle = await amodels.idd_or.Vehicle.create(
                project=project,
                **data,
            )
            vehicles[vehicle.name] = vehicle

        orders = {}
        for data in self.orders:
            lat, lon = await atools.geocode(data['address'])
            data['store'] = stores[data['store']]
            order = await amodels.idd_or.Order.create(
                project=project,
                lat=lat,
                lon=lon,
                **data,
            )
            orders[order.name] = order

        await project.computate()

        solutions = await amodels.Solution.all(
            project=project,
        )
        self.assertTrue(len(solutions) > 0)
        solution = solutions[0]

        vehicles = await amodels.idd_or.Vehicle.all(
            project=project,
            solution=solution,
        )
        for vehicle in vehicles:
            self._print_vehicle(vehicle)

        orders = await amodels.idd_or.Order.all(
            project=project,
            solution=solution,
        )
        for order in orders:
            self._print_order(order)