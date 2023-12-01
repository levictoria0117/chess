from enum import Enum

# Function to convert a string into an enum member
def string_to_enum(string_value: str, enum_class: Enum) -> Enum:
    try:
        return enum_class(string_value)
    except ValueError:
        raise ValueError(f"{string_value} is not a valid value for {enum_class.__name__}")