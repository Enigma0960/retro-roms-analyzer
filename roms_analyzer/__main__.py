import os
import attr
import glob
import logging
import pprint
import argparse

from typing import Union, Optional

from roms_analyzer.platforms.snes import get_header

logging.basicConfig(level=logging.DEBUG)

_LOGGER = logging.getLogger(__name__)

HEADER_LoROM_ADDR = 0x007FC0
HEADER_HiROM_ADDR = 0x00FFC0
HEADER_ExLoROM_ADDR = 0x407FC0
HEADER_ExHiROM_ADDR = 0x40FFC0

FILE_HEADER_SIZE = 512


@attr.s()
class SnesHeader:
    cartridge_title = attr.ib(type=bytes, default=b'')
    rom_speed = attr.ib(type=bytes, default=b'')
    chipset = attr.ib(type=bytes, default=b'')
    rom_size = attr.ib(type=bytes, default=b'')
    ram_size = attr.ib(type=bytes, default=b'')
    country = attr.ib(type=bytes, default=b'')
    developer_id = attr.ib(type=bytes, default=b'')
    rom_version = attr.ib(type=bytes, default=b'')
    checksum = attr.ib(type=bytes, default=b'')
    checksum_compliment = attr.ib(type=bytes, default=b'')
    interrupt_vectors = attr.ib(type=bytes, default=b'')


def get_app_param() -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog='retro roms analyzer')
    parser.add_argument('input')
    return parser.parse_args()


def get_files(path: str, ext: Union[str, list[str]]) -> list[str]:
    res: list[str] = []
    path = os.path.abspath(path)
    if type(ext) is str:
        ext = [ext]
    for file_type in ext:
        file_path = os.path.join(path, "**", f"*.{file_type}")
        res += glob.glob(file_path, recursive=True)
    return res


def check_file_header(data: bytes) -> bool:
    s = 1024
    while s < len(data): s += 1024
    return s - len(data) == 512


def get_bytes(data: bytes, size: int = 1, offset: int = 0) -> bytes:
    return data[offset:offset + size]


def extract_bytes(data: bytes, size) -> tuple[bytes, bytes]:
    res = data[:size]
    data = data[size:]
    return data, res


# def get_header(data: bytes, start: int) -> Optional[SnesHeader]:
#     header: Optional[SnesHeader] = SnesHeader()
#
#     hdata = get_bytes(data=data, offset=start, size=53)
#
#     hdata, header.cartridge_title = extract_bytes(hdata, 21)
#     hdata, header.rom_speed = extract_bytes(hdata, 1)
#     hdata, header.chipset = extract_bytes(hdata, 1)
#     hdata, header.rom_size = extract_bytes(hdata, 1)
#     hdata, header.ram_size = extract_bytes(hdata, 1)
#     hdata, header.country = extract_bytes(hdata, 1)
#     hdata, header.developer_id = extract_bytes(hdata, 1)
#     hdata, header.rom_version = extract_bytes(hdata, 1)
#     hdata, header.checksum = extract_bytes(hdata, 2)
#     hdata, header.checksum_compliment = extract_bytes(hdata, 2)
#     _, header.interrupt_vectors = extract_bytes(hdata, 32)
#
#     return header


if __name__ == '__main__':
    args = get_app_param()
    file_list = get_files(args.input, ["smc", "sfc"])

    for file_name in file_list:
        _LOGGER.info(f'File:{file_name}')

        with open(file_name, mode='rb') as file:
            data = file.read()

        _LOGGER.info(f'File size: {len(data)}')

        if check_file_header(data):
            start = 512
        else:
            start = 0
        _LOGGER.info(f'ROM size: {len(data) - start}')

        _LOGGER.info(get_header(data[start + HEADER_LoROM_ADDR:]))

        # header_LoROM = get_header(data, start + HEADER_LoROM_ADDR)
        # header_HiROM = get_header(data, start + HEADER_HiROM_ADDR)
        # header_ExLoROM = get_header(data, start + HEADER_ExLoROM_ADDR)
        # header_ExHiROM = get_header(data, start + HEADER_ExHiROM_ADDR)
        #
        # _LOGGER.info('LoROM: ' + pprint.pformat(header_LoROM.cartridge_title))
        # _LOGGER.info('HiROM: ' + pprint.pformat(header_HiROM.cartridge_title))
        # _LOGGER.info('ExHiROM: ' + pprint.pformat(header_ExHiROM.cartridge_title))
        #
        # _LOGGER.info('LoROM checksum: ' + pprint.pformat(header_LoROM.checksum))
        # _LOGGER.info('HiROM checksum: ' + pprint.pformat(header_HiROM.checksum))
        # _LOGGER.info('ExHiROM checksum: ' + pprint.pformat(header_ExHiROM.checksum))
        #
        # _LOGGER.info('\n\n')
