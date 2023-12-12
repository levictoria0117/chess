from enum import Enum
from typing import Type, TypeVar

EnumType = TypeVar('EnumType', bound=Enum)

# Function to convert a string into an enum member
def string_to_enum(string_value: str, enum_class: Type[EnumType]) -> EnumType:
    try:
        return enum_class(string_value)
    except ValueError:
        raise ValueError(f"{string_value} is not a valid value for {enum_class}")