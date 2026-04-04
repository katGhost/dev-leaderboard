from app.services.github_service import GithubService
from app.models import User


def get_leaderboard():
    
    # Fetch all users with GitHub connected -> calculate their weekly contributions,
    # return sorted leaderboard.
    
    users_with_github = User.query.filter(
        User.github_token.isnot(None),
        User.github_username.isnot(None)
    ).all()

    leaderboard = []

    for user in users_with_github:
        try:
            github = GithubService(user.github_token)
            score = github.get_weekly_contributions(user.github_username)
            leaderboard.append({
                'name': user.name,
                'nickname': user.nickname,
                'picture': user.picture,
                'github_username': user.github_username,
                'score': score
            })
        except Exception as e:
            # giard against one bad token breaking the whole leaderboard
            print(f"Error fetching contributions for {user.github_username}: {e}")
            continue

    leaderboard.sort(key=lambda x: x['score'], reverse=True)
    return leaderboard

# define a user profile from the assumed profile in github service
