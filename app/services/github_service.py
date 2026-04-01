import requests
from config import Config


def get_user_repos(token):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{Config.GITHUB_API}/user/repos", headers=headers)
    return response.json()


def get_commit_count(token):
    # TODO: You implement this
    # Hint: use /repos/{owner}/{repo}/commits
    return 0