import requests
import os
from app.config import Config

# Get token vault configs
AUTH0_CUSTOM_API_CLIENT_ID=Config.AUTH0_CUSTOM_API_CLIENT_ID
AUTH0_CUSTOM_API_CLIENT_SECRET=Config.AUTH0_CUSTOM_API_CLIENT_SECRET
AUTH0_DOMAIN=Config.AUTH0_DOMAIN
GITHUB_CONNECTION_NAME=Config.GITHUB_CONNECTION_NAME


def get_management_api_token():
    """Get an Auth0 Management API token using client credentials."""
    response = requests.post(
        f"https://{AUTH0_DOMAIN}/oauth/token",
        json={
            "grant_type": "client_credentials",
            "client_id": AUTH0_CUSTOM_API_CLIENT_ID,
            "client_secret": AUTH0_CUSTOM_API_CLIENT_SECRET,
            "audience": f"https://{AUTH0_DOMAIN}/api/v2/",
        }
    )
    response.raise_for_status()
    return response.json()["access_token"]


def get_github_token_from_vault(auth0_user_id):
    """
    Fetch the GitHub access token stored in Auth0 Token Vault
    for a given Auth0 user (identified by their sub/auth0_id).
    """
    try:
        mgmt_token = get_management_api_token()

        # fetch the user's connected accounts from Auth0
        response = requests.get(
            f"https://{AUTH0_DOMAIN}/api/v2/users/{auth0_user_id}",
            headers={
                "Authorization": f"Bearer {mgmt_token}",
                "Content-Type": "application/json",
            }
        )
        response.raise_for_status()
        user_data = response.json()

        # find the github identity in the user's linked accounts
        identities = user_data.get("identities", [])
        for identity in identities:
            if identity.get("connection") == GITHUB_CONNECTION_NAME:
                access_token = identity.get("access_token")
                if access_token:
                    return access_token

        return None

    except Exception as e:
        print(f"Token Vault error: {e}")
        return None


def connect_github_account(auth0_user_id, github_access_token):
    """
    Link a GitHub account to an Auth0 user profile,
    storing the token in Token Vault.
    """
    try:
        mgmt_token = get_management_api_token()

        # link the github account to the auth0 user
        response = requests.post(
            f"https://{AUTH0_DOMAIN}/api/v2/users/{auth0_user_id}/identities",
            headers={
                "Authorization": f"Bearer {mgmt_token}",
                "Content-Type": "application/json",
            },
            json={
                "provider": "github",
                "connection": GITHUB_CONNECTION_NAME,
                "access_token": github_access_token,
            }
        )
        response.raise_for_status()
        return True

    except Exception as e:
        print(f"Token Vault link error: {e}")
        return False