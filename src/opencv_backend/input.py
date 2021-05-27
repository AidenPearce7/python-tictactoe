"""Collects functions to get input from camera"""
from time import perf_counter
import cv2 as cv


def setup_tracker(camera):
    """Setup KCF tracker using selectROI function"""
    read_frame, frame = camera.read()
    while not read_frame:
        read_frame, frame = camera.read()

    bbox = cv.selectROI(frame, False)
    tracker = cv.TrackerKCF_create()
    tracker.init(frame, bbox)
    return tracker


# def eliminate_background(frame):
#    bgModel = cv.createBackgroundSubtractorMOG2(0, 50)


def check_bounds(camera, tracker, interface):
    """Tracks and checks the objects current location\n
    if object stays in the same place for 5 seconds returns that place"""
    separators = interface.get_separators()
    start = perf_counter()
    cache = (0, 0)
    while True:
        frame_read, frame = camera.read()
        if not frame_read:
            continue
        notlost, bbox = tracker.update(frame)
        if notlost:
            loc = (check_x(separators["x"], bbox), check_y(separators["y"], bbox))
            if loc != cache:
                cache = loc
                start = perf_counter()
            else:
                if perf_counter() - start > 5:
                    return cache


def check_x(separator_x, bbox):
    """Returns the x space on the grid that tracked object is located at"""
    if bbox[0] + bbox[2] < separator_x[1]:
        return 0
    if bbox[0] > separator_x[2]:
        return 2
    return 1


def check_y(separator_y, bbox):
    """Returns the y space on the grid that tracked object is located at"""
    if bbox[1] + bbox[3] < separator_y[1]:
        return 0
    if bbox[0] > separator_y[3]:
        return 2
    return 1
