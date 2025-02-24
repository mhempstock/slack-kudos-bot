import re
from src.utils.emoji_logic import EMOJI  # Ensure this points to where EMOJI is defined

MENTION_REGEX = r'<@([A-Z0-9]+)>'

class SlackMessage:
    def __init__(self, sender, recipients, message, channel):
        self.sender = sender
        self.recipients = recipients
        self.message = message
        self.channel = channel

    def count_emojis_in_message(self):
        """
        Counts the number of specific emojis (e.g., :taco:) in the message.
        """
        emoji_pattern = re.escape(EMOJI)  # Escape to safely use in regex
        return len(re.findall(rf'{emoji_pattern}', self.message))

def parse_message(event):
    """
    Parses the incoming Slack event to extract sender, recipients, message text, and channel.
    Returns a SlackMessage object only if a user mention and the specific emoji are present.
    """
    if event['type'] == 'message' and 'subtype' not in event:
        sender_user_id = event['user']
        message_text = event['text']
        channel = event['channel']

        # Extract recipients only if the emoji is present
        recipients = _extract_recipient_from_message(message_text)
        if recipients:
            return SlackMessage(sender_user_id, recipients, message_text, channel)
    
    # Return None if conditions are not met
    return None

def _extract_recipient_from_message(message_text):
    """
    Extracts recipients only if the message contains both a user mention and the specific emoji.
    """
    # Use regex to find the emoji as a word
    emoji_pattern = re.escape(EMOJI)  # Escape to safely use in regex

    if not re.search(rf'(?:(?:^|\s)){emoji_pattern}(?=\s|$|[!?.])', message_text):
        return None
    
    # Extract mentions from the message
    matches = re.findall(MENTION_REGEX, message_text)

    # Return recipients if mentions are found and the emoji is present
    return matches if matches else None
