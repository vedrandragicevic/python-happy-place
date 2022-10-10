import requests


def get_request(url, headers):
    response = requests.get(url, headers=headers)
    response = response.json()
    return response


def post_request(url, payload, headers):
    response = requests.post(url, json=payload, headers=headers)
    response = response.json()
    return response


def patch_request(url, payload, headers):
    response = requests.patch(url, json=payload, headers=headers)
    return response.json()


if __name__ == '__main__':
    # Bearer Token Authentication
    get_token_url = f"GET TOKEN URL"
    client_id, client_secret = "TEST ID", "TEST_SECRET"

    get_token_payload = {
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "client_credentials"
    }

    access_token_response = requests.post(get_token_url, data=get_token_payload, verify=False, allow_redirects=False,
                                          auth=(client_id, client_secret))

    access_token_response = access_token_response.json()
    token = access_token_response.get('access_token')
    print(f"GOT THE BENCHLING ACCESS TOKEN, SUCCESSFUL AUTHENTICATION!")

    api_headers = {'Authorization': 'Bearer ' + token}
