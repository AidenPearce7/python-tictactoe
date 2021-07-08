"""UI class"""
import cv2 as cv
import numpy as np


class UI:
    """Handles UI drawing and managing"""

    def __init__(self, frame):
        height, width, channels = frame.shape
        self.width = width
        self.height = height
        self.separators = {
            "y": (0, height // 3, 2 * height // 3),
            "x": (0, width // 3, 2 * width // 3),
        }
        self.figure = np.zeros((height, width, channels), dtype=np.uint8)
        self.grid_drawn = False

    def draw_grid(self, color=(255, 0, 0), thickness=9):
        """Draws a 3 by 3 grid on the frame"""
        if not self.grid_drawn:
            for i in range(1, 3):
                startpoint_height = (0, self.separators["y"][i])
                startpoint_width = (self.separators["x"][i], 0)
                endpoint_height = (self.width, self.separators["y"][i])
                endpoint_width = (self.separators["x"][i], self.height)
                self.figure = cv.line(
                    self.figure, startpoint_height, endpoint_height, color, thickness
                )
                self.figure = cv.line(
                    self.figure, startpoint_width, endpoint_width, color, thickness
                )
            self.grid_drawn = True

    def _draw_x(self, x, y, color, thickness):
        """Draws X on the selected grid marker.\n
        location should be a tuple with two numbers indicating place on the grid"""
        width_offset = self.separators["x"][1] * 0.25
        height_offset = self.separators["y"][1] * 0.25

        left = int(self.separators["x"][x] + width_offset)
        up = int(self.separators["y"][y] + height_offset)
        right = int(self.separators["x"][x] + width_offset * 3)
        down = int(self.separators["y"][y] + height_offset * 3)
        self.figure = cv.line(self.figure, (left, up), (right, down), color, thickness)
        self.figure = cv.line(self.figure, (left, down), (right, up), color, thickness)

    def _draw_circle(self, x, y, color, thickness):
        """Draws circle on the selected grid marker.\n
        location should be a tuple with two numbers indicating place on the grid"""
        width_offset = self.separators["x"][1] * 0.5
        height_offset = self.separators["y"][1] * 0.5
        center = (
            int(self.separators["x"][x] + width_offset),
            int(self.separators["y"][y] + height_offset),
        )
        radius = int(height_offset * 0.75)
        self.figure = cv.circle(self.figure, center, radius, color, thickness)

    def draw_move(self, coords, color=(0, 0, 255), thickness=7):
        """Draws a shape based on the coordinate object"""
        if coords.symbol == "x":
            self._draw_x(coords.x, coords.y, color, thickness)
        else:
            self._draw_circle(coords.x, coords.y, color, thickness)

    def get_separators(self):
        """Returns the separators used for the processing"""
        return self.separators

    def overlay(self, frame):
        """Returns the frame with added figure array"""
        return cv.add(frame, self.figure)
