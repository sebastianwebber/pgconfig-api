from enum import Enum
import json

class EnumEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Enum):
            return str(obj.name)

        return json.JSONEncoder.default(self, obj)

def as_enum(d):
    if "__enum__" in d:
        name, member = d["__enum__"].split(".")
        return getattr(globals()[name], member)
    else:
        return d


class ParameterFormat(Enum):
    """
    Defines a parameter format
    """
    NONE = ""
    String = "aaaa"
    Decimal = 2
    Bytes = 3
    Float = 4
    Time = 5
