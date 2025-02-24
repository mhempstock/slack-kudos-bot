import os

EMOJI = os.environ.get('EMOJI', ':taco:')
EMOJI_PLURAL = os.environ.get('EMOJI_PLURAL', 'tacos')

def format_help_message():
    """
    Generates the help message for the Slack Kudos Bot.
    """
    help_text = (
        f"🎉 *Welcome to the Kudos Bot!* 🎉\n"
        "Here are the commands you can use to spread some love and recognition:\n\n"
        
        "*🌟 View Leaderboard*:\n"
        "`/kudos leaderboard` - See the all-time leaderboard.\n"
        "`/kudos weekly` - Check out this week's leaderboard.\n\n"
        
        f"*{EMOJI} Check Remaining Points*:\n"
        f"`/kudos points` - See how many {EMOJI_PLURAL} you have left to give today.\n\n"
        
        "*❓ Help*:\n"
        "`/kudos help` - Display this help message.\n\n"
        
        "💬 *Example Usage*:\n"
        "`/kudos leaderboard` - Shows the top performers of all time.\n"
        "`/kudos weekly` - Shows this week's high scorers.\n"
        f"`/kudos points` - Check your remaining {EMOJI_PLURAL} for today.\n\n"
        
        f"Spread the love with {EMOJI_PLURAL}! {EMOJI}"
    )
    return help_text
