import json
import requests

def get_token(email, password, device_name):
    # API endpoint for getting the token
    token_url = "https://budburst.org/api/sanctum/token"

    # Payload for the token request
    token_payload = {
        'email': email,
        'password': password,
        'device_name': device_name
    }

    # Headers for the token request
    token_headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    # Make the request to get the token
    response = requests.post(token_url, data=token_payload, headers=token_headers)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Split the response text using the pipe character
        response_parts = response.text.split('|')

        # Check if there are at least two parts in the response
        if len(response_parts) >= 2:
            # Extract the token from the second part
            token = response_parts[1]
            return token
        else:
            print("Unexpected response format. Unable to extract token.")
            return None
    else:
        print("Token request failed with status code {}".format(response.status_code))
        print("Response:", response.text)
        return None

def load_config(file_path='config.json'):
    try:
        with open(file_path) as config_file:
            config = json.load(config_file)
            return config
    except FileNotFoundError:
        print(f"Error: Config file '{file_path}' not found.")
        return None
    except json.JSONDecodeError:
        print(f"Error: Unable to decode JSON in '{file_path}'. Check the file format.")
        return None

def get_authorization_headers(file_path='config.json'):
    # Load configuration from the file
    config = load_config(file_path)

    if config is None:
        return None  # Exit if there is an issue with the config

    # Extract values from the configuration
    email = config.get('email')
    password = config.get('password')
    device_name = config.get('device_name')

    if not email or not password or not device_name:
        print("Error: Email, password, and device_name must be specified in the config file.")
        return None
    else:
        # Call the function to get the token
        token = get_token(email, password, device_name)

        # Check if the token is obtained successfully
        if token:
            # Headers with the Authorization token
            headers = {
                'Authorization': f'Bearer {token}',
                'Accept': 'application/json',
            }
            return headers
        else:
            return None
