import os
import requests
import logging

SLACK_ROOT = "https://slack.com/api/"
POST_MESSAGE = "chat.postMessage"
GET_USERS = 'users.list'
BOT_TOKEN = os.environ.get('BOT_TOKEN')


import os
import requests

# Global Constants
SLACK_ROOT = "https://slack.com/api/"
POST_MESSAGE = "chat.postMessage"
OPEN_DM = "conversations.open"
BOT_TOKEN = os.environ.get('BOT_TOKEN')

def send_dm_to_slack(user_id, message):
    """
    Sends a Direct Message (DM) to a specific user in Slack.
    """
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {BOT_TOKEN}"
    }
    
    # Open a DM channel with the user
    open_dm_response = requests.post(
        SLACK_ROOT + OPEN_DM,
        headers=headers,
        json={"users": user_id}
    )
    open_dm_response.raise_for_status()
    dm_channel = open_dm_response.json().get('channel', {}).get('id')
    
    if not dm_channel:
        raise Exception(f"Failed to open DM channel: {open_dm_response.json()}")

    # Send message to the opened DM channel
    message_data = {
        "channel": dm_channel,
        "text": message
    }
    response = requests.post(
        SLACK_ROOT + POST_MESSAGE,
        headers=headers,
        json=message_data
    )
    response.raise_for_status()
    return response.json()



def send_message_to_slack(channel, message):
    data = {
        "token": BOT_TOKEN,
        "channel": channel,
        "text": message
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    response = requests.post(
        SLACK_ROOT + POST_MESSAGE,
        data=data,
        headers=headers
    )
    response.raise_for_status()
    return response.json()


def get_from_slack(endpoint, params=None):
    url = SLACK_ROOT + endpoint
    headers = {
        "Authorization": f"Bearer {BOT_TOKEN}"
    }
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()

        if not data.get('ok'):
            logging.error(f"Slack API Error: {data.get('error')}")
            return {}

        return data

    except requests.exceptions.RequestException as e:
        logging.error(f"Error connecting to Slack API: {str(e)}")
        return {}


def fetch_user_info():
    local_user_mappings = {}
    user_info_response = get_from_slack(GET_USERS)

    if not user_info_response.get('ok'):
        logging.error(f"Slack API Error: {user_info_response.get('error')}")
        return local_user_mappings

    for user in user_info_response.get('members', []):
        display_name = user['profile'].get('display_name') or user['profile'].get('real_name')
        local_user_mappings[user['id']] = display_name
    
    return local_user_mappings

