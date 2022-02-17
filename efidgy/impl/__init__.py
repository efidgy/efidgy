import logging

from efidgy import Env

from . import client
from . import fields


module_logger = logging.getLogger('efidgy')


class ModelMeta(type):
    @classmethod
    def _iter_fields(cls, obj):
        for base in obj.__bases__:
            for field_name, field in cls._iter_fields(base):
                yield field_name, field

            for field_name, field in vars(obj).items():
                if not isinstance(field, fields.Field):
                    continue
                yield field_name, field

    @classmethod
    def _find_meta_bases(cls, bases):
        ret = []
        for base in bases:
            meta = getattr(base, 'Meta', None)
            if meta is None:
                ret.extend(cls._find_meta_bases(base.__bases__))
            else:
                ret.append(meta)
        return ret

    @classmethod
    def _meta_factory(cls, bases):
        return type('Meta', tuple(cls._find_meta_bases(bases)), {})

    @classmethod
    def _repr(cls):
        def repr_impl(self):
            fields = []
            for field in self.Meta.fields:
                value = getattr(self, field.name, None)
                if isinstance(value, str):
                    value = '"{}"'.format(value)
                fields.append('{}={}'.format(field.name, value))
            return '<{} {}>'.format(self.__class__.__name__, ' '.join(fields))
        return repr_impl

    def __new__(cls, name, bases, attrs):
        if 'Meta' not in attrs:
            attrs['Meta'] = cls._meta_factory(bases)

        Model = super().__new__(cls, name, bases, attrs)

        Model.Meta.fields = []
        for field_name, field in cls._iter_fields(Model):
            field.name = field_name
            Model.Meta.fields.append(field)
            if (
                field.primary_key
                and getattr(Model.Meta, 'primary_key', None) is None
            ):
                Model.Meta.primary_key = field

        Model.__repr__ = cls._repr()

        return Model


class Model(metaclass=ModelMeta):
    class Meta:
        path = None
        fields = []
        primary_key = None

    @classmethod
    def decode(cls, data, **kwargs):
        kw = {**kwargs}
        for field in cls.Meta.fields:
            kw[field.name] = field.decode(data.get(field.name), **kwargs)
        return cls(**kw)

    @classmethod
    def encode(cls, obj):
        ret = {}
        for field in obj.Meta.fields:
            value = field.encode(getattr(obj, field.name))
            if value is not None:
                ret[field.name] = value
        return ret

    @classmethod
    def get_path(cls, context):
        return cls.Meta.path

    @classmethod
    def get_env(cls):
        return Env.current

    def get_context(self):
        return {}

    def __init__(self, **kwargs):
        for field in self.Meta.fields:
            setattr(self, field.name, kwargs.get(field.name))


class EfidgyModel(Model):
    @classmethod
    def get_env(cls):
        return super().get_env().extend(code='efidgy')


class CustomerModel(Model):
    pass


class ProjectModel(Model):
    @classmethod
    def get_path(cls, context):
        project = context.get('project')
        assert project is not None, (
            'Project not passed.'
        )
        return '/projects/{project}{path}'.format(
            project=project.pk,
            path=cls.Meta.path,
        )

    def get_context(self):
        return {
            **super().get_context(),
            'project': self.project,
        }

    def __init__(self, project=None, **kwargs):
        super().__init__(**kwargs)
        assert project is not None, (
            'Project not specified.'
        )
        self.project = project


class SolutionModel(ProjectModel):
    @classmethod
    def get_path(cls, context):
        solution = context.get('solution')
        if solution is None:
            return super().get_path(context)
        project = context.get('project')
        return '/projects/{project}/solutions/{solution}{path}'.format(
            project=project.pk,
            solution=solution.pk,
            path=cls.Meta.path,
        )

    def get_context(self):
        return {
            **super().get_context(),
            'solution': self.solution,
        }

    def __init__(self, solution=None, **kwargs):
        super().__init__(**kwargs)
        self.solution = solution


