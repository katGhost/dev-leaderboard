
from app.services.github_service import GithubService
# def calculate_points(commits):
#     return commits  # simple for MVP


# def rank_users(users):
#     return sorted(users, key=lambda x: x["points"], reverse=True)

def get_leaderboard(users):
    """
    users: list of dicts {'id': ..., 'github_token': ...}
    """
    leaderboard = []
    for user in users:
        github = GithubService(user["github_token"])
        score = github.get_weekly_contributions(user['github_username'])
        leaderboard.append({"id": user["id"], "score": score})

    # Sort descending by score
    leaderboard.sort(key=lambda x: x["score"], reverse=True)
    return leaderboard