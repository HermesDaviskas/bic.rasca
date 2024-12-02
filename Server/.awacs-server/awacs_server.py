"""
Module: RASCA_server
File: RASCA_server.py

This module defines the main application for managing RTLS tags, updating their states, and communicating 
with an MQTT broker to send telemetry data. It includes functions for initializing objects, updating them, 
creating vectors, and controlling warning lights.

Dependencies:
    - config
    - locServerRequests
    - dataProcessing
    - lightsController_gpioserver or lightsController_gpiozero
    - paho.mqtt.publish
    - time
    - json
"""

from config import MQTT_IP, MQTT_PORT
from locServerRequests import GetAllTags
from dataProcessing import createObject, updateObject, create_vector
from lightsController_gpioserver import check_zones, set_all_lights
#from lightsController_gpiozero import check_zones, set_all_lights
import paho.mqtt.publish as pub
from time import sleep
from json import dumps


def initialize_objects():
    """
    Initialize objects for all tags retrieved from the location server.

    Retrieves tag data from the location server and creates an object for each tag using the `createObject` function.

    Returns:
        dict: A dictionary where keys are object IDs and values are the initialized objects.
    """
    obj_dict = {}  # Initialize an empty dictionary to store objects

    try:
        # Retrieve all tags from the location server
        response = GetAllTags()

        # Process each tag in the response
        for result in response.get('results', []):
            # Convert the tag ID to an integer
            result_id = int(result['id'])

            # Create an object for each tag and add it to the dictionary
            obj_dict[result_id] = createObject(result_id, result)

    except Exception as e:
        # Print an error message if an exception occurs during initialization
        print(f"Failed to initialize objects: {str(e)}")

    return obj_dict


def update_objects(obj_dict):
    """
    Update existing objects with the latest data from the location server.

    Retrieves updated tag data from the location server and applies changes to objects that exist in the provided dictionary.

    Args:
        obj_dict (dict): The dictionary of objects to update, where keys are object IDs and values are the objects.

    Returns:
        None
    """
    try:
        # Retrieve all tags from the location server
        response = GetAllTags()

        # Process each tag in the response
        for result in response.get('results', []):
            # Convert the tag ID to an integer
            result_id = int(result['id'])

            # Check if the object with the given ID exists in the dictionary
            if result_id in obj_dict:
                # Update the existing object with the new data
                updateObject(obj_dict[result_id], result)

    except Exception as e:
        # Print an error message if an exception occurs during the update process
        print(f"Failed to update objects: {str(e)}")


def create_vectors(obj_dict):
    """
    Create vectors between tags and store them in the objects.

    Calculates vectors between each tag and all other tags and updates the objects with these vectors.

    Args:
        obj_dict (dict): A dictionary where keys are object IDs and values are the objects to create vectors for.

    Returns:
        None
    """
    try:
        # Iterate over each object ID in the dictionary
        for this_id in obj_dict.keys():
            vectors_array = []  # Initialize a list to store vectors for the current object

            # Compare the current object with every other object
            for other_id, other_obj in obj_dict.items():
                # Skip vector creation if comparing the object with itself
                if other_id != this_id:
                    # Create a vector between the current object and another object
                    vector = create_vector(obj_dict[this_id], other_obj)
                    # Add the created vector to the list
                    vectors_array.append(vector)

            # Update the current object with the list of vectors
            obj_dict[this_id]['vct'] = vectors_array

    except Exception as e:
        # Print an error message if an exception occurs during vector creation
        print(f"Failed to create vectors: {str(e)}")


def send_telemetry(obj_dict):
    """
    Send telemetry data for all objects to the MQTT broker.

    Publishes the telemetry data for each object to the specified MQTT broker. 
    Introduces a slight delay between messages to avoid overwhelming the broker.

    Args:
        obj_dict (dict): A dictionary where keys are object IDs and values are the telemetry data to be sent.

    Returns:
        None
    """
    # Iterate over each object in the dictionary
    for key, value in obj_dict.items():
        # Slight delay between publishing messages to avoid overwhelming the broker
        sleep(0.05)

        try:
            # Publish the telemetry data to the MQTT broker
            pub.single(str(key), payload=dumps(value),
                       hostname=MQTT_IP, port=MQTT_PORT)
        except Exception as e:
            # Print an error message if publishing fails
            print(f"Failed to publish to topic '{key}': {e}")


def main():
    """
    Main function to run the application.

    This function initializes the system, including lights and objects, and then enters a continuous loop where it:
    1. Updates the object data from the location server.
    2. Creates vectors between objects.
    3. Controls warning lights based on object zones.
    4. Sends updated telemetry data to the MQTT broker.

    The function handles any exceptions that occur during execution and logs error messages.
    """
    try:
        # Initialize lights
        set_all_lights(False)  # Turn lights ON
        set_all_lights(True)   # Turn lights OFF

        # Initialize objects
        obj_dict = initialize_objects()

        # Enter the working loop
        while True:
            # Delay between iterations to manage the frequency of updates
            sleep(0.15)

            # Update objects with the latest data from the location server
            update_objects(obj_dict)

            # Create vectors for each object relative to other objects
            create_vectors(obj_dict)

            # Control warning lights based on the current zones of objects
            print(obj_dict)
            check_zones(obj_dict)

            # Send telemetry data for each object to the MQTT broker
            send_telemetry(obj_dict)

    except Exception as e:
        # Print an error message if an exception occurs
        print(f"Main application error: {str(e)}")


if __name__ == "__main__":
    """
    Entry point of the script.

    This block ensures that the `main` function is executed when the script is run directly,
    but not when it is imported as a module in another script.
    """
    main()
