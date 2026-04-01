def calculate_points(commits):
    return commits  # simple for MVP


def rank_users(users):
    return sorted(users, key=lambda x: x["points"], reverse=True)