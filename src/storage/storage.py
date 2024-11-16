import settings
from utils.capped_dict import CappedDict

__all__ = ['rooms']

rooms = CappedDict(capacity=settings.MAX_ROOMS_COUNT)
