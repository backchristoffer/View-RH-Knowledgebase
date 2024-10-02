import os
import requests
from dotenv import load_dotenv

load_dotenv()

# get your offline token from https://access.redhat.com/management/api. check https://access.redhat.com/articles/3626371#bgenerating-a-new-offline-tokenb-3
def get_access_token():
    data = {
        "grant_type": "refresh_token",
        "client_id": "rhsm-api",
        "refresh_token": os.getenv("OFFTOKEN")
    }
    try:
        r = requests.post(url="https://sso.redhat.com/auth/realms/redhat-external/protocol/openid-connect/token", data=data)
        r.raise_for_status()
        return r.json().get("access_token")
    except requests.exceptions.RequestException as request_error:
        print(f"Error refreshing access token: {request_error}")
        return None
    except Exception as e:
        print(f"Error getting access token: {e}")
        return None