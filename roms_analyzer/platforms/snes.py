import attr

from typing import Optional

from roms_analyzer.utils import extract, attr_to_string_converter, attr_to_int_converter

SNES_HEADER_SIZE = 64


@attr.s(init=False)
class SnesRomHeader:
    cartridge_title = attr.ib(type=str, on_setattr=attr_to_string_converter)
    rom_speed = attr.ib(type=int, on_setattr=attr_to_int_converter)
    chipset = attr.ib(type=int, on_setattr=attr_to_int_converter)
    rom_size = attr.ib(type=int, on_setattr=attr_to_int_converter)
    ram_size = attr.ib(type=int, on_setattr=attr_to_int_converter)
    country = attr.ib(type=int, on_setattr=attr_to_int_converter)
    developer_id = attr.ib(type=int, on_setattr=attr_to_int_converter)
    rom_version = attr.ib(type=int, on_setattr=attr_to_int_converter)
    checksum = attr.ib(type=bytes)
    interrupts = attr.ib(type=bytes)


def get_header(data: bytes) -> Optional[SnesRomHeader]:
    if len(data) < SNES_HEADER_SIZE:
        return None

    header: SnesRomHeader = SnesRomHeader()

    data = data[: SNES_HEADER_SIZE]

    header.cartridge_title, data = extract(data, 21)
    header.rom_speed, data = extract(data, 1)
    header.chipset, data = extract(data, 1)
    header.rom_size, data = extract(data, 1)
    header.ram_size, data = extract(data, 1)
    header.country, data = extract(data, 1)
    header.developer_id, data = extract(data, 1)
    header.rom_version, data = extract(data, 1)
    header.checksum, data = extract(data, 4)
    header.interrupts, data = extract(data, 32)

    return header
