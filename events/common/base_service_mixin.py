class BaseServiceMixin:
    def __init__(self, *args, **kwargs):
        pass

    @classmethod
    def call(cls, *args, **kwargs):
        instance = cls(*args, **kwargs)
        instance.exec()

    def exec(self):
        raise NotImplementedError
