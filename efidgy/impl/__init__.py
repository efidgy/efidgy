from collections import deque

from efidgy import Env
from efidgy.fields import Field

from . import client


class ModelMeta(type):
    @classmethod
    def _iter_fields(cls, obj):
        q = deque([obj])
        while q:
            o = q.popleft()
            for field_name, field in o.__dict__.items():
                if not isinstance(field, Field):
                    continue
                yield field_name, field
            q.extend(o.__bases__)

    @classmethod
    def __new__(cls, *args):
        Model = super().__new__(*args)

        Model.Meta.fields = []
        for field_name, field in cls._iter_fields(Model):
            field.name = field_name
            Model.Meta.fields.append(field)

        return Model


class Model(metaclass=ModelMeta):
    class Meta:
        pass

    @classmethod
    def decode(cls, data, **kwargs):
        kw = {**kwargs}
        for field in cls.Meta.fields:
            kw[field.name] = field.decode(data.get(field.name))
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

    def get_context(self):
        return {}

    def __init__(self, **kwargs):
        for field in self.Meta.fields:
            setattr(self, field.name, kwargs.get(field.name))


class ProjectModel(Model):
    @classmethod
    def get_path(cls, context):
        project = context.get('project')
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
        self.project = project


class SyncListMixin:
    @classmethod
    def all(cls, **kwargs):
        c = client.SyncClient(Env.current)
        path = cls.get_path(kwargs)
        ret = []
        for data in c.get(path):
            ret.append(cls.decode(data, **kwargs))
        return ret


class SyncCreateMixin:
    @classmethod
    def create(cls, **kwargs):
        c = client.SyncClient(Env.current)
        path = cls.get_path(kwargs)
        obj = cls(**kwargs)
        data = c.post(path, cls.encode(obj))
        return cls.decode(data, **kwargs)


class SyncSaveMixin:
    def save(self):
        c = client.SyncClient(Env.current)
        path = self.get_path(self.get_context())
        c.put('{}/{}'.format(path, self.pk), self.encode(self))


class SyncDeleteMixin:
    def delete(self):
        c = client.SyncClient(Env.current)
        path = self.get_path(self.get_context())
        c.delete('{}/{}'.format(path, self.pk))


class SyncViewMixin(SyncListMixin):
    pass


class SyncChangeMixin(
            SyncCreateMixin,
            SyncSaveMixin,
            SyncDeleteMixin,
            SyncViewMixin
        ):
    pass


class AsyncListMixin:
    @classmethod
    async def all(cls, **kwargs):
        c = client.AsyncClient(Env.current)
        path = cls.get_path(kwargs)
        ret = []
        for data in await c.get(path):
            ret.append(cls.decode(data, **kwargs))
        return ret


class AsyncCreateMixin:
    @classmethod
    async def create(cls, **kwargs):
        c = client.AsyncClient(Env.current)
        path = cls.get_path(kwargs)
        obj = cls(**kwargs)
        data = await c.post(path, cls.encode(obj))
        return cls.decode(data, **kwargs)


class AsyncSaveMixin:
    async def save(self, **kwargs):
        c = client.AsyncClient(Env.current)
        path = self.get_path(self.get_context())
        await c.put('{}/{}'.format(path, self.pk), self.encode(self))


class AsyncDeleteMixin:
    async def delete(self, **kwargs):
        c = client.AsyncClient(Env.current)
        path = self.get_path(self.get_context())
        await c.delete('{}/{}'.format(path, self.pk))


class AsyncViewMixin(AsyncListMixin):
    pass


class AsyncChangeMixin(
            AsyncCreateMixin,
            AsyncSaveMixin,
            AsyncDeleteMixin,
            AsyncViewMixin,
        ):
    pass
