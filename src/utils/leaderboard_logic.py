from src.services.dynamodb_service import get_user_points

def get_leaderboard_message():
    user_totals = get_user_points()
    message = "*Leaderboard*\n```\n"
    message += "{:<20} {:<10}\n".format("User", "Total")
    message += "-" * 30 + "\n"
    for user, total in user_totals:
        message += "{:<20} {:<10}\n".format(user, total)
    message += "```"
    return message

def get_leaderboard_message_weekly():
    user_totals = get_user_points(weekly=True)
    message = "*Leaderboard*\n```\n"
    message += "{:<20} {:<10}\n".format("User", "Total")
    message += "-" * 30 + "\n"
    for user, total in user_totals:
        message += "{:<20} {:<10}\n".format(user, total)
    message += "```"
    return message
