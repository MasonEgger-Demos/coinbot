# import the library requests, which we'll use to fetch a dad joke from the 
# icanhazdadjoke.com API
import requests

# Create the DadBot Class
class DadBot:

    # Create a constant that contains the default text for the message
    DAD_BLOCK = {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": (
                "Sure! Here's a doozy for you:\n\n"
            ),
        },
    }

    # The constructor for the class. It takes the channel name as the a 
    # parameter. It then sets the channel, username, and icon_emoji as instance
    # variables.
    def __init__(self, channel):
        self.channel = channel

    # Craft and return the entire message payload as a dictionary.
    def get_message_payload(self):
        return {
            "channel": self.channel,
            "blocks": [
                self.DAD_BLOCK,
                *self._get_dadjoke_block(),
            ],
        }

    # Craft the dad joke by getting a random joke from the icanhazdadjoke.com 
    # API and return the section that contains the dad joke.
    def _get_dadjoke_block(self):
        joke = requests.get("https://icanhazdadjoke.com/", 
                            headers={'Accept': 'text/plain'})
        text = f"{joke.text} :rolling_on_the_floor_laughing: "
        ":rolling_on_the_floor_laughing: :rolling_on_the_floor_laughing:"
        return {"type": "section", "text": {"type": "mrkdwn", "text": text}},
