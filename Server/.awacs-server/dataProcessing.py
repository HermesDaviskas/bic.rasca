"""
Module: dataProcessing
File: dataProcessing.py

This module contains functions for creating and updating objects and processing data related to the RTLS system.

Dependencies:
- geometricFunctions: Module containing geometric calculation functions.
"""

from datetime import datetime
from geometricFunctions import calculate_angle, calculate_distance, calculate_heading, calculate_speed
from config import POS_FLUCTUATION_FILTER


def createObject(id, data):
    """
    Create an object with the given ID and data.

    Args:
        id (int): The ID of the object.
        data (dict): The data used to initialize the object.

    Returns:
        dict: The initialized object.
    """
    # Extract position (X, Y) from data
    pos = (_extract_pos(data, 'posX'), _extract_pos(data, 'posY'))
    # Extract timestamp from data
    tms = _extract_tms(data)
    # Extract moving zone names from data
    mvz = _extract_zone_names(data, 'M')
    # Extract warning lights zone names from data
    liz = _extract_zone_names(data, 'L')
    # Extract bad signal zone names from data
    bsz = _extract_zone_names(data, 'B')

    # Create the object with the extracted and default values
    obj = {
        "aka": data['alias'],  # Alias name of the object
        "soc": None,    # Placeholder for social interactions (not yet defined)
        "pos": pos,     # Current position
        "tms": tms,     # Current timestamp
        "his": {
            "pos": None,    # Placeholder for previous position
            "tms": None     # Placeholder for previous timestamp
        },
        "spd": None,    # Placeholder for speed (to be calculated later)
        "hdg": None,    # Placeholder for heading (to be calculated later)
        "mvz": mvz,     # Monitored zones
        "liz": liz,     # Location zones
        "bsz": bsz,     # Bad signal zones
        "vct": []       # Placeholder for vectors (to be calculated later)
    }

    return obj


def updateObject(obj, data):
    """
    Update the given object with new data.

    Args:
        obj (dict): The object to update.
        data (dict): The new data for the object.

    Returns:
        dict: The updated object.
    """

    # Update only if tag has moved more than the standart fluctuation inaccuaracy
    if (calculate_distance((_extract_pos(data, 'posX'), _extract_pos(data, 'posY')), obj.get('pos')) >= POS_FLUCTUATION_FILTER or obj.get('pos') == None):

        # Extract current position (X, Y) from data
        pos = (_extract_pos(data, 'posX'), _extract_pos(data, 'posY'))

        # Extract current timestamp from data
        tms = _extract_tms(data)

        # Set current position and timestamp as previous
        his_pos = obj.get('pos')
        his_tms = obj.get('tms')

        # Calculate speed if both current and historical timestamps are available
        # If tms == his_tms and <> of None, means that posX or posY haven't changed so spd = 0
        spd = calculate_speed(his_pos, his_tms, pos,
                              tms) if tms and his_tms else 0
        # Calculate heading if current and historical positions are different
        hdg = calculate_heading(
            his_pos, pos) if pos and his_pos and pos != his_pos else obj['hdg']

        # Update the object with new values
        obj.update({
            'pos': pos,      # Update position
            'tms': tms,      # Update timestamp
            'his': {
                'pos': his_pos,   # Update historical position
                'tms': his_tms    # Update historical timestamp
            },
            'spd': spd,      # Update speed
            'hdg': hdg      # Update heading
        })

    # Extract monitored zone names from data
    mvz = _extract_zone_names(data, 'M')
    # Extract location zone names from data
    liz = _extract_zone_names(data, 'L')
    # Extract bad signal zone names from data
    bsz = _extract_zone_names(data, 'B')

    # Update the object with new values
    obj.update({
        "mvz": mvz,     # Monitored zones
        "liz": liz,     # Location zones
        "bsz": bsz,      # Bad signal zones
        'vct': []        # Reset vectors
    })

    return obj


