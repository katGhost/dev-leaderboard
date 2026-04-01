import requests
from cachetools import TTLCache
from datetime import datetime, timedelta
from app.config import Config

# 1-hour in-memory cache for user weekly contributions
weekly_score_cache = TTLCache(maxsize=100, ttl=3600)

class GithubService:
    GITHUB_API_BASE_URL = Config.GITHUB_API_BASE_URL

    def __init__(self, token: str):
        self.token = token
        self.headers = {'Authorization': f'Bearer {self.token}'}

    def get_user_repos(self):
        """Fetch all user repos (reduces repeated calls)."""
        response = requests.get(f'{self.GITHUB_API_BASE_URL}/user/repos', headers=self.headers)
        response.raise_for_status()
        return response.json()

    def get_repo_commits(self, repo_full_name, since):
        """Get commits for a repo since the given datetime."""
        url = f'{self.GITHUB_API_BASE_URL}/repos/{repo_full_name}/commits'
        params = {"since": since.isoformat()}
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()

    def get_weekly_contributions(self):
        """Return total commits across all repos in the past 7 days, cached per token."""
        # Use token as cache key (or user_id if you prefer)
        cache_key = self.token
        if cache_key in weekly_score_cache:
            return weekly_score_cache[cache_key]

        since = datetime.utcnow() - timedelta(days=7)
        repos = self.get_user_repos()
        total_commits = 0

        for repo in repos:
            # Only count user's own commits in each repo
            commits = self.get_repo_commits(repo['full_name'], since)
            total_commits += len([c for c in commits if c.get('author') and c['author'].get('login')])

        weekly_score_cache[cache_key] = total_commits
        return total_commits