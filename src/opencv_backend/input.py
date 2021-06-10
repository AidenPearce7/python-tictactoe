"""Collects functions to get input from camera"""
from time import perf_counter
import cv2 as cv
import numpy as np


class InputSystem:
    """Inits and processes input from camera"""

    def __init__(self, camera):
        self.camera = camera
        self.tracker = None
        self.rois = None
        # self.average_skin_color = None

    # def __sample_hand_color(self):
    #     """Samples color of the hand"""
    #     self._create_rois_for_sampling()
    #     means = list()
    #     while True:
    #         ok, frame = self.camera.read()
    #         self._draw_squares(frame)
    #         cv.imshow("Sampling", frame)
    #         if cv.waitKey(1) != -1:
    #             frame = cv.cvtColor(frame, cv.COLOR_BGR2HLS)
    #             for coord_set in self.rois:
    #                 means.append(
    #                     cv.mean(
    #                         frame[
    #                             coord_set[0][0] : coord_set[1][0],
    #                             coord_set[0][1] : coord_set[1][1],
    #                         ]
    #                     )
    #                 )
    #             break
    #     self.average_skin_color = np.array(means).mean(axis=0)
    #     cv.destroyWindow("Sampling")

    def _create_rois_for_sampling(self):
        """Returns a collection of preset ROIS\n
        Might be needed to automate this so it's not stuck to the one spot
         regardless of resolution."""
        self.rois = [
            ((400, 120), (410, 130)),
            ((440, 120), (450, 130)),
            ((400, 160), (410, 170)),
            ((400, 200), (410, 210)),
            ((440, 160), (450, 170)),
            ((440, 200), (450, 210)),
        ]

    def _draw_squares(self, frame, color=(0, 255, 0), thickness=2):
        for coord_set in self.rois:
            frame = cv.rectangle(frame, coord_set[0], coord_set[1], color, thickness)

    def setup_tracker(self):
        """Setup KCF tracker using preset tracking spot"""
        roi = ((400, 100), (500, 250))
        self.tracker = cv.TrackerKCF_create()
        while True:
            ok, frame = self.camera.read()
            frame = cv.flip(frame, 1)
            cv.rectangle(frame, roi[0], roi[1], (0, 255, 0), 2)
            cv.putText(
                frame,
                "Put your hand in the box",
                (50, 50),
                cv.FONT_HERSHEY_SIMPLEX,
                1,
                (255, 0, 0),
                2,
            )
            cv.putText(
                frame,
                "Press any key to continue",
                (50, 300),
                cv.FONT_HERSHEY_SIMPLEX,
                1,
                (255, 0, 0),
                2,
            )
            # ROI = frame[roi[0][1] : roi[1][1], roi[0][0] : roi[1][0]]

            cv.imshow("Input", frame)
            if cv.waitKey(1) != -1:
                self.tracker.init(
                    frame,
                    (
                        roi[0][0],
                        roi[0][1],
                        roi[1][0] - roi[0][0],
                        roi[1][1] - roi[0][1],
                    ),
                )
                break

    # def __setup_tracker(self):
    #     """Setup KCF tracker using selectROI function"""

    #     read_frame, frame = self.camera.read()
    #     while not read_frame:
    #         read_frame, frame = self.camera.read()

    #     bbox = cv.selectROI(frame, False)
    #     self.tracker = cv.TrackerKCF_create()
    #     self.tracker.init(frame, bbox)

    def check_bounds(self, interface):
        """Tracks and checks the objects current location\n
        if object stays in the same place for 5 seconds returns that place"""
        separators = interface.get_separators()
        start = perf_counter()
        cache = (0, 0)
        while True:
            frame_read, frame = self.camera.read()
            if not frame_read:
                continue
            frame = cv.flip(frame, 1)
            notlost, bbox = self.tracker.update(frame)
            if notlost:
                lost_start = 0
                cv.rectangle(
                    frame,
                    (bbox[0], bbox[1]),
                    (bbox[0] + bbox[2], bbox[1] + bbox[3]),
                    (0, 0, 255),
                    2,
                )
                frame = interface.overlay(frame)
                cv.imshow("Input", frame)
                loc = (
                    self._check_x(separators["x"], bbox),
                    self._check_y(separators["y"], bbox),
                )

                cv.waitKey(1)
                if not (isinstance(loc[0], int) and isinstance(loc[1], int)):
                    continue
                if loc != cache:
                    cache = loc
                    start = perf_counter()
                else:
                    if perf_counter() - start > 5:
                        return cache
            else:
                cv.putText(
                    frame,
                    "Hand lost reseting tracker in 5 seconds",
                    (50, 50),
                    cv.FONT_HERSHEY_SIMPLEX,
                    1,
                    (255, 0, 0),
                    2,
                )
                cv.imshow("Input", frame)
                cv.waitKey(1)
                if lost_start != 0:
                    lost_start = perf_counter()
                elif perf_counter() - lost_start > 5:
                    self.setup_tracker()

    def _check_x(self, separator_x, bbox):
        """Returns the x space on the grid that tracked object is located at"""
        if bbox[0] + bbox[2] < separator_x[1]:
            return 0
        if bbox[0] > separator_x[2]:
            return 2
        if bbox[0] > separator_x[1] and bbox[0] + bbox[2] < separator_x[2]:
            return 1
        return "n/a"

    def _check_y(self, separator_y, bbox):
        """Returns the y space on the grid that tracked object is located at"""
        if bbox[1] + bbox[3] < separator_y[1]:
            return 0
        if bbox[1] > separator_y[2]:
            return 2
        if bbox[1] > separator_y[1] and bbox[1] + bbox[3] < separator_y[2]:
            return 1
        return "n/a"