class SyncAllMixin:
    @classmethod
    def all(cls, **kwargs):
        c = client.SyncClient(cls.get_env())
        path = cls.get_path(kwargs)
        ret = []
        for data in c.get(path):
            ret.append(cls.decode(data, **kwargs))
        return ret


class SyncGetMixin:
    @classmethod
    def get(cls, **kwargs):
        c = client.SyncClient(cls.get_env())
        path = cls.get_path(kwargs)
        pk_name = cls.Meta.primary_key.name
        pk = kwargs.get(pk_name, None)
        assert pk is not None, (
            'Primary key not provided: {}'.format(pk_name),
        )
        data = c.get('{}/{}'.format(path, pk))
        return cls.decode(data, **kwargs)

    def refresh(self):
        pk_name = self.Meta.primary_key.name
        pk = getattr(self, pk_name, None)
        kwargs = {
            **self.get_context(),
            pk_name: pk,
        }
        obj = self.get(**kwargs)
        for field in self.Meta.fields:
            setattr(self, field.name, getattr(obj, field.name))


class SyncCreateMixin:
    @classmethod
    def create(cls, **kwargs):
        c = client.SyncClient(cls.get_env())
        path = cls.get_path(kwargs)
        obj = cls(**kwargs)
        data = c.post(path, cls.encode(obj))
        return cls.decode(data, **kwargs)


class SyncSaveMixin:
    def save(self):
        c = client.SyncClient(self.get_env())
        path = self.get_path(self.get_context())
        c.put('{}/{}'.format(path, self.pk), self.encode(self))


class SyncDeleteMixin:
    def delete(self):
        c = client.SyncClient(self.get_env())
        path = self.get_path(self.get_context())
        c.delete('{}/{}'.format(path, self.pk))


class SyncViewMixin(
            SyncAllMixin,
            SyncGetMixin,
        ):
    pass


class SyncChangeMixin(
            SyncCreateMixin,
            SyncSaveMixin,
            SyncDeleteMixin,
            SyncViewMixin
        ):
    pass


class AsyncAllMixin:
    @classmethod
    async def all(cls, **kwargs):
        c = client.AsyncClient(cls.get_env())
        path = cls.get_path(kwargs)
        ret = []
        for data in await c.get(path):
            ret.append(cls.decode(data, **kwargs))
        return ret


class AsyncGetMixin:
    @classmethod
    async def get(cls, **kwargs):
        c = client.AsyncClient(cls.get_env())
        path = cls.get_path(kwargs)
        pk_name = cls.Meta.primary_key.name
        pk = kwargs.get(pk_name, None)
        assert pk is not None, (
            'Primary key not provided: {}'.format(pk_name),
        )
        data = await c.get('{}/{}'.format(path, pk))
        return cls.decode(data, **kwargs)

    async def refresh(self):
        pk_name = self.Meta.primary_key.name
        pk = getattr(self, pk_name, None)
        kwargs = {
            **self.get_context(),
            pk_name: pk,
        }
        obj = await self.get(**kwargs)
        for field in self.Meta.fields:
            setattr(self, field.name, getattr(obj, field.name))


class AsyncCreateMixin:
    @classmethod
    async def create(cls, **kwargs):
        c = client.AsyncClient(cls.get_env())
        path = cls.get_path(kwargs)
        obj = cls(**kwargs)
        data = await c.post(path, cls.encode(obj))
        return cls.decode(data, **kwargs)


class AsyncSaveMixin:
    async def save(self, **kwargs):
        c = client.AsyncClient(self.get_env())
        path = self.get_path(self.get_context())
        await c.put(
            '{}/{}'.format(path, self.pk),
            self.encode(self),
        )


class AsyncDeleteMixin:
    async def delete(self, **kwargs):
        c = client.AsyncClient(self.get_env())
        path = self.get_path(self.get_context())
        await c.delete('{}/{}'.format(path, self.pk))


class AsyncViewMixin(
            AsyncAllMixin,
            AsyncGetMixin,
        ):
    pass


class AsyncChangeMixin(
            AsyncCreateMixin,
            AsyncSaveMixin,
            AsyncDeleteMixin,
            AsyncViewMixin,
        ):
    pass
