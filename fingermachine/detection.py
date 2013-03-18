import sys
from collections import defaultdict, namedtuple
import itertools

import cv2
import math

Point = namedtuple('Point', ('x', 'y'))


def get_center(contour):
    """Computes and returns the center of a contour object.

    You get back a tuple of positions (x, y).

    """
    moments = cv2.moments(contour)
    try:
        x = moments['m10'] / moments['m00']
        y = moments['m01'] / moments['m00']
    except ZeroDivisionError:
        return None
    return Point(x, y)


def get_borders(borders):
    matrix = dict()
    for p1, p2, p3 in itertools.permutations(borders, 3):
        (x1, y1), (x2, y2), (x3, y3) = p1, p2, p3

        # pythagore!
        a = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
        b = math.sqrt((x3 - x2) ** 2 + (y3 - y2) ** 2)
        c = math.sqrt((x3 - x1) ** 2 + (y3 - y1) ** 2)

        delta = (a ** 2 + b ** 2) - c ** 2
        matrix[abs(delta)] = (p1, p2, p3)
    return matrix[min(matrix.keys())]


def detect_shapes(img_path):
    """Opens an image, finds and returns markers (start, end, corners) and
    a path if one is detected.

    :param img_path: the path to the image to load.

    Returns a tuple of (markers, path).
    """
    gray = cv2.imread(img_path, 0)
    # gray = cv2.equalizeHist(gray)

    _, threshold = cv2.threshold(gray, 80, 255, cv2.THRESH_BINARY_INV)

    contours, _ = cv2.findContours(threshold, mode=cv2.RETR_EXTERNAL,
                                   method=cv2.CHAIN_APPROX_SIMPLE)

    shapes = {
        3: 'borders',  # triangles
        4: 'start',  # square
        5: 'end',  # kinda square
    }

    markers = defaultdict(list)
    path = None

    possible_paths = []

    # first iteration, get the start, end and borders.
    for cnt in contours:
        approx = cv2.approxPolyDP(cnt,
                    epsilon=0.04 * cv2.arcLength(cnt, True),
                    closed=True)

        sections = len(approx)

        if sections in shapes:
            center = get_center(cnt)
            if center is not None:
                markers[shapes[sections]].append(center)
        elif sections > max(shapes.keys()):
            possible_paths.append(cnt)

    borders = get_borders(markers['borders'])

    # let's find which points are where
    #                   TR < top right
    #
    #
    #
    # BL                BR < bottom right
    # ^ Bottom left

    matrix = {}
    for p1, p2, p3 in itertools.permutations(borders, 3):
        diff = p1.x - p2.x + p1.y, p2.y
        matrix[diff] = p1, p2, p3

    bottom_right, p1, p2 = matrix[min(matrix.keys())]


    return markers, path
    top_left = borders[0]
    bottom_left = borders[1]
    top_right = borders[2]

    for cnt in possible_paths:
        # check the path is inside the paper
        center = get_center(cnt)
        if (top_left <= center <= top_right
                and center[0] > bottom_left[0]
                and center[1] < bottom_left[1]):

            # That's probably the racing path.
            path = cnt
            print "path detected"

    return markers, path


def display_img(img):
    cv2.imshow('img', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print 'you must supply the path to your image'
        sys.exit(0)
    img_path = sys.argv[1]

    markers, path = detect_shapes(img_path)

    # eventually do something with it.
    img = cv2.imread(img_path)

    colors = {'borders': (0, 0, 255),
              'start': (0, 255, 0),
              'end': (255, 0, 0)}

    for key, values in markers.items():
        color = colors[key]
        for center in values:
            cv2.circle(img, center, 2, color, 5)

    print markers

    if path is not None:
        cv2.drawContours(img, [path], 0, (0, 255, 255), -1)

    display_img(img)
