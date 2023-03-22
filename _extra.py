from typing import IO, Union
from PIL import Image


def open_img(file_name: Union[str, IO[bytes]]):
    if isinstance(file_name, Image.Image):
        return file_name
    return Image.open(file_name)


def str2bit(c: str):
    return [bin(ord(x))[2:].rjust(8, "0") for x in c]


def setlsb(component: int, bit: str):
    """Set Least Significant Bit of a colour component."""
    return component & ~1 | int(bit)


def bits2a(b):
    return ''.join(chr(int(''.join(x), 2)) for x in zip(*[iter(b)] * 8))

