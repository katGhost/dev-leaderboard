import requests
from cachetools import TTLCache
from datetime import datetime, timedelta
from app.config import Config

# 1-hour in-memory cache
weekly_score_cache = TTLCache(maxsize=100, ttl=3600)

class GithubService:
    GITHUB_API_BASE_URL = Config.GITHUB_API_BASE_URL

    def __init__(self, token: str):
        self.token = token
        self.headers = {
            'Authorization': f'Bearer {self.token}',
            # required by GitHub API
            'Accept': 'application/vnd.github+json',
            'X-GitHub-Api-Version': '2022-11-28'
        }

    def get_user_repos(self):
        """Fetch ALL user repos across all pages, excluding forks."""
        repos = []
        page = 1

        while True:
            response = requests.get(
                f'{self.GITHUB_API_BASE_URL}/user/repos',
                headers=self.headers,
                params={
                    'per_page': 100,   # max allowed by GitHub
                    'page': page,
                    'type': 'owner',   # only repos the user owns, no collaborations
                    'sort': 'updated', # most recently updated first
                }
            )
            response.raise_for_status()
            page_repos = response.json()

            # no more pages
            if not page_repos:
                break

            for repo in page_repos:
                # skip forks and archived repos
                if repo.get('fork') or repo.get('archived'):
                    continue
                repos.append(repo)

            # GitHub returns less than per_page on the last page
            if len(page_repos) < 100:
                break

            page += 1

        return repos

    def get_repo_commits(self, repo_full_name, since, github_username):
        """Get commits by the authenticated user in a repo since a given date."""
        commits = []
        page = 1

        while True:
            response = requests.get(
                f'{self.GITHUB_API_BASE_URL}/repos/{repo_full_name}/commits',
                headers=self.headers,
                params={
                    'since': since.isoformat(),
                    'author': github_username,  # only this user's commits
                    'per_page': 100,
                    'page': page,
                }
            )

            # repo may be empty or inaccessible
            if response.status_code in (404, 409):
                break

            response.raise_for_status()
            page_commits = response.json()

            if not page_commits:
                break

            commits.extend(page_commits)

            if len(page_commits) < 100:
                break

            page += 1

        return commits

    def get_weekly_contributions(self, github_username: str):
        """Return total commits across all owned repos in the past 7 days."""
        cache_key = f"{self.token}:{github_username}"
        if cache_key in weekly_score_cache:
            return weekly_score_cache[cache_key]

        since = datetime.utcnow() - timedelta(days=7)
        repos = self.get_user_repos()
        total_commits = 0

        for repo in repos:
            commits = self.get_repo_commits(
                repo['full_name'],
                since,
                github_username
            )
            total_commits += len(commits)

        weekly_score_cache[cache_key] = total_commits
        return total_commits
    


"""HELPER FUNCTIONs"""

# get or extract user experience level from GitHub profile

    
# summarize user activity
def summarize_user_activity(github_token):

    github = GithubService(github_token)
    
    # get repos and commits to extract information for experience level classification
    since_last_7_days = datetime.utcnow() - timedelta(days=7)
    since_all_time = datetime.utcnow() - timedelta(days=365*10)

    # Get authenticated user's username
    user_response = requests.get(
        f'{GithubService.GITHUB_API_BASE_URL}/user',
        headers=github.headers
    )
    user_response.raise_for_status()
    github_username = user_response.json()['login']

    # Get repos, from repos get total commits first
    # get commits from the last 7 days
    repos = github.get_user_repos()
    total_commits = github.get_repo_commits(repos[0]['full_name'], since_all_time, github_username) if repos else []   # if user has repos else an empty array as fallnback
    commits_last_7_days = github.get_repo_commits(repos[0][ 'full_name'], since_last_7_days, github_username) if repos else []
    
    # simple heuristic based on public repos (and perhaps followers)
    if not repos:
        experience_level = 'No Repositories | Armature'
    elif len(total_commits) < 50 and len(repos) < 3:
        experience_level = 'Beginner'
    elif len(total_commits) >= 50 and len(commits_last_7_days) >= 10 and len(repos) >= 5:
        experience_level = 'Intermediate'
    elif len(total_commits) >= 200 and len(commits_last_7_days) >= 30 and len(repos) >= 10:
        experience_level = 'Advanced'
    else:
        experience_level = 'Intermediate'  # default to intermediate if they have some activity but don't meet advanced criteria
    
    # extract languages used across repos for AI recomendations
    languages = set()
    for repo in repos:
        if repo.get('language'):
            languages.add(repo['language'])
    
    # return an assumed user profile object
    return {
        'username': github_username,
        'experience_level': experience_level,
        'languages': list(languages),
        'total_commits': len(total_commits)
    }






