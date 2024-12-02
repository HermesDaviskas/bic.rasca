"""
Module: lightsController_gpioserver
File: lightsController_gpioserver.py

This module contains functions for controlling lights based on zone penetration status.

Dependencies:
- requests: Library for making HTTP requests.
- time: Standard Python library for time-related functions.
- config: Configuration file containing zone pin mapping and control URLs.
"""

import requests
import time
from config import ZONE_PIN_MAP, GPIO_SERVER_URL, GPIO_SERVER_HEADER


def set_all_lights(state):
    """
    Set the state of all lights.

    Args:
        state (bool): Boolean indicating the state to set (True for ON, False for OFF).

    Description:
        This function iterates over all the light pins defined in ZONE_PIN_MAP and sets each pin to the specified state.
        A delay is introduced between setting each pin to prevent overwhelming the server with rapid requests.
    """
    for pin in ZONE_PIN_MAP.values():
        _control_light_pin(pin, state)  # Control the state of the light pin
        time.sleep(0.4)  # Introduce a delay to avoid overwhelming the server


def check_zones(objects):
    """
    Check the penetration status of zones and control the lights accordingly.

    Args:
        objects (dict): A dictionary where each key is an object ID and each value is a dictionary containing object information.
                        Each object should include a list of zone names under the "liz" key, which indicates warning lights zones.

    Description:
        This function determines which zones are currently penetrated by checking each object's zone list.
        It then controls the corresponding lights based on whether each zone is penetrated or not.
    """
    # Determine which zones are currently penetrated
    penetrated_zones = {zone for obj in objects.values()
                        for zone in obj.get("liz", [])}

    # Control the lights for each zone based on its penetration status
    for zone, pin in ZONE_PIN_MAP.items():
        # Set the light to ON if the zone is not penetrated; otherwise, set it to OFF
        _control_light_pin(pin, zone not in penetrated_zones)


def _control_light_pin(pin, state):
    """
    Control the state of a light pin.

    Args:
        pin (int): The pin number of the light to control.
        state (bool): Boolean indicating the desired state for the light.
                      True for ON, False for OFF.

    Description:
        Sends a command to the GPIO server to set the specified light pin to the desired state.
        Handles exceptions that occur during the HTTP request to ensure that any errors are logged.
    """
    try:
        # Prepare the command payload
        cmd = {"pin": pin, "state": state}

        # Send the command to the GPIO server
        response = requests.post(
            GPIO_SERVER_URL, json=cmd, headers=GPIO_SERVER_HEADER
        )

        # Raise an exception if the HTTP response indicates an error
        response.raise_for_status()

    except requests.exceptions.RequestException as e:
        # Print an error message if an exception occurs
        print(f"Error controlling pin {pin}: {e}")
