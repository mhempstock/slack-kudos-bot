# Slack Kudos Bot

A Slack bot that spreads positivity and recognition in your team by allowing users to give kudos (or emojis) to each other using Slack commands and mentions. This bot tracks points, maintains leaderboards, and promotes a culture of appreciation!

---

## Features 🚀
- **Give Kudos**: Mention teammates and add emojis to reward them.
- **Leaderboard**: See the top-recognized teammates with `/kudos leaderboard`.
- **Weekly Leaderboard**: Check the weekly leaders with `/kudos weekly`.
- **Points Tracker**: View your remaining emojis for the day with `/kudos points`.
- **Custom Emoji**: Customize the emoji used for giving kudos.
- **Public Announcements**: Announce achievements in public channels.

---

## Slash Commands ⚡
- **`/kudos leaderboard`**: Displays the all-time leaderboard.
- **`/kudos weekly`**: Shows the top performers for the week.
- **`/kudos points`**: Checks how many emojis you have left to give today.
- **`/kudos help`**: Displays a help message with command usage.

---

## Giving Kudos 🌟
Mention one or more teammates and add emojis to give kudos. For example:
:taco: Great job on the release @user1 @user2!


- If you mention multiple users, they each get the specified number of emojis.
- emojis are distributed equally to each recipient.
- Self-giving is allowed, but a friendly reminder to share the love will be sent!

---

## Installation & Setup ⚙️

### Prerequisites:
- AWS Account with permissions to create Lambda functions, API Gateway, and DynamoDB tables.
- AWS CLI and SAM CLI installed.
- Python 3.13 installed locally.

### Environment Variables:
Set the following environment variables for the bot to function:

```yaml
EMOJI: ":taco:"               # Emoji used for giving kudos
EMOJI_PLURAL: "emojis"         # Plural form of the emoji
MAX_POINTS_PER_USER_PER_DAY: "5" # Maximum emojis a user can give per day
BOT_NAME: "KudosBot"          # Name of your bot
VERIFICATION_TOKEN: "your-slack-verification-token"
BOT_TOKEN: "your-slack-bot-token"
ANNOUNCEMENT_CHANNEL: "general" # Channel to announce kudos (optional)
```
## Deploying with SAM:
### Build the application:
```sam build```

### Deploy the application:
```sam deploy --parameter-overrides $(yq -r '.Parameters | to_entries[] | "\(.key)=\(.value)"' env.yaml) --no-confirm-changeset --no-fail-on-empty-changeset```

After deployment, note the API Gateway URLs for Slash Commands and Event Subscriptions.

## Required OAuth Scopes:
Ensure your Slack app has the following OAuth scopes:


- `chat:write:` Post messages in channels.
- `users:read:` Fetch user display names.
- `channels:history:` Read channel messages for event subscriptions.
- `im:write:` Send direct messages to users.

## Setting Up in Slack:
### Slash Commands:

Command: /kudos
Request URL: https://YOUR_API_URL/slack/commands
Event Subscriptions:

Request URL: https://YOUR_API_URL/slack/events

### Subscribe to the following events:
message.channels: To monitor channel messages.
reaction_added: To track reactions (optional).
message.im: (Optional, for DMs)

## License 📄
This project is licensed under the MIT License. Feel free to use, modify, and distribute this bot as you see fit!
