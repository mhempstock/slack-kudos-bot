from src.services.slack_service import send_message_to_slack
from src.utils.leaderboard_logic import get_leaderboard_message, get_leaderboard_message_weekly
from src.utils.emoji_logic import handle_the_giving_of_emojis, get_points_remaining_today
from src.utils.helpers import format_help_message
import os

EMOJI_PLURAL = os.environ.get('EMOJI_PLURAL', 'tacos')


def handle_slash_command(slack_command):
    command_text = slack_command.get('text', '').lower().split()
    channel = slack_command['channel_id']
    sender = slack_command['user_id']

    if not command_text:
        return "Type `/kudos help` to see available commands."

    subcommand = command_text[0]

    if subcommand == 'leaderboard':
        formatted_message = get_leaderboard_message()
        send_message_to_slack(channel, formatted_message)

    elif subcommand == 'weekly':
        formatted_message = get_leaderboard_message_weekly()
        send_message_to_slack(channel, formatted_message)

    elif subcommand == 'points':
        remaining = get_points_remaining_today(sender)
        return f"You have {remaining} {EMOJI_PLURAL} left today."

    elif subcommand == 'help':
        formatted_message = format_help_message()
        return formatted_message

    else:
        return "Invalid command. Type `/kudos help` to see available commands."
    
    return None