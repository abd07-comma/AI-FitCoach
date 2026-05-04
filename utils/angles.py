import numpy as np


def calculate_angle(a, b, c):
    """
    Calculate the angle between three body points.
    a, b, c — lists of [x, y] coordinates
    b — the central point (joint)
    Returns angle in degrees (0-180)
    """
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)

    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - \
              np.arctan2(a[1] - b[1], a[0] - b[0])

    angle = np.abs(radians * 180.0 / np.pi)

    if angle > 180.0:
        angle = 360 - angle

    return angle


def get_coords(landmarks, point):
    """
    Extract [x, y] coordinates for a given body landmark.
    """
    return [
        landmarks[point.value].x,
        landmarks[point.value].y
    ]