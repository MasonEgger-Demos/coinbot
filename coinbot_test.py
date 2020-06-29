from slack import WebClient
from coinbot import CoinBot
import os

# create a slack client
slack_web_client = WebClient(token=os.environ.get("SLACK_TOKEN"))

# Get a new dad joke
dad_joke = CoinBot("#bot-testing")

# Get the onboarding message payload
message = dad_joke.get_message_payload()

print(message)

# Post the onboarding message in Slack
slack_web_client.chat_postMessage(**message)