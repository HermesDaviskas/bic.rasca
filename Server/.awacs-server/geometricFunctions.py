"""
Module: geometricCalculations
File: geometricCalculations.py

This module provides functions for calculating distance and angle between points in a two-dimensional space.

Dependencies:
- math: Standard Python library for mathematical operations.
"""

import math


def calculate_angle(myCoordinates, othersCoordinates, myHeading):
    """
    Calculate the angle between two points in a two-dimensional space relative to
    the heading of the observer.

    Args:
        myCoordinates (tuple): Tuple containing the (x, y) coordinates of the observer.
        othersCoordinates (tuple): Tuple containing the (x, y) coordinates of the target point.
        myHeading (float): Heading of the observer in degrees, where 0 degrees is the positive x-axis.

    Returns:
        float: The angle between the line connecting the two points and the horizontal axis,
               adjusted for the observer's heading. The angle is in the range [0, 360) degrees.
    """
    X1, Y1 = myCoordinates
    X2, Y2 = othersCoordinates

    # Calculate the angle between the two points relative to the horizontal axis
    angleBetweenUs = calculate_heading(myCoordinates, othersCoordinates)

    # Calculate the relative angle between the line and the observer's heading
    relative_angle = round(angleBetweenUs - myHeading)

    # Normalize the angle to the range [0, 360)
    relative_angle = (360 + relative_angle) % 360

    return relative_angle


def calculate_distance(coordinates_1, coordinates_2):
    """
    Calculate the Euclidean distance between two points in a two-dimensional space.

    Args:
        coordinates_1 (tuple): Tuple containing the (x, y) coordinates of the first point.
        coordinates_2 (tuple): Tuple containing the (x, y) coordinates of the second point.

    Returns:
        float: The Euclidean distance between the two points, rounded to 1 decimal place.
    """
    X1, Y1 = coordinates_1
    X2, Y2 = coordinates_2

    # Calculate the Euclidean distance using the distance formula
    return round(math.sqrt((X2 - X1)**2 + (Y2 - Y1)**2), 1)


def calculate_heading(coordinates_1, coordinates_2):
    """
    Calculate the heading from one point to another in a two-dimensional space.

    Args:
        coordinates_1 (tuple): Tuple (Xstart, Ystart) representing the starting coordinates.
        coordinates_2 (tuple): Tuple (Xend, Yend) representing the ending coordinates.

    Returns:
        float: The heading from the starting point to the ending point, in the range [0, 360) degrees.
               The heading is measured clockwise from the positive y-axis.
    """
    Xstart, Ystart = coordinates_1
    Xend, Yend = coordinates_2

    # Calculate the change in X and Y coordinates
    dx = Xend - Xstart
    dy = Yend - Ystart

    # Calculate the angle in radians using atan2
    heading_rad = math.atan2(-dy, dx)

    # Convert radians to degrees
    heading_deg = math.degrees(heading_rad)

    # Normalize the heading to the range [0, 360) degrees
    heading_deg = (90 - heading_deg) % 360

    return round(heading_deg)


def calculate_speed(coordinates_1, tmsStart, coordinates_2, tmsEnd):
    """
    Calculate the speed between two points given their coordinates and timestamps.

    Args:
        coordinates_1 (tuple): Tuple (Xstart, Ystart) representing the starting coordinates.
        coordinates_2 (tuple): Tuple (Xend, Yend) representing the ending coordinates.
        tmsStart (float): Timestamp (in seconds) when the starting coordinates were recorded.
        tmsEnd (float): Timestamp (in seconds) when the ending coordinates were recorded.

    Returns:
        float: The speed between the two points in kilometers per hour (km/h), rounded to 1 decimal place.
    """
    dx = calculate_distance(
        coordinates_1, coordinates_2)   # Distance between the two points
    dt = tmsEnd - tmsStart              # Time difference

    if dt <= 0:
        # Prevent division by zero and return speed as 0 if time difference is non-positive
        # RTLS updates timestamp only if positional data (X,Y,Z) are updated. So, dt == 0, means that
        # position is not changed, assuming that vehicle is stationary.
        return 0

    # Calculate speed in meters per second (m/s)
    spd_MpSec = dx / dt

    # Convert speed to kilometers per hour (km/h)
    spd_MpHr = spd_MpSec * 3600
    spd_kMpHr = spd_MpHr / 1000

    return round(spd_kMpHr, 1)
