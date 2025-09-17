
import requests
from typing import List, Dict, Any, Optional

def register_user(base_url, username, password):
    """
    Registers a new user with the Polly-API.

    Args:
        base_url (str): The base URL of the API (e.g., "http://localhost:8000").
        username (str): The desired username.
        password (str): The desired password.

    Returns:
        requests.Response: The response object from the API call.
    """
    url = f"{base_url}/register"
    user_data = {"username": username, "password": password}
    try:
        response = requests.post(url, json=user_data)
        response.raise_for_status()  # Raise an exception for bad status codes
        return response
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

def get_polls(base_url: str, skip: int = 0, limit: int = 10) -> Optional[List[Dict[str, Any]]]:
    """
    Fetches a paginated list of polls from the Polly-API.

    Args:
        base_url (str): The base URL of the API (e.g., "http://localhost:8000").
        skip (int): The number of polls to skip for pagination.
        limit (int): The maximum number of polls to return.

    Returns:
        Optional[List[Dict[str, Any]]]: A list of poll objects as dictionaries, 
                                         or None if an error occurs.
    """
    url = f"{base_url}/polls"
    params = {"skip": skip, "limit": limit}
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching polls: {e}")
        return None
    except requests.exceptions.JSONDecodeError:
        print("Failed to decode JSON from response.")
        return None

if __name__ == '__main__':
    # Example usage:
    BASE_URL = "http://localhost:8000"
    
    # --- Register User Example ---
    new_username = "testuser"
    new_password = "testpassword"

    print(f"Registering user '{new_username}'...")
    response = register_user(BASE_URL, new_username, new_password)

    if response:
        print(f"Status Code: {response.status_code}")
        try:
            print("Response JSON:", response.json())
        except requests.exceptions.JSONDecodeError:
            print("Response content is not in JSON format.")
            print("Response Text:", response.text)

    print("\n" + "="*20 + "\n")

    # --- Get Polls Example ---
    print("Fetching polls with default pagination (skip=0, limit=10)...")
    polls = get_polls(BASE_URL)
    if polls is not None:
        print(f"Successfully fetched {len(polls)} polls.")
        for poll in polls:
            print(f"  - Poll ID: {poll.get('id')}, Question: {poll.get('question')}")
    else:
        print("Failed to fetch polls.")

    print("\nFetching next page of polls (skip=10, limit=10)...")
    polls_page_2 = get_polls(BASE_URL, skip=10, limit=10)
    if polls_page_2 is not None:
        print(f"Successfully fetched {len(polls_page_2)} polls.")
        for poll in polls_page_2:
            print(f"  - Poll ID: {poll.get('id')}, Question: {poll.get('question')}")
    else:
        print("Failed to fetch the next page of polls.")
