"""Collection of functions used for UI"""
import cv2 as cv


def draw_grid(frame):
    """Draws a 3 by 3 grid on the frame"""
    height, width = frame.shape
    for i in range(1, 3):
        startpoint_height = (0, i * height // 3)
        startpoint_width = (i * width // 3, 0)
        endpoint_height = (width, i * height // 3)
        endpoint_width = (i * width // 3, height)
        thickness = 3
        color = (255, 0, 0)
        frame = cv.line(frame, startpoint_height, endpoint_height, color, thickness)
        frame = cv.line(frame, startpoint_width, endpoint_width, color, thickness)


def draw_x(frame, grid_location, color=(0, 0, 255), thickness=7):
    """Draws X on the selected grid marker.\n
    location should be a tuple with two numbers indicating place on the grid"""
    height, width = frame.shape
    width_offset = width // 3 * 0.25
    height_offset = height // 3 * 0.25

    left = int(grid_location[0] * width // 3 + width_offset)
    up = int(grid_location[1] * height // 3 + height_offset)
    right = int((grid_location[0] + 1) * width // 3 - width_offset)
    down = int((grid_location[1] + 1) * height // 3 - height_offset)
    frame = cv.line(frame, (left, up), (right, down), color, thickness)
    frame = cv.line(frame, (left, down), (right, up), color, thickness)


def draw_circle(frame, grid_location, color=(0, 0, 255), thickness=7):
    """Draws circle on the selected grid marker.\n
    location should be a tuple with two numbers indicating place on the grid"""
    height, width = frame.shape
    width_offset = width // 3 * 0.5
    height_offset = height // 3 * 0.5
    center = (
        int(grid_location[0] * width // 3 + width_offset),
        int(grid_location[1] * height // 3 + height_offset),
    )
    radius = int(height_offset * 0.75)
    cv.circle(frame, center, radius, color, thickness)