def create_vector(obj, other_obj):
    """
    Create a vector between two objects.

    Args:
        obj (dict): The source object.
        other_obj (dict): The target object.

    Returns:
        dict: The vector containing direction and radius.
    """
    my_pos = obj.get('pos')  # Position of the source object
    my_hdg = obj.get('hdg')  # Heading of the source object
    other_pos = other_obj.get('pos')  # Position of the target object
    # Calculate the direction angle if the heading is known.

    # direction = -1 means that the angle between two vehicles cannot be calculated as we don't know the heading of this vehicle,
    # direction = -2 means that the other vehicle is inside a fuzzy position zone.
    # direction = -3 means that both vehicles are inside a fuzzy position zone.
    contactIsFuzzy = False
    direction = calculate_angle(my_pos, other_pos, my_hdg) if my_hdg else -1
    if (other_obj['bsz'] != []):
        contactIsFuzzy = True
    if (obj['bsz'] != [] and other_obj['bsz'] != []):
        direction = -1
    # Calculate the distance between the source and target objects
    radius = calculate_distance(my_pos, other_pos)
    # Probably, the frontend will present multiple  incoming vehicle from all directions.
    vector = {
        "d": direction,  # Direction angle
        "r": radius,  # Distance radius
        "f": contactIsFuzzy
    }

    return vector


def _extract_pos(response, pos_id):
    """
    Extract position (X or Y) from the response.

    Args:
        response (dict): The response data containing various datastreams.
        pos_id (str): The position identifier ('posX' or 'posY') to extract.

    Returns:
        float: The extracted position value or None if not found.
    """
    # Iterate over each datastream in the response
    for stream in response.get('datastreams', []):
        # Check if the current datastream's ID matches the given position ID
        if stream['id'] == pos_id:
            # Extract and return the position value as a float
            return float(stream['current_value'].strip())

    # Return None if the position ID is not found in any datastream
    return None


def _extract_zone_names(response, zone_type):
    """
    Extract zone names of the given type from the response.

    Args:
        response (dict): The response data containing zone information.
        zone_type (str): The zone type prefix ('M' for moving zones, 'L' for warning lights zones).

    Returns:
        list: A list of zone names matching the given zone type.
    """
    zone_names = []

    # Check if the response is a dictionary and contains the 'zones' key
    if isinstance(response, dict) and 'zones' in response:
        # Iterate over each zone in the response
        for zone in response['zones']:
            # Check if the zone name starts with the given zone type prefix
            if zone.get('zone_name', '').startswith(zone_type):
                # Append the zone name to the list of zone names
                zone_names.append(zone['zone_name'])

    return zone_names


def _extract_tms(response):
    """
    Extract timestamps from 'posY' and 'posX' streams in the response and return the latest one.

    Args:
        response (dict): The response data containing datastreams.

    Returns:
        float: The latest timestamp as a Unix timestamp, or None if no valid timestamp is found.
    """
    datetime_format = '%Y-%m-%d %H:%M:%S.%f'  # Expected format for timestamps
    max_timestamp = None  # Initialize to track the latest timestamp

    # Iterate over each datastream in the response
    for stream in response.get('datastreams', []):
        # Check if the datastream's ID is either 'posY' or 'posX'
        if stream.get('id') in {'posY', 'posX'}:
            datetime_str = stream.get('at')  # Retrieve the timestamp string
            if datetime_str:
                try:
                    # Convert the timestamp string to a Unix timestamp
                    current_timestamp = datetime.strptime(
                        datetime_str, datetime_format).timestamp()
                    # Update max_timestamp if the current timestamp is newer
                    if max_timestamp is None or current_timestamp > max_timestamp:
                        max_timestamp = current_timestamp
                except ValueError as e:
                    # Print error message if timestamp parsing fails
                    print(f"Error parsing timestamp for {stream['id']}: {e}")

    return max_timestamp
