import os
import logging
from flask import Flask
from slack import WebClient
from slackeventsapi import SlackEventAdapter
from dadbot import DadBot

# Initialize a Flask app to host the events adapter
app = Flask(__name__)
slack_events_adapter = SlackEventAdapter("cdee3bb4e6c9c083c47ffefa875669a5", "/slack/events", app)

# Initialize a Web API client
slack_web_client = WebClient(token="xoxb-275531859079-1156235827062-ZgkjQF5DLDXUKH23K10MGkfS")

def tell_joke(channel):
    # Get a new dad joke
    dad_joke = DadBot(channel)

    # Get the onboarding message payload
    message = dad_joke.get_message_payload()

    # Post the onboarding message in Slack
    slack_web_client.chat_postMessage(**message)

# ============== Message Events ============= #
# When a user sends a DM, the event type will be 'message'.
# Here we'll link the message callback to the 'message' event.
@slack_events_adapter.on("message")
def message(payload):
    """Display the onboarding welcome message after receiving a message
    that contains "start".
    """
    event = payload.get("event", {})

    channel_id = event.get("channel")

    text = event.get("text")

    if "hey sammy, tell me a joke" in text.lower():
        return tell_joke(channel_id)

if __name__ == "__main__":
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler())
    app.run(host='0.0.0.0', port=80)