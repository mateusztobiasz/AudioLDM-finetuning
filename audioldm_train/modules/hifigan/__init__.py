from .models import Generator as Generator
from .models_hifires import Generator_HiFiRes


class AttrDict(dict):
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self
