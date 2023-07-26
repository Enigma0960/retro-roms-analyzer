from typing import Optional, Any, Union, Dict


def extract(data: bytes, size: int = 1, offset: int = 0) -> Union[bytes, bytes]:
    if len(data) < offset + size:
        raise ValueError(f'Data size ({len(data)}) is smaller then necessary ({offset + size})')
    first = data[offset:size]
    last = data[offset + size:]
    return first, last


def attr_to_string_converter(instance: Any, attrib: Any, new_value: Optional[bytes]) -> Optional[str]:
    if new_value is None:
        return None
    try:
        return new_value.decode(encoding="ascii")
    except UnicodeDecodeError:
        return None


def attr_to_int_converter(instance: Any, attrib: Any, new_value: Optional[bytes]) -> Optional[int]:
    if new_value is None:
        return None

    return int.from_bytes(new_value, byteorder="little")
