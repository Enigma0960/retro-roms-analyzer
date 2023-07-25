import os
import glob
import logging
import pprint
import argparse

logging.basicConfig(level=logging.DEBUG)

_LOGGER = logging.getLogger(__name__)

HEADER_LoROM_ADDR = 0x007FC0
HEADER_HiROM_ADDR = 0x00FFC0
HEADER_ExLoROM_ADDR = 0x407FC0
HEADER_ExHiROM_ADDR = 0x40FFC0

FILE_HEADER_SIZE = 512


def get_app_param() -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog='retro roms analyzer')
    parser.add_argument('input')
    return parser.parse_args()


def get_files(path: str) -> list[str]:
    path = os.path.abspath(path)
    res = glob.glob(path)
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


def get_header(data: bytes, start: int) -> dict:
    if len(data) < 1024512:
        return {}

    hdata = get_bytes(data=data, offset=start, size=53)

    hdata, cartridge_title = extract_bytes(hdata, 21)
    hdata, rom_speed = extract_bytes(hdata, 1)
    hdata, chipset = extract_bytes(hdata, 1)
    hdata, rom_size = extract_bytes(hdata, 1)
    hdata, ram_size = extract_bytes(hdata, 1)
    hdata, country = extract_bytes(hdata, 1)
    hdata, developer_id = extract_bytes(hdata, 1)
    hdata, rom_version = extract_bytes(hdata, 1)
    hdata, checksum = extract_bytes(hdata, 2)
    hdata, checksum_compliment = extract_bytes(hdata, 2)
    _, interrupt_vectors = extract_bytes(hdata, 32)

    return {
        'cartridge_title': cartridge_title,
        'rom_speed': rom_speed,
        'chipset': chipset,
        'rom_size': rom_size,
        'ram_size': ram_size,
        'country': country,
        'developer_id': developer_id,
        'rom_version': rom_version,
        'checksum': checksum,
        'checksum_compliment': checksum_compliment,
        'interrupt_vectors': interrupt_vectors,
    }


if __name__ == '__main__':
    args = get_app_param()
    file_list = get_files(args.input)

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

        header_LoROM = get_header(data, start + HEADER_LoROM_ADDR)
        header_HiROM = get_header(data, start + HEADER_HiROM_ADDR)
        header_ExLoROM = get_header(data, start + HEADER_ExLoROM_ADDR)
        header_ExHiROM = get_header(data, start + HEADER_ExHiROM_ADDR)

        _LOGGER.info('LoROM: ' + pprint.pformat(header_LoROM['cartridge_title']))
        _LOGGER.info('HiROM: ' + pprint.pformat(header_HiROM['cartridge_title']))
        _LOGGER.info('ExHiROM: ' + pprint.pformat(header_ExHiROM['cartridge_title']))

        _LOGGER.info('LoROM checksum: ' + pprint.pformat(header_LoROM['checksum']))
        _LOGGER.info('HiROM checksum: ' + pprint.pformat(header_HiROM['checksum']))
        _LOGGER.info('ExHiROM checksum: ' + pprint.pformat(header_ExHiROM['checksum']))

        _LOGGER.info('\n\n')
