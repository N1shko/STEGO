from PIL import Image
from _extra import str2bit, setlsb


def lsb_hide(file_input_name, file_output_name, message: str):
    img = Image.open(file_input_name).convert("RGB")
    message_length = len(message)
    assert message_length != 0, "message length is zero"
    encoded = img.copy()
    width, height = img.size
    i = 0
    message = str(message_length) + "#" + str(message)  # преобразование исходного сообщения в битовое представление
    message_bits = "".join(str2bit(message))
    message_bits += "0" * ((3 - (len(message_bits) % 3)) % 3)  # добавление незначащих нулей
    print(message_bits)
    npixels = width * height
    len_message_bits = len(message_bits)
    if len_message_bits > npixels * 3:  # проверка на допустимость длины сообщения по отношению к размеру изображения
        raise Exception(
            "The message size is too big for that image: {}".format(message_length)
        )
    for row in range(height):
        for col in range(width):
            if i + 3 <= len_message_bits:
                pixel = img.getpixel((col, row))
                r = pixel[0]
                g = pixel[1]
                b = pixel[2]
                r = setlsb(r, message_bits[i])
                g = setlsb(g, message_bits[i + 1])
                b = setlsb(b, message_bits[i + 2])
                encoded.putpixel((col, row), (r, g, b))
                i += 3
            else:
                img.close()
                encoded.save(file_output_name)
                return encoded


def lsb_reveal(input_image_file):
    img = Image.open(input_image_file).convert("RGB")
    width, height = img.size
    buff, count = 0, 0
    bitab = []
    limit = None
    for row in range(height):
        for col in range(width):
            pixel = img.getpixel((col, row))
            for color in pixel:
                buff += (color & 1) << (8 - 1 - count)
                count += 1
                if count == 8:
                    bitab.append(chr(buff))
                    buff, count = 0, 0
                    if bitab[-1] == "#" and limit is None:
                        try:
                            limit = int("".join(bitab[:-1]))
                        except Exception:
                            pass

            if len(bitab) - len(str(limit)) - 1 == limit:
                img.close()
                return "".join(bitab)[len(str(limit)) + 1:]


if __name__ == "__main__":
    secret_message = "ABC_DEF"
    encrypt1 = lsb_hide("test12.bmp", "999.bmp", secret_message)
    print(lsb_reveal("999.bmp"))