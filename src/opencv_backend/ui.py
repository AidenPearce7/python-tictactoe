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
        self.figure = np.zeros((width, height, channels))
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

    def draw_x(self, grid_location, color=(0, 0, 255), thickness=7):
        """Draws X on the selected grid marker.\n
        location should be a tuple with two numbers indicating place on the grid"""
        width_offset = self.separators["x"][1] * 0.25
        height_offset = self.separators["y"][1] * 0.25

        left = int(self.separators["x"][grid_location[0]] + width_offset)
        up = int(self.separators["y"][grid_location[1]] + height_offset)
        right = int(self.separators["x"][grid_location[0]] + width_offset * 3)
        down = int(self.separators["y"][grid_location[1]] + height_offset * 3)
        self.figure = cv.line(self.figure, (left, up), (right, down), color, thickness)
        self.figure = cv.line(self.figure, (left, down), (right, up), color, thickness)

    def draw_circle(self, grid_location, color=(0, 0, 255), thickness=7):
        """Draws circle on the selected grid marker.\n
        location should be a tuple with two numbers indicating place on the grid"""
        width_offset = self.separators["x"][1] * 0.5
        height_offset = self.separators["y"][1] * 0.5
        center = (
            int(self.separators["x"][grid_location[0]] + width_offset),
            int(self.separators["y"][grid_location[1]] + height_offset),
        )
        radius = int(height_offset * 0.75)
        self.figure = cv.circle(self.figure, center, radius, color, thickness)

    def get_separators(self):
        """Returns the separators used for the processing"""
        return self.separators
