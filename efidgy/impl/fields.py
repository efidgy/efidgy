from datetime import time
import re


class Field:
    def __init__(self, primary_key=False, required=True):
        self.required = required
        self.primary_key = primary_key

    def decode(self, value):
        return value

    def encode(self, value):
        return value


class BooleanField(Field):
    pass


class FloatField(Field):
    pass


class CharField(Field):
    pass


class PrimaryKey(CharField):
    def __init__(self, **kwargs):
        kwargs['primary_key'] = True
        super().__init__(**kwargs)


class TimeField(Field):
    def encode(self, value):
        if value is None:
            return None
        return '{:02d}:{:02d}'.format(value.hour, value.minute)

    def decode(self, value):
        if value is None:
            return None
        m = re.match(r'(\d{2}):(\d{2})', value)
        assert m, (
            'Unexpected time value: {}'.format(value)
        )
        return time(int(m[1]), int(m[2]))


class DictField(Field):
    pass


class ObjectField(Field):
    def __init__(self, model=None, **kwargs):
        super().__init__(**kwargs)
        self.model = model

    def decode(self, value):
        if value is None:
            return None
        return self.model.decode(value)

    def encode(self, value):
        if value is None:
            return None
        return self.model.encode(value)


class ListField(Field):
    def __init__(self, item=None, **kwargs):
        super().__init__(**kwargs)
        self.item = item

    def decode(self, value):
        if value is None:
            return None
        ret = []
        for item in value:
            ret.append(self.item.decode(item))
        return ret

    def encode(self, value):
        if value is None:
            return None
        ret = []
        for item in value:
            ret.append(self.item.encode(item))
        return ret
