import datetime

import re

from math import floor

from . import routines


class Field:
    def __init__(self, primary_key=False, required=True):
        self.required = required
        self.primary_key = primary_key

    def decode(self, value, **kwargs):
        return value

    def encode(self, value):
        return value


class BooleanField(Field):
    pass


class FloatField(Field):
    pass


class IntegerField(Field):
    pass


class CharField(Field):
    pass


class PrimaryKey(CharField):
    def __init__(self, **kwargs):
        kwargs['primary_key'] = True
        super().__init__(**kwargs)


class TimeField(Field):
    def decode(self, value, **kwargs):
        if value is None:
            return None
        m = re.match(r'(\d{2}):(\d{2})', value)
        assert m, (
            'Unexpected time value: {}'.format(value)
        )
        return datetime.time(int(m[1]), int(m[2]))

    def encode(self, value):
        if value is None:
            return None
        return '{:02d}:{:02d}'.format(value.hour, value.minute)


class DurationField(Field):
    def decode(self, value, **kwargs):
        if value is None:
            return None
        m = re.match(r'(\d+):(\d{2})', value)
        assert m, (
            'Unexpected duration value: {}'.format(value)
        )
        return datetime.timedelta(hours=int(m[1]), minutes=int(m[2]))

    def encode(self, value):
        if value is None:
            return None
        seconds = value.total_seconds()
        hours = int(floor(seconds / 3600))
        minutes = int(floor(seconds / 60) % 60)
        return '{:d}:{:02d}'.format(hours, minutes)


class DictField(Field):
    pass


class ObjectField(Field):
    def __init__(self, model=None, **kwargs):
        super().__init__(**kwargs)
        self._model = model

    @property
    def model(self):
        if isinstance(self._model, str):
            self._model = routines.import_string(self._model)
        return self._model

    def decode(self, value, **kwargs):
        if value is None:
            return None
        return self.model.decode(value, **kwargs)

    def encode(self, value):
        if value is None:
            return None
        assert isinstance(value, self.model), (
            '{} instance expected: {}'.format(self.model, type(value))
        )
        return self.model.encode(value)


class PolymorphObjectField(Field):
    def __init__(self, lookup_field=None, models=None, **kwargs):
        super().__init__(**kwargs)
        self.lookup_field = lookup_field
        self.models = models

    def _get_model(self, value):
        object_type = value.get(self.lookup_field)
        assert object_type is not None, (
            'Lookup field not found: {}'.format(self.lookup_field)
        )

        model = self.models.get(object_type)
        assert model is not None, (
            'Model not found: {}'.format(object_type)
        )

        if isinstance(model, str):
            model = routines.import_string(model)
            self.models[object_type] = model

        return model

    def decode(self, value, **kwargs):
        if value is None:
            return None

        return self._get_model(value).decode(value, **kwargs)

    def encode(self, value):
        if value is None:
            return None

        model = self._get_model(value)

        assert isinstance(value, model), (
            '{} instance expected: {}'.format(model, type(value))
        )

        return model.encode(value)


class ListField(Field):
    def __init__(self, item=None, **kwargs):
        super().__init__(**kwargs)
        self._item = item

    @property
    def item(self):
        if isinstance(self._item, str):
            self._item = routines.import_string(self._item)
        return self._item

    def decode(self, value, **kwargs):
        if value is None:
            return None
        ret = []
        for item in value:
            ret.append(self.item.decode(item, **kwargs))
        return ret

    def encode(self, value):
        if value is None:
            return None
        ret = []
        for item in value:
            ret.append(self.item.encode(item))
        return ret
