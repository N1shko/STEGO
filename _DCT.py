import numpy as np
from skimage.util import view_as_blocks
from scipy.fftpack import dct, idct
from _extra import *
u1, v1 = 4, 5
u2, v2 = 5, 4
n = 8
P = 25


def double_to_byte(arr):
    return np.uint8(np.round(np.clip(arr, 0, 255), 0))


def increment_abs(x):
    if x >= 0:
        return x + 1
    else:
        return x - 1


def decrement_abs(x):
    if np.abs(x) <= 1:
        return 0
    elif x >= 0:
        return x - 1
    else:
        return x + 1


def valid_coefficients(transform, bit, threshold):
    difference = abs(transform[u1, v1]) - abs(transform[u2, v2])
    if (bit == 0) and (difference > threshold):
        return True
    elif (bit == 1) and (difference < -threshold):
        return True
    else:
        return False


def change_coefficients(transform, bit):
    coefs = transform.copy()
    if bit == 0:
        coefs[u1, v1] = increment_abs(coefs[u1, v1])
        coefs[u2, v2] = decrement_abs(coefs[u2, v2])
    elif bit == 1:
        coefs[u1, v1] = decrement_abs(coefs[u1, v1])
        coefs[u2, v2] = increment_abs(coefs[u2, v2])
    return coefs


def embed_bit(block, bit):
    patch = block.copy()
    coefs = dct(dct(patch, axis=0), axis=1)
    while not valid_coefficients(coefs, bit, P) or (bit != retrieve_bit(patch)):
        coefs = change_coefficients(coefs, bit)
        patch = double_to_byte(idct(idct(coefs, axis=0), axis=1)/(2*n)**2)
    return patch


def embed_message(orig, msg):
    changed = orig.copy()
    blue = changed[:, :, 2]
    blocks = view_as_blocks(blue, block_shape=(n, n))
    h = blocks.shape[1]
    for index, bit in enumerate(msg):
        i = index // h
        j = index % h
        block = blocks[i, j]
        blue[i * n: (i + 1) * n, j * n: (j + 1) * n] = embed_bit(block, bit)
    changed[:, :, 2] = blue
    im = Image.fromarray(changed)
    im.save("output.bmp")
    return changed


def retrieve_bit(block):
    transform = dct(dct(block, axis=0), axis=1)
    if abs(transform[u1, v1]) - abs(transform[u2, v2]) > P:
        return 0
    else:
        return 1


def retrieve_message(img, length):
    blocks = view_as_blocks(img[:, :, 2], block_shape=(n, n))
    h = blocks.shape[1]
    return [retrieve_bit(blocks[index//h, index % h]) for index in range(length)]


if __name__ == '__main__':
    original = np.array(Image.open('4k.jpg'))
    c = "al;asdfl;asdkflasd"
    a = str2bit(c)
    a = "".join(a)
    values = list(map(int, a.split(' ')))
    result = []
    for i in range(0, len(a), 1):
        result.append(int(a[i: i + 1]))
    test_message = result
    changed = embed_message(original, test_message)
    result = retrieve_message(changed, len(test_message))
    new_bin = ""
    for i in range(len(c) * 8):
        new_bin += str(result[i])
    new_bin = bits2a(new_bin)
    print(new_bin)

