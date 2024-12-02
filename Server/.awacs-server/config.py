"""
Module: config
File: config.py

This module defines user-defined settings for the RTLS server, MQTT broker, and lights controller. 
It also includes predefined settings for API endpoints, headers, and URLs related to the RTLS system 
and lights controller.

Dependencies: None
"""

# USER DEFINED SETTINGS

# RTLS SERVER
# IP address of the RTLS server
RTLS_IP = "192.168.10.112"
# Port number for the RTLS server HTTP API
RTLS_PORT = "8080"
# API key for accessing the RTLS server
RTLS_X_API_KEY = "gduVczl0kn1TBeMOKuYQIygrt"
# Port number for the RTLS server WebSocket API
RTLS_WS_PORT = "8080"

# DATA PROCESSING
# IGNORE POSITION CHANGES EQUAL OR LESS THAN:
POS_FLUCTUATION_FILTER = 0.8

# DESIGNATE BAD SIGNAL ZONES:
BSZ1 = {
    (0, 21), (10, 30)
}
BAD_SIGNAL_ZONES = [BSZ1]

# MQTT
# IP address of the MQTT broker
MQTT_IP = "192.168.20.150"
# Port number for the MQTT broker
MQTT_PORT = 1884

# LIGHTS CONTROLLER
# IP address of the GPIO server for lights control
GPIO_SERVER_IP = "192.168.10.150"
# Port number for the GPIO server
GPIO_SERVER_PORT = "4000"
# Mapping of light zone identifiers to GPIO pins
ZONE_PIN_MAP = {"LZ1": 2, "LZ2": 3, "LZ3": 14, "LZ4": 4}


# DO NOT CHANGE
# GENERATED CONST FROM USER DEFINED SETTINGS

# Constructed URL for the RTLS server HTTP API
RTLS_HTTP_API_URL = f"http://{RTLS_IP}:{RTLS_PORT}/sensmapserver/api/tags"
# Headers for the RTLS server API requests
RTLS_HEADERS = {'X-ApiKey': RTLS_X_API_KEY}
# Constructed URL for the RTLS server WebSocket API
RTLS_WS_API_URL = f'ws://{RTLS_IP}:{RTLS_WS_PORT}'
# Subscription command for the RTLS server WebSocket API
RTLS_WS_SUB_COMMAND = {
    "headers": {"X-ApiKey": RTLS_X_API_KEY},
    "method": "subscribe",
    "resource": "/feeds/"
}

# Headers for the GPIO server API requests
GPIO_SERVER_HEADER = {"Content-Type": "application/json"}
# Constructed URL for the GPIO server API
GPIO_SERVER_URL = f"http://{GPIO_SERVER_IP}:{GPIO_SERVER_PORT}/gpio/control"
