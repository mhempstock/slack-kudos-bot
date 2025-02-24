import boto3
from datetime import datetime, timedelta
from boto3.dynamodb.conditions import Key, Attr
from collections import Counter

# DynamoDB Table Setup
dynresource = boto3.resource('dynamodb')
table = dynresource.Table('emoji_log')

def add_points_to_user(sender, recipient, recipient_name, channel, points):
    """
    Records the points in DynamoDB along with the recipient's and sender's real names.
    """
    now = datetime.now().isoformat()
    table.put_item(Item={
        'sender': sender,
        'recipient': recipient,
        'recipient_name': recipient_name,
        'channel': channel,
        'points': points,
        'datetime_given': now
    })


def get_user_points(weekly=False):
    """
    Fetches the total points each user has received, summed up from DynamoDB.
    If `weekly=True`, only include points from the current week.
    """
    if weekly:
        start_of_week = (datetime.now() - timedelta(days=datetime.now().weekday())).isoformat()
        results = table.scan(FilterExpression=Attr('datetime_given').gte(start_of_week))['Items']
    else:
        results = table.scan(ProjectionExpression='recipient_name, points')['Items']

    # Sum up the points for each recipient
    recipients = []
    for item in results:
        points = int(item.get('points', 0))  # Safely parse points as an integer
        recipient_name = item.get('recipient_name', '[Unknown]')
        recipients.append((recipient_name, points))

    # Calculate totals for each recipient
    totals = Counter()
    for recipient, points in recipients:
        totals[recipient] += points

    # Return as a sorted list of tuples
    return totals.most_common()


def get_number_of_points_given_so_far_today(user_id):
    """
    Calculates the total points given by the user today.
    """
    start_of_day = datetime.now().date().isoformat()
    end_of_day = (datetime.now().date() + timedelta(1)).isoformat()

    results = table.query(
        KeyConditionExpression=Key('sender').eq(user_id) & Key('datetime_given').between(start_of_day, end_of_day)
    )['Items']

    # Sum up the points given today
    total_points_given = sum(int(item.get('points', 0)) for item in results)
    
    return total_points_given
