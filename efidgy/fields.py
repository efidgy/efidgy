class Field:
    def __init__(self):
        pass

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


class ObjectField(Field):
    def __init__(self, model=None, **kwargs):
        super().__init__(**kwargs)
        self.model = model

    def decode(self, value):
        return self.model.decode(value)

    def encode(self, value):
        return self.model.encode(value)
