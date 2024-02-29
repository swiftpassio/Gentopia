from typing import Any
from typing import ClassVar
from typing import Dict
from typing import Type
from typing import TypeVar
from marshmallow import EXCLUDE
from marshmallow import Schema
from marshmallow_dataclass import dataclass

T = TypeVar("T", bound="Base")


@dataclass
class ClassWithSchema:
    Schema: ClassVar[Type[Schema]] = Schema
    ID_FIELDS = []

    def dumps(self, **kwargs) -> str:
        return self.Schema().dumps(self, **kwargs)

    def dump(self, **kwargs) -> Dict[str, Any]:
        return self.Schema().dump(self, **kwargs)

    @classmethod
    def load(cls, d: Dict[str, Any], **kwargs) -> T:
        return cls.Schema().load(d, **kwargs)

    @classmethod
    def loads(cls, string: str, **kwargs) -> T:
        return cls.Schema().loads(string, **kwargs)

    class Meta:
        unknown = EXCLUDE

    def __post_init__(self):
        for field in self.ID_FIELDS:
            original_value = getattr(self, field)
            str_value = str(original_value) if original_value else None
            setattr(self, f"{field}_str", str_value)
