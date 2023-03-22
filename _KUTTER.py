from random import randint
from PIL import Image
from _extra import str2bit, bits2a


def kut_hide(file_input_name, file_output_name, message, r, lam):
    img = Image.open(file_input_name).convert("RGB")
    message_length = len(message)
    encoded = img.copy()
    width, height = img.size
    message_bits = (str2bit(message))
    n, m, w = message_length, 8, r
    x_coord = [[[randint(4, width - 5) for k in range(m)] for j in range(n)]for i in range(w)]
    y_coord = [[[randint(4, height - 5) for k in range(m)] for j in range(n)] for i in range(w)]
    for i in range(n):
        for j in range(m):
            for k in range(w):
                pixel = img.getpixel((x_coord[k][i][j], y_coord[k][i][j]))
                r = pixel[0]
                g = pixel[1]
                b = pixel[2]
                y = round(0.298 * r + 0.586 * g + 0.114 * b)
                if y == 0:
                    y = 5/lam
                if int(message_bits[i][j]) == 1:
                    if b + lam * y > 255:
                        encoded.putpixel((x_coord[k][i][j], y_coord[k][i][j]), (r, g, 255))
                    else:
                        encoded.putpixel((x_coord[k][i][j], y_coord[k][i][j]), (r, g, b + round(lam * y)))
                else:
                    if b + lam * y < 0:
                        encoded.putpixel((x_coord[k][i][j], y_coord[k][i][j]), (r, g, 0))
                    else:
                        encoded.putpixel((x_coord[k][i][j], y_coord[k][i][j]), (r, g, b - round(lam * y)))
    img.close()
    encoded.save(file_output_name)
    return [x_coord, y_coord, message_length]


def kut_reveal(file_name, x_coord, y_coord, message_length, r):
    img = Image.open(file_name)
    new_bin = [[0] * 8 for i in range(message_length)]
    sigma = 3
    n, m, w = message_length, 8, r
    for i in range(n):
        for j in range(m):
            count = 0
            for k in range(w):
                pixel = img.getpixel((x_coord[k][i][j], y_coord[k][i][j]))
                sum_b = 0
                for t in range(1, sigma+1):
                    sum_b += (img.getpixel((x_coord[k][i][j] + t, y_coord[k][i][j])))[2]
                    sum_b += (img.getpixel((x_coord[k][i][j] - t, y_coord[k][i][j])))[2]
                    sum_b += (img.getpixel((x_coord[k][i][j], y_coord[k][i][j] + t)))[2]
                    sum_b += (img.getpixel((x_coord[k][i][j], y_coord[k][i][j] - t)))[2]
                sum_b = sum_b/(4 * sigma)
                dew = pixel[2] - sum_b
                if dew == 0 and sum_b == 255:
                    dew = 0.5
                if dew == 0 and sum_b == 0:
                    dew = -0.5
                if dew > 0:
                    count += 1
            new_bin[i][j] = round(count / r)
    result = ''
    for i in range(message_length):
        result += "".join(map(str, new_bin[i]))
    result = bits2a(result)
    return result


if __name__ == "__main__":
    r = 60
    lam = 100
    secret_message = "secret message"
    temp = kut_hide("4k.jpg", "tes.jpg", secret_message, r, lam)
    print(kut_reveal("tes.jpg", temp[0], temp[1], temp[2], r))
