import json
import os
import time
from gpiozero import LED
from threading import Thread, Event
from signal import signal, SIGTERM

# Setup for the GPIO pin, change the pin number as needed
pin_number = 21
led = LED(pin_number)

# Event to control the toggling thread
stop_event = Event()
toggle_thread = None
toggle_flag_file = '/tmp/alarm_toggle.flag'

def toggle_led():
    """Function to toggle the LED on and off at intervals."""
    while not stop_event.is_set():
        led.off()
        time.sleep(0.35)
        led.on()
        
        led.off()
        time.sleep(0.35)
        led.on()
        
        time.sleep(0.7)

def handle_signal(signum, frame):
    """Handle termination signal."""
    global stop_event, toggle_thread
    stop_event.set()
    if toggle_thread and toggle_thread.is_alive():
        toggle_thread.join()
    led.on()
    os.remove(toggle_flag_file)
    exit(0)

def check_flag_file():
    """Check if the toggle flag file exists."""
    return os.path.exists(toggle_flag_file)

def run():
    """Main function to run the LED toggle service."""
    global toggle_thread
    signal(SIGTERM, handle_signal)
    while True:
        if check_flag_file():
            if toggle_thread is None or not toggle_thread.is_alive():
                stop_event.clear()
                toggle_thread = Thread(target=toggle_led)
                toggle_thread.start()
        else:
            if toggle_thread and toggle_thread.is_alive():
                stop_event.set()
                toggle_thread.join()
            led.on()
        time.sleep(0.1)

if __name__ == '__main__':
    run()
