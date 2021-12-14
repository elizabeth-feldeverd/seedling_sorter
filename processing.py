# from PIL import Image
import numpy as np
from numpy import asarray


def split(image):
    # Convert image to nparray
    X = asarray(image)
    # Get image dimensions
    height = X.shape[0]
    width = X.shape[1]
    # Pad image with white so its dimensions are multiples of 32. Assumes an RGB image
    pad_height = int(np.ceil(height / 32)) * 32
    pad_width = int(np.ceil(width / 32)) * 32
    pad = np.ones((pad_height, pad_width, 3), dtype=np.uint8) * 255
    pad[:height, :width, :] = X
    # Create an array of 32 x 32 images
    img_array = np.zeros(
        (int(pad_height / 32) * int(pad_width / 32), 32, 32, 3),
        dtype=np.uint8)
    for h in range(int(pad_height / 32)):
        for w in range(int(pad_width / 32)):
            img_array[h * int(pad_width / 32) +
                      w, :, :, :] = pad[h * 32:(h + 1) * 32,
                                        w * 32:(w + 1) * 32, :]
    return img_array


def stitch(array, pad_height, pad_width):
    # Create an array of 255 that is the same size as the padded image
    new_img_array = np.ones((pad_height, pad_width, 3), dtype=np.uint8) * 255
    width_div_32 = int(pad_width / 32)
    for h in range(int(pad_height / 32)):
        for w in range(int(pad_width / 32)):
            new_img_array[h * 32:(h + 1) * 32,
                          w * 32:(w + 1) * 32, :] = array[h * width_div_32 + w]
    return new_img_array
