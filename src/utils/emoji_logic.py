from src.services.dynamodb_service import add_points_to_user, get_number_of_points_given_so_far_today
from src.services.slack_service import get_from_slack, send_message_to_slack
from src.services.slack_service import send_dm_to_slack

import os
import re

# Global Constants
EMOJI = os.environ.get('EMOJI', ':taco:')
EMOJI_PLURAL = os.environ.get('EMOJI_PLURAL', 'tacos')
MAX_POINTS_PER_USER_PER_DAY = int(os.environ.get('MAX_POINTS_PER_USER_PER_DAY', 5))
ANNOUNCEMENT_CHANNEL = os.environ.get('ANNOUNCEMENT_CHANNEL', None)

MENTION_REGEX = r'<@([A-Z0-9]+)>'

def extract_recipients_from_message(message):
    """
    Extracts all mentioned recipients from the message.
    """
    recipients = re.findall(MENTION_REGEX, message)
    return list(set(recipients))  # Remove duplicates

def count_emojis_in_message(message):
    """
    Counts the number of emojis in a message.
    """
    emoji_pattern = re.escape(EMOJI)
    return len(re.findall(emoji_pattern, message))

def get_points_remaining_today(user_id):
    """
    Returns the number of points a user has left to give today.
    """
    points_given_today = get_number_of_points_given_so_far_today(user_id)
    points_remaining = MAX_POINTS_PER_USER_PER_DAY - points_given_today
    return max(points_remaining, 0)

def get_display_name(user_id):
    """
    Fetches the display name of a user from Slack using the user ID.
    Falls back to the real name if display name is not set.
    """
    response = get_from_slack('users.info', {'user': user_id})
    if response.get('ok'):
        user_profile = response['user']['profile']
        return user_profile.get('display_name') or user_profile.get('real_name') or "Unknown"
    else:
        return "Unknown"

def handle_the_giving_of_emojis(sender, message, channel):
    """
    Handles the process of giving emojis (tacos) to recipients.
    """
    # Extract Recipients
    recipients = extract_recipients_from_message(message)

    # Count the number of emojis in the message
    total_emoji_count = count_emojis_in_message(message)
    
    # Get points remaining for the sender today
    points_remaining_today = get_points_remaining_today(sender)
    
    # If no points left today, notify and exit
    if points_remaining_today <= 0:
        send_dm_to_slack(sender, f"Sorry, you've used all your {EMOJI_PLURAL} today.")
        return
    
    # Calculate total emojis that can be given today
    total_emojis_to_give = min(total_emoji_count, points_remaining_today)

    # If no emojis to give, exit
    if total_emojis_to_give <= 0:
        send_dm_to_slack(sender, f"No {EMOJI_PLURAL} to give.")
        return
    
    # Give the total emojis to each recipient
    for recipient in recipients:
        recipient_name = get_display_name(recipient)
        
        # Give all tacos to each recipient
        add_points_to_user(sender, recipient, recipient_name, channel, total_emojis_to_give)
        
        # Self-giving case
        if sender == recipient:
            sender_message = (f"You gave yourself {total_emojis_to_give} {EMOJI_PLURAL}! "
                              "Self-care is important, but remember to share the love too!")
            send_dm_to_slack(sender, sender_message)
        else:
            # Inform the sender
            sender_message = (f"{recipient_name} has been given {total_emojis_to_give} {EMOJI_PLURAL}.")
            send_dm_to_slack(sender, sender_message)

            # Inform the recipient
            recipient_message = (
                f"🎉 You received {total_emojis_to_give} {EMOJI_PLURAL} from *{get_display_name(sender)}*!\n"
                f"> _\"{message}\"_"
            )
            send_dm_to_slack(recipient, recipient_message)

        # Announce in Public Channel if applicable
    if ANNOUNCEMENT_CHANNEL:
        announcement = (
            f":tada: *{get_display_name(sender)}* gave *{total_emojis_to_give} {EMOJI_PLURAL}*\n"
            f">_\"{message}\"_"
        )
        send_message_to_slack(ANNOUNCEMENT_CHANNEL, announcement)
