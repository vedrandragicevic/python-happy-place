import boto3
import base64
import json
import requests
import urllib3
import logging
urllib3.disable_warnings()


def get_requests(url, headers, secret):
    response = requests.get(url, headers=headers, auth=(secret, ''))
    response = response.json()
    return response


def post_requests(url, payload, secret):
    response = requests.post(url, json=payload, auth=(secret, ''))
    response = response.json()
    return response


def patch_requests(url, payload, secret):
    response = requests.patch(url, json=payload, auth=(secret, ''))
    return response.text


def second_version_get_request(url: str, api_call_headers: dict) -> dict:
    """
    API GET request function.
    :param url: Endpoint URL
    :param api_call_headers: dict -> {'Authorization': 'Bearer ' + token}
    :return: API get request response as dict
    """
    response = requests.get(url, headers=api_call_headers, verify=False)
    response = response.json()
    return response


def second_version_post_request(url: str, payload: dict, api_call_headers: dict) -> dict:
    """
    API POST request function.
    :param url: Endpoint URL
    :param api_call_headers: dict -> {'Authorization': 'Bearer ' + token}
    :param payload: json payload for post request
    :return: API post request response as dict
    """
    response = requests.post(url, json=payload, headers=api_call_headers, verify=False)
    response = response.json()
    return response


def second_version_delete_request(url: str, api_call_headers: dict) -> str:
    """
    API DELETE request function.
    :param url: Endpoint URL
    :param api_call_headers: dict -> {'Authorization': 'Bearer ' + token}
    :return: API delete request response as str
    """
    response = requests.delete(url, headers=api_call_headers, verify=False)
    response = response.text
    return response
