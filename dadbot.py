import requests
class DadBot:
    """Constructs the onboarding message and stores the state of which tasks were completed."""

    DAD_BLOCK = {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": (
                "Sure! Here's a doozy for you:\n\n"
            ),
        },
    }
    def __init__(self, channel):
        self.channel = channel
        self.username = "Dad Bot"
        self.icon_emoji = ":hear_no_evil:"
        self.timestamp = ""

    def get_message_payload(self):
        return {
            "ts": self.timestamp,
            "channel": self.channel,
            "username": self.username,
            "icon_emoji": self.icon_emoji,
            "blocks": [
                self.DAD_BLOCK,
                *self._get_dadjoke_block(),
            ],
        }

    def _get_dadjoke_block(self):
        joke = requests.get("https://icanhazdadjoke.com/", headers={'Accept': 'text/plain'})
        text = f"{joke.text} :rolling_on_the_floor_laughing: :rolling_on_the_floor_laughing: :rolling_on_the_floor_laughing:"
        return {"type": "section", "text": {"type": "mrkdwn", "text": text}},
