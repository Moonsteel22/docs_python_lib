from abc import ABC
from enum import Enum
from typing import Dict


class DocumentObject(ABC):
    def _normalize(self, key: str):
        _key = key.split("_")
        key = _key.pop(0)
        key += "".join(list(map(lambda x: x.capitalize(), _key)))
        return key

    def _dict(self):
        result = {}
        for key, value in self.__dict__.items():
            key = self._normalize(key)
            if hasattr(value, "_dict"):
                result[key] = value._dict()
            elif isinstance(value, Enum):
                result[key] = value.value
            else:
                result[key] = value
        return result


class DocumentRequest(DocumentObject):
    def _to_dict(self) -> Dict:

        if not hasattr(self, "__dict__"):
            return {}

        return self._dict()
