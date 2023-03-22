from PIL import Image
import piexif


def meta_hide(
    file_input_name,
    file_output_name,
    secret_message=None,
    img_format=None,
):
    from zlib import compress
    from base64 import b64encode

    try:
        text = compress(b64encode(bytes(secret_message, "utf-8")))
        # print(b64encode(bytes(secret_message, "utf-8")))
        # print(text)
    except Exception:
        text = compress(b64encode(secret_message))

    img = Image.open(file_input_name)
    if img_format is None:
        img_format = img.format

    if "exif" in img.info:
        exif_dict = piexif.load(img.info["exif"])
    else:
        exif_dict = {}
        exif_dict["0th"] = {}
    exif_dict["0th"][piexif.ImageIFD.ImageDescription] = text
    exif_bytes = piexif.dump(exif_dict)
    img.save(file_output_name, format=img_format, exif=exif_bytes)
    img.close()
    return img


def meta_reveal(input_image_file):
    from base64 import b64decode
    from zlib import decompress

    img = Image.open(input_image_file)

    try:
        if img.format in "JPEG":
            if "exif" in img.info:
                exif_dict = piexif.load(img.info.get("exif", b""))
                description_key = piexif.ImageIFD.ImageDescription
                encoded_message = exif_dict["0th"][description_key]
            else:
                encoded_message = b""
        else:
            raise ValueError("Given file is not JPEG")
    finally:
        img.close()
    # print(encoded_message)
    return b64decode(decompress(encoded_message)).decode("utf-8")


if __name__ == "__main__":
    secret_message = "AMG 4MATIC"
    encrypt = meta_hide("test1.jpg", "test123.jpg", secret_message)
    print(meta_reveal("test123.jpg"))