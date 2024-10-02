import os
import requests
import argparse
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
    
#based on https://access.redhat.com/management/api/case_management#/search/getKcsSearchResults
def get_kcs_articles(keyword, limit=100):
    access_token = get_access_token()

    if not access_token:
        raise Exception("Failed to get access token")
    
    kcs_api_url = "https://api.access.redhat.com/support/search/kcs"
    headers = {
        'Authorization': f"Bearer {access_token}",
        'Accept': 'application/json'
    }
    params = {
        'q': keyword,
        'rows': limit
    }

    response = requests.get(kcs_api_url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"failed to get the response. status code: {response.status_code}")

#need to be able to use this as CLI at first. WIP
def main():
    parser = argparse.ArgumentParser(
        description='fetch KCS articles',
        epilog='Example: python3 app.py 6988487 --limit 1'
    )
    parser.add_argument('query', type=str, help='Search query string (e.g., document id or keyword)')
    parser.add_argument('--limit', type=int, default=100, help='Limit number of results (default: 5)')

    args = parser.parse_args()

    data = get_kcs_articles(args.query, limit=args.limit)

    if data:
        import json
        print(json.dumps(data, indent=4))

if __name__ == '__main__':
    main()