"""
Module: locServerRequests
File: locServerRequests.py

This module contains functions for making requests to the location server and processing the response data.

Dependencies:
- requests: Library for making HTTP requests.
- config: Configuration module for defining API URLs and headers.
"""

import requests
from config import RTLS_HTTP_API_URL, RTLS_HEADERS


def GetAllTags():
    """
    Fetch the full data from the RTLS HTTP API.

    Returns:
        dict or None: The full JSON response from the API if successful, otherwise None.

    Raises:
        HTTPError: If the HTTP request returns an unsuccessful status code.
        RequestException: For other issues related to the request.
    """
    try:
        response = requests.get(RTLS_HTTP_API_URL, headers=RTLS_HEADERS)
        response.raise_for_status()  # Raises an HTTPError for bad responses (4xx, 5xx)
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"Request error occurred: {req_err}")
    except Exception as err:
        print(f"An unexpected error occurred: {err}")

    return None  # Return None explicitly if there's an error


def GetTag(id):
    """
    Fetch data for a specific tag from the RTLS HTTP API.

    Args:
        id (int or str): The ID of the tag to retrieve.

    Returns:
        dict or None: The JSON response for the tag if successful, otherwise None.

    Raises:
        HTTPError: If the HTTP request returns an unsuccessful status code.
        RequestException: For other issues related to the request.
    """
    try:
        response = requests.get(
            f'{RTLS_HTTP_API_URL}/{id}', headers=RTLS_HEADERS)
        response.raise_for_status()  # Raises an HTTPError for bad responses (4xx, 5xx)
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"Request error occurred: {req_err}")
    except Exception as err:
        print(f"An unexpected error occurred: {err}")

    return None  # Return None explicitly if there's an error
