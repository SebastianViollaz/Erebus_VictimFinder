import math
import cv2 as cv
import numpy as np
import os
from fixture_detection.color_filter import ColorFilter

script_dir = os.path.dirname(__file__)
image_dir = os.path.join(script_dir, "images")

def save_image(image, filename):
    cv.imwrite(os.path.join(image_dir, filename), image)


def normalizeRads(rad):
    rad %= 2 * math.pi
    if rad < 0:
        rad += 2 + math.pi
    return rad

def degsToRads(deg):
    """Converts from degrees to radians
    """
    return deg * math.pi / 180

def radsToDegs(rad):
    """ Converts from radians to degrees
    """
    return rad * 180 / math.pi

def mapVals(val, in_min, in_max, out_min, out_max):
    """Converts a number from a range of value to another
    """
    return (val - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def getCoordsFromRads(rad, distance):
    """# Gets x, y coordinates from a given angle in radians and distance
    """
    y = float(distance * math.cos(rad))
    x = float(distance * math.sin(rad))
    return (x, y)

def getCoordsFromDegs(deg, distance):
    """# Gets x, y coordinates from a given angle in degrees and distance
    """
    rad = degsToRads(deg)
    y = float(distance * math.cos(rad))
    x = float(distance * math.sin(rad))
    return (x, y)


def multiplyLists(list1, list2):
    """MUltiply a list elemnt to elemnt"""
    return [item1 * item2 for item1, item2 in zip(list1, list2)]

def sumLists(list1, list2):
    """Sum lists element to element"""
    return [item1 + item2 for item1, item2 in zip(list1, list2)]

def subtractLists(list1, list2):
    """Substract lists element to element"""
    return [item1 - item2 for item1, item2 in zip(list1, list2)]


def divideLists(list1, list2):
    """Divide lists element to element"""
    return [item1 / item2 for item1, item2 in zip(list1, list2)]


def draw_grid(image, square_size, offset = [0,0], color=255):
    for y, row in enumerate(image):
        for x, pixel in enumerate(row):
            if (y + offset[1]) % square_size == 0 or (x + offset[0]) % square_size == 0:
                if len(image.shape) == 3:
                    image[y][x][:] = color
                else:
                    image[y][x] = color

def draw_poses(image, poses, color=255, back_image=None, xx_yy_format=False):
    if xx_yy_format:
        if back_image is not None:
            in_bounds_x = (poses[0] < min(image.shape[0], back_image.shape[0]) - 1) & (poses[0] > 0)
            in_bounds_y = (poses[1] < min(image.shape[1], back_image.shape[1]) - 1) & (poses[1] > 0)
        else:
            in_bounds_x = (poses[0] < image.shape[0] - 1) & (poses[0] > 0)
            in_bounds_y = (poses[1] < image.shape[1] - 1) & (poses[1] > 0)
        
        poses = (poses[0][in_bounds_x & in_bounds_y], poses[1][in_bounds_x & in_bounds_y])

        if back_image is None:
            image[poses[1], poses[0], :] = color
        else:
            image[poses[1], poses[0], :] = back_image[poses[1], poses[0], :]
        
    else:
        in_bounds = (poses[:, 0] >= 0) & (poses[:, 0] < image.shape[1]) & (poses[:, 1] >= 0) & (poses[:, 1] < image.shape[0])
        poses = poses[in_bounds]

        if back_image is None:
            image[poses[:, 1], poses[:, 0], :] = color
        else:
            image[poses[:, 1], poses[:, 0], :] = back_image[poses[:, 1], poses[:, 0], :]
            

def draw_squares_where_not_zero(image, square_size, offsets, color=(255, 255, 255)):
    ref_image = image.copy()
    for y in range(image.shape[0] // square_size):
        for x in range(image.shape[1] // square_size):
            square_points = [
                (y * square_size)        + (square_size - offsets[1]),
                ((y + 1) * square_size)  + (square_size - offsets[1]), 
                (x * square_size)        + (square_size - offsets[0]),
                ((x + 1) * square_size)  + (square_size - offsets[0])]
            square = ref_image[square_points[0]:square_points[1], square_points[2]:square_points[3]]
            non_zero_count = np.count_nonzero(square)
            if non_zero_count > 0:
                #print("Non zero count: ", non_zero_count)
                #print("max: ", np.max(square))
                cv.rectangle(image, (square_points[2], square_points[0]), (square_points[3], square_points[1]), color, 3)

def get_squares(image, square_size, offsets):
    grid = []
    for y in range(image.shape[0] // square_size):
        row = []
        for x in range(image.shape[1] // square_size):
            square_points = [
                (y * square_size)        + (square_size - offsets[1]),
                ((y + 1) * square_size)  + (square_size - offsets[1]), 
                (x * square_size)        + (square_size - offsets[0]),
                ((x + 1) * square_size)  + (square_size - offsets[0])]
            row.append(square_points)
        grid.append(row)
    return grid

def resize_image_to_fixed_size(image, size):
    """Recice an image depending of a specif size (heigth,width)"""
    height, width = image.shape[:2]

    if width > size[1] or height > size[0]:
        ratio = min(size[1] / width, size[0] / height)
        new_width = round(width * ratio)
        new_height = round(height * ratio)
        final_image = cv.resize(image, (new_width, new_height), interpolation=cv.INTER_NEAREST)
    else:
        final_image = image

    return final_image


def divide_into_chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


class ColorFilterTuner:
    def __init__(self, color_filter: ColorFilter, activate=False) -> None:
        self.filter_for_tuning = color_filter

        self.activate = activate

        if self.activate:
            cv.namedWindow("filter_tuner")

            cv.createTrackbar("min_h", "filter_tuner", self.filter_for_tuning.lower[0], 255, lambda x: None)
            cv.createTrackbar("max_h", "filter_tuner", self.filter_for_tuning.upper[0], 255, lambda x: None)

            cv.createTrackbar("min_s", "filter_tuner", self.filter_for_tuning.lower[1], 255, lambda x: None)
            cv.createTrackbar("max_s", "filter_tuner", self.filter_for_tuning.upper[1], 255, lambda x: None)

            cv.createTrackbar("min_v", "filter_tuner", self.filter_for_tuning.lower[2], 255, lambda x: None)
            cv.createTrackbar("max_v", "filter_tuner", self.filter_for_tuning.upper[2], 255, lambda x: None)

    def tune(self, image):
        if self.activate and image is not None:
            min_h = cv.getTrackbarPos("min_h", "filter_tuner")
            max_h = cv.getTrackbarPos("max_h", "filter_tuner")
            min_s = cv.getTrackbarPos("min_s", "filter_tuner")
            max_s = cv.getTrackbarPos("max_s", "filter_tuner")
            min_v = cv.getTrackbarPos("min_v", "filter_tuner")
            max_v = cv.getTrackbarPos("max_v", "filter_tuner")
            self.filter_for_tuning = ColorFilter((min_h, min_s, min_v), (max_h, max_s, max_v))
            print(tuple(self.filter_for_tuning.lower), tuple(self.filter_for_tuning.upper))
            cv.imshow("filter_tuner", self.filter_for_tuning.filter(image))