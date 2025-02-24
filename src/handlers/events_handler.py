from src.utils.message_parser import parse_message
from src.utils.emoji_logic import handle_the_giving_of_emojis
from src.services.slack_service import send_message_to_slack

IGNORED_PATTERNS = [
    "Woohoo!",                   # Recipient notification
    "You received",        # Recipient notification
    "You gave yourself",          # Self-giving message
    "No valid recipients found",  # Error message
    "You've used all your"        # No points remaining
]

def handle_reaction_added(event):
    from src.services.slack_service import fetch_user_info
    user_mappings = fetch_user_info()

    reaction = event.get("reaction")
    user = event.get("user")
    item_user = event.get("item_user")
    channel = event.get("item", {}).get("channel")

    if user and item_user and channel:
        message = f"{user_mappings.get(user, '[Unknown User]')} reacted with :{reaction}: to a message from {user_mappings.get(item_user, '[Unknown User]')}"
        send_message_to_slack(channel, message)


def handle_message(data):
    slack_event = data.get('event', {})
    message_text = slack_event.get('text', '')
    # Ignore bot messages by matching known patterns
    if any(pattern in message_text for pattern in IGNORED_PATTERNS):
        return

    if "bot_id" in slack_event:
        return

    if slack_event.get("type") == "message" and "subtype" not in slack_event:
        slack_message = parse_message(slack_event)
        if slack_message and slack_message.recipients:
            handle_the_giving_of_emojis(
            sender=slack_message.sender,
            message=slack_message.message,
            channel=slack_message.channel
)

    elif slack_event.get("type") == "reaction_added":
        handle_reaction_added(slack_event)


