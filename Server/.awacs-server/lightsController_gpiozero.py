from gpiozero import LED
from time import sleep
from config import ZONE_PIN_MAP

# Dictionary to hold LED objects
leds = {pin: LED(pin) for pin in ZONE_PIN_MAP.values()}


def set_all_lights(state):
    """
    Set the state of all lights.

    Args:
        state (bool): Boolean indicating the state to set (True for ON, False for OFF).
    """
    for pin in leds:
        _control_light_pin(pin, state)
        sleep(0.8)  # Introduce a delay to prevent overwhelming the system


def check_zones(objects):
    """
    Check zone penetration status and control lights accordingly.

    Args:
        objects (dict): Dictionary containing object information. Each object should have a list of zone names under the "liz" key.
    """
    penetrated_zones = {zone for obj in objects.values()
                        for zone in obj["liz"]}

    for zone, pin in ZONE_PIN_MAP.items():
        # Set the light to ON if the zone is not penetrated, otherwise OFF
        _control_light_pin(pin, zone not in penetrated_zones)


def _control_light_pin(pin, state):
    """
    Control the state of a light pin.

    Args:
        pin (int): The pin number of the light to control.
        state (bool): Boolean indicating the desired state for the light.
                      True for ON, False for OFF.
    """
    try:
        # Use the maintained LED object to control the pin
        led = leds[pin]

        # Set the state of the LED
        if state:
            led.on()
        else:
            led.off()

    except Exception as e:
        print(f"Error controlling pin {pin}: {e}")
