import requests
import json

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

# Load configuration from the file
with open('config.json') as config_file:
    config = json.load(config_file)

# Extract values from the configuration
email = config.get('email')
password = config.get('password')
device_name = config.get('device_name')

if not email or not password or not device_name:
    print("Error: Email, password, and device_name must be specified in the config file.")
else:
    # Call the function to get the token
    token = get_token(email, password, device_name)

    # Check if the token is obtained successfully
    if token:
        print("Token: {}".format(token))
        observations_url = 'https://budburst.org/api/observations'

        # Parameters for the request
        params = {
            'report_type': 'phenophase',  # or 'pollinators' or 'monarchs'
            'per_page': 50,
            'page': 1,
            'created_after': 'YYYY-MM-DD',  # Replace with the actual date
            'created_before': 'YYYY-MM-DD',  # Replace with the actual date
            'modified_after': 'YYYY-MM-DD',  # Replace with the actual date
            'modified_before': 'YYYY-MM-DD'  # Replace with the actual date
        }

        # Headers with the Authorization token
        headers = {
            'Authorization': f'Bearer {token}',
            'Accept': 'application/json',
        }

        # Make the request to the observations endpoint
        response = requests.get(observations_url, params=params, headers=headers)

        # Check the response
        if response.status_code == 200:
            # Parse and print the response JSON
            observations_data = response.json()
            print(observations_data)
        else:
            print(f"End. Request failed with status code {response.status_code}")
            print("Response:", response.text)
