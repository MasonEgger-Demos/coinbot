  *The author selected the [Tech Education Fund](https://www.brightfunds.org/funds/tech-education) to receive a donation as part of the [Write for DOnations](https://do.co/w4do-cta) program.*

## Introduction

[Slack](https://slack.com/) is a communication platform designed for workplace productivity. It includes features such as direct messaging, public and private channels, voice and video calls, as well as bot integrations. A Slackbot is an automated program that can perform a variety of functions in slack, from sending messages to triggering tasks to alerting on certain events. 

In this tutorial you will build a Slackbot in the [Python](https://www.python.org/) programming language. Python is a popular language that prides itself on simplicity and readability. Slack provides a rich [Python Slack API](https://github.com/slackapi/python-slackclient) for integrating with Slack to perform common tasks such as sending messages, adding emojis to message, etc. Slack also provides a [Python Slack Events API](https://github.com/slackapi/python-slack-events-api) for integrating with events in slack, allowing you to perform actions on events such as messages and mentions. This tutorial will use Python 3 and will not be compatible with Python 2.

## Prerequisites

In order to follow this guide, you'll need:

* A Slack Workspace that you have the ability to install applications into. If you created the workspace you have this ability. If you don't already have one, you can create one on the [Slack website](https://slack.com/create).

* (Optional) A server or computer with a public ip address for development. We recommend a fresh installation of Ubuntu 20.04, a non-root user with `sudo` privileges, and SSH enabled. [You can follow this guide to initialize your server and complete these steps](https://www.digitalocean.com/community/tutorials/initial-server-setup-with-ubuntu-20-04). 

<$>[note]
You may want to test this tutorial on a server that has a public ip address. Slack will need to be able to send events such as messages to your bot. If you are testing on a local machine you will need to port forward traffic through your firewall to your local system. If you are looking for a way to develop on a cloud server, check out this tutorial on [How To Use Visual Studio Code for Remote Development via the Remote-SSH Plugin](https://www.digitalocean.com/community/tutorials/how-to-use-visual-studio-code-for-remote-development-via-the-remote-ssh-plugin). 
<$>

## Step 1 — Creating the Slackbot in the Slack UI

The first thing we need to do is create our Slack app in the Slack API Control Panel. Login to your workspace in Slack via a web browser and navigate to the [API Control Panel](https://api.slack.com/apps). Here we will click on the **Create an App** button.

![Create Your Slack App](https://i.imgur.com/LGsKT6X.png)

Next you'll be prompted for the name of your app and to select a development slack workspace. For this tutorial name your app *DadBot* and select a workspace you have admin access to. Once you have done this click on the **Create App** button.

![Name Your Slack App and Select a Workspace](https://i.imgur.com/pKxppBq.png)

Once your app is created you'll be presented with the following default app dashboard. This dashboard is where you manage your app by setting permissions, subscribing to events, installing the app into workspaces, etc.

![Default Slack App Panel](https://i.imgur.com/ce4nTbk.png)

In order for our app to be able to post messages to a channel we need to grant the app permissions to send messages. To do this, click on the **Permissions** button in the control panel.

![Select the Permissions Button in the Control Panel](https://i.imgur.com/pf1YlSE.png)

When you arrive at the **OAuth & Permissions** page scroll down until you find the **Scopes** section of the page. You then need to find the **Bot Token Scopes** subsection in the scope and click on **Add an OAuth Scope** button.

![Select the Add an OAuth Scope Button](https://i.imgur.com/dAxWKdZ.png)

When you click on that button you'll need to type in `chat:write` and select that permission to add it to your bot as shown below This will allow the app to post messages to channels that it has been invited to. For more information on the available permissions refer to [Slack's Documentation](https://api.slack.com/scopes).

![Add the chat:write Permission](https://i.imgur.com/afv3zlD.png)

Now that we've added the appropriate permission it is time to install our app into our Slack workspace. Scroll back up on the **OAuth & Permissions** page and click the **Install App to Workspace** button at the top.

![Install App to Workspace](https://i.imgur.com/C02TSnT.png)

Once you click this button you'll need to review the actions the app can perform in the channel and then click the **Allow** button to finish the installation.

![Install App to Workspace](https://i.imgur.com/5ZpYTT2.png)

Once the bot is installed you'll be presented with a **Bot User OAuth Access Token** for your app to use when attempting to perform actions in the workspace. Go ahead and copy this token as we'll need it later.

![Save the Access Token](https://i.imgur.com/A1uOLZy.png)

Finally, you'll need to add your newly installed bot into a channel within your workspace. If you haven't created a channel yet you can use the *#general* channel that is created by default in your Slack workspace. *Locate the app in the **Apps** section of the navigation bar in your Slack client and click on it. Once you've done that open the **Details** menu in the top right hand side. If your slack client isn't full-screened it will look like an `i` in a circle.

![Click on the App Details Icon](https://i.imgur.com/P21Poph.png)

To finish adding your app to a channel you'll need to click on the **More** button represented by three dots in the details page and select **Add this app to a channel...**. Type in your channel into the modal that appears and click **Add** to add the bot to the channel.

![Add App to a Channel](https://i.imgur.com/9h9I9uC.png)

Now that you've successfully created and added your app to a channel within your workspace, once we write the code your app will be able to post messages in that channel. In the next section we'll start writing the Python code that will power this app. 


## Step 2 — Setting Up Our Python Developer Environment

Now let's setup our Python environment so we can develop the Slackbot.

The first thing we need to do is to open a terminal and install `python3` and the relevant tools onto our system.

```command
sudo apt install python3 python3-venv
```

Next we need to do is create a virtual environment to isolate our Python packages from the system installation of Python. We need to create a directory to create our virtual environment into. We'll do this at *~/.venvs*

```command
mkdir ~/.venvs
```

Now we can create our Python virtual environment:

```command
python3 -m venv ~/.venvs/slackbot
```

Next, we need to activate our virtual environment so we can use its Python installation and install packages.

```command
source ~/.venvs/slackbot/bin/activate
```

You will now see that your shell prompt will now show the virtual environment in parenthesis. For example:

```shell
(slackbot) sammy@slackbotserver:~$
```

Now we can install the necessary Python packages into our virtual environment.

```command
pip install slackclient slackeventsapi Flask requests
```

Now that we have our developer environment setup we can start writing our Python Slackbot.

## Step 3 — Creating the Slackbot Message Class in Python

Messages in Slack are sent via a [specifically formatted JSON payload](https://api.slack.com/reference/surfaces/formatting). Below is an example of the JSON that our Slackbot will craft and send as a message. 

```json
{
   "channel":"channel",
   "blocks":[
      {
         "type":"section",
         "text":{
            "type":"mrkdwn",
            "text":"Sure! Here\\'s a doozy for you:\\n\\n"
         }
      },
      {
         "type":"section",
         "text":{
            "type":"mrkdwn",
            "text":"I finally bought the limited edition Thesaurus that I\\'ve always wanted. When I opened it, all the pages were blank.\\r\\nI have no words to describe how angry I am. :rolling_on_the_floor_laughing: :rolling_on_the_floor_laughing: :rolling_on_the_floor_laughing:"
         }
      }
   ]
}
```

We could manually craft this JSON and send it, but instead let's build a Python class that not only crafts this payload, but fetches a random dad joke to send. 

First create a file named `dadbot.py`. 

```command
touch dadbot.py
```

Next, open this file with your favorite text editor and add the following lines of code to import the relevant libraries for our app. The only library we will need for this class is the `requests` library, which allows us to make HTTP requests to the dad joke API. 

Add the following lines to `dadbot.py` to import all of the necessary libraries.

```python
# import the library requests, which we'll use to fetch a dad joke from the 
# icanhazdadjoke.com API
import requests
```

Next we need to create our `DadBot` class. We will create an instance of this class
to craft the message payload.

Add the following lines `dadbot.py` to create the `DadBot` class.

```python
class DadBot:
```

Now we indent in one and create the constants, constructors and methods necessary for our class. First let's create the constant that will hold the base of our message payload. In this section we specify that this constant is of the section type, that the text is formatted via markdown and the text we wish to display in this section. You can read more about the different payload options in the [official Slack message payload documentation](https://api.slack.com/reference/messaging/payload). 

Append the following lines to `dadbot.py` to create the base template for the payload.

```python
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
```

Next we need to create a constructor for our class so we can create a separate instance of our bot for every request. Don't worry about memory overhead hear, the Python garbage collector will clean up these instances once they are no longer needed.  This code sets the recipient channel based on a parameter passed to the constructor, as well as sets the username and Slack icon.

Append the following lines to `dadbot.py` to create the constructor.

```python
    # The constructor for the class. It takes the channel name as the a 
    # parameter and sets it as an instance variable.
    def __init__(self, channel):
        self.channel = channel
```

Next we will write the code that actually fetches the dad joke from *https://icanhazdadjoke.com* using the `requests` library and creates a slack block section that is properly formatted. 

Append the following lines to `dadbot.py` to fetch the dad joke from the REST API and return the crafted joke section.

```python
    # Craft the dad joke by getting a random joke from the icanhazdadjoke.com 
    # API and return the section that contains the dad joke.
    def _get_dadjoke_block(self):
        joke = requests.get("https://icanhazdadjoke.com/", 
                            headers={'Accept': 'text/plain'})
        text = f"{joke.text} :rolling_on_the_floor_laughing: :rolling_on_the_floor_laughing: :rolling_on_the_floor_laughing:"
        return {"type": "section", "text": {"type": "mrkdwn", "text": text}},
```

Finally, we create a method that crafts and returns the entire message payload, including the data from our constructor and by calling our `_get_dadjoke_block` method. 


Append the following lines to `dadbot.py` to create the method that will create the finished method payload.
```python
    # Craft and return the entire message payload as a dictionary.
    def get_message_payload(self):
        return {
            "channel": self.channel,
            "blocks": [
                self.DAD_BLOCK,
                *self._get_dadjoke_block(),
            ],
        }
```

We are now finished with the `DadBot` class and it is ready for testing. Before we move on verify that your finished file, `dadbot.py` contains the following:
```python
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
    # parameter and sets it as an instance variable.
    def __init__(self, channel):
        self.channel = channel

    # Craft the dad joke by getting a random joke from the icanhazdadjoke.com 
    # API and return the section that contains the dad joke.
    def _get_dadjoke_block(self):
        joke = requests.get("https://icanhazdadjoke.com/", 
                            headers={'Accept': 'text/plain'})
        text = f"{joke.text} :rolling_on_the_floor_laughing: "
        ":rolling_on_the_floor_laughing: :rolling_on_the_floor_laughing:"
        return {"type": "section", "text": {"type": "mrkdwn", "text": text}},

    # Craft and return the entire message payload as a dictionary.
    def get_message_payload(self):
        return {
            "channel": self.channel,
            "username": self.username,
            "icon_emoji": self.icon_emoji,
            "blocks": [
                self.DAD_BLOCK,
                *self._get_dadjoke_block(),
            ],
        }
```

Now that we have a Python class ready to do the work for our Slackbot, let's ensure that this class produces a useful message payload and that we can send it to our workspace.


## Step 4 - Testing Our Message 

Now let's test that this class produces a proper payload. Create a file named
`dadbot_test.py` and add the following code. **Be sure to change the channel name in the instantiation of the DadBot class `dad_joke = DadBot("#YOUR_CHANNEL_HERE")`**. This code will create a slack client in Python that will send a message to the channel you specify that you have already installed the app into.

```python
from slack import WebClient
from dadbot import DadBot
import os

# Create a slack client
slack_web_client = WebClient(token=os.environ.get("SLACK_TOKEN"))

# Get a new dad joke
dad_joke = DadBot("#YOUR_CHANNEL_HERE")

# Get the onboarding message payload
message = dad_joke.get_message_payload()

# Post the onboarding message in Slack
slack_web_client.chat_postMessage(**message)
```

Before you can run this file you will need to export your Slack token that you saved in part one as an environment variable. 

```command
export SLACK_TOKEN="xbob-SOMETOKENSTUFF"
```

You can test this file and verify that the payload is produced and sent by running the following script in your terminal. Make sure that your virtual environment is activated. You can verify this by seeing the `(slackbot)` text at the front of your bash prompt. Once you run this command you should get a message from your Slackbot with a _hilarious_ dad joke.

```command
python dadbot_test.py
```

Check the channel that you installed your app into and verify that your bot did indeed send a joke. It will not be the exact same joke as this. 

![DadJoke Test](https://i.imgur.com/Rp9Cu0P.png)

Now that your Slackbot has been verified to create jokes and deliver them, lets create a [Flask](https://flask.palletsprojects.com/en/1.1.x/) to perpetually run this app and make it send a dad joke when it sees certain text in messages sent in the channel.

## Step 5 — Creating a Flask Application to Run Our Slackbot

Now that we have a functioning application that can send messages to our slack workspace, we need to create a long running process so our bot can listen to messages sent in the channel and reply to them if the text meets certain criteria. We're going to use the Python web framework [Flask](https://flask.palletsprojects.com/en/1.1.x/) to run this process and listen for events in our channel.

<$>[note]
In this section we will be running our Flask application from a server with a public IP address so the Slack API can send us events. If you are running this locally on your personal workstation you will need to forward the port from your personal firewall to the port that will be running on your workstation. These ports can be the same and this tutorial will be setup to use port 3000.
<$>

The first thing we need to do is create the file for our Flask app. Name this file `app.py`

```command
touch app.py
```

Next, open this file in your favorite text editor and add the following import statements. We'll import the following libraries for the following reasons.

* `import os` - So we can access environment variables
* `import logging` - To log the events of the app
* `from flask import Flask` - So we can create a Flask app
* `from slack import WebClient` - So we can send messages via Slack
* `from slackeventsapi import SlackEventAdapter` - So we can receive events from Slack and process them
* `from dadbot import DadBot` - So we can create an instance of our DadBot and generate the message payload.

Append the following lines to `app.py` to import all of the necessary libraries.

```python
import os
import logging
from flask import Flask
from slack import WebClient
from slackeventsapi import SlackEventAdapter
from dadbot import DadBot
```

Now we need to create our Flask app and register a Slack Event Adapter to our Slack app at the `/slack/events` endpoint. This will create a route in our Slack app where Slack events will be sent and ingested. To do this we will need to get another token from our slack app, which we will do later in the tutorial. Once we get this variable we will export it as an environment variable named *SLACK_EVENTS_TOKEN*. We'll go ahead and write our code to read it in when creating the `SlackEventAdapter` even though we haven't set it yet.

Append the following lines to `app.py` to create the Flask app and register the events adapter into this app.
```python
# Initialize a Flask app to host the events adapter
app = Flask(__name__)

# Create an events adapter and register it to an endpoint in the slack app for event injestion.
slack_events_adapter = SlackEventAdapter(os.environ.get("SLACK_EVENTS_TOKEN"), "/slack/events", app)
```

Next we need to create a web client object that will allow our app to perform actions in the workspace, specifically to send messages. This is similar to what we did when we tested our `DadBot.py` file previously. 

Append the following line to `app.py` to create this slack_web_client.
```python
# Initialize a Web API client
slack_web_client = WebClient(token=os.environ.get("SLACK_TOKEN"))
```

Next we need to create a function that can be called that will create an instance of DadBot, use this instance to create a message payload and pass the message payload to the slack web client for delivery. This function will take in a single parameter, channel, that will specify which channel to send the message too.

Append the following lines to `app.py` to create the function mentioned above.
```python
def tell_joke(channel):
    """Craft the DadJoke and send the message to the channel
    """
    # Get a new dad joke
    dad_joke = DadBot(channel)

    # Get the onboarding message payload
    message = dad_joke.get_message_payload()

    # Post the onboarding message in Slack
    slack_web_client.chat_postMessage(**message)
```

Now that we have created a function to handle the messaging aspects of our app, we need to create one that monitors Slack events for a certain action and then executes our bot. We're going to configure our app to respond with a dad joke when it sees the phrase "Hey Sammy, Tell me a joke". We're going to accept any version of this, case and appended punctuation won't prevent the app from telling a joke. 

First we need to decorate our function with the `@slack_events_adapter.on` syntax that allows our function to receive events. We'll specify that we only want the `message` events and have our function accept a payload parameter containing all of the necessary Slack information. Once we have this payload we will parse out the text, analyze it, and if we see the activation phrase we'll have our app send a dad joke. 

Append the following code to `app.py` to receive, analyze, and act on incoming messages.
```python
# When a 'message' event is detected by the events adapter, forward that payload
# to this function.
@slack_events_adapter.on("message")
def message(payload):
    """Parse the message event, and if the activation string is in the text, 
    send a dad joke
    """

    # Get the event data from the payload
    event = payload.get("event", {})

    # Get the text from the event that came through
    text = event.get("text")

    # Check and see if the activation phrase was in the text of the message.
    # If so, execute the code to send the dad joke.
    if "hey sammy, tell me a joke" in text.lower():
        # Since the activation phrase was met, get the channel ID that the event
        # was executed on
        channel_id = event.get("channel")

        # Execute the tell_joke function and send a dad joke to the channel
        return tell_joke(channel_id)
```

Finally, we need to create a `main` section that will create a logger so we can see the internals of our application as well as lauch the app on our external IP address on port 3000. In order to injest the events from Slack, such as when a new message is sent, we must test our application on a public facing IP address.

Append the following lines to `app.py` to setup our main section.
```python
if __name__ == "__main__":
    # Create the logging object
    logger = logging.getLogger()

    # Set the log level to DEBUG. This will increase verbosity of logging messages
    logger.setLevel(logging.DEBUG)

    # Add the StreamHandler as a logging handler
    logger.addHandler(logging.StreamHandler())

    # Run our app on our externally facing IP address on port 3000 instead of
    # running it on localhost, which is traditional for development.
    app.run(host='0.0.0.0', port=3000)
```

We are now finished with the Flask and it is ready for testing. Before we move on verify that your finished file, `app.py` contains the following:

```python
import os
import logging
from flask import Flask
from slack import WebClient
from slackeventsapi import SlackEventAdapter
from dadbot import DadBot

# Initialize a Flask app to host the events adapter
app = Flask(__name__)
# Create an events adapter and register it to an endpoint in the slack app for event injestion.
slack_events_adapter = SlackEventAdapter(os.environ.get("SLACK_EVENTS_TOKEN"), "/slack/events", app)

# Initialize a Web API client
slack_web_client = WebClient(token=os.environ.get("SLACK_TOKEN"))

def tell_joke(channel):
    """Craft the DadJoke and send the message to the channel
    """
    # Get a new dad joke
    dad_joke = DadBot(channel)

    # Get the onboarding message payload
    message = dad_joke.get_message_payload()

    # Post the onboarding message in Slack
    slack_web_client.chat_postMessage(**message)


# When a 'message' event is detected by the events adapter, forward that payload
# to this function.
@slack_events_adapter.on("message")
def message(payload):
    """Parse the message event, and if the activation string is in the text, 
    send a dad joke
    """

    # Get the event data from the payload
    event = payload.get("event", {})

    # Get the text from the event that came through
    text = event.get("text")

    # Check and see if the activation phrase was in the text of the message.
    # If so, execute the code to send the dad joke.
    if "hey sammy, tell me a joke" in text.lower():
        # Since the activation phrase was met, get the channel ID that the event
        # was executed on
        channel_id = event.get("channel")

        # Execute the tell_joke function and send a dad joke to the channel
        return tell_joke(channel_id)

if __name__ == "__main__":
    # Create the logging object
    logger = logging.getLogger()

    # Set the log level to DEBUG. This will increase verbosity of logging messages
    logger.setLevel(logging.DEBUG)

    # Add the StreamHandler as a logging handler
    logger.addHandler(logging.StreamHandler())

    # Run our app on our externally facing IP address on port 3000 instead of
    # running it on localhost, which is traditional for development.
    app.run(host='0.0.0.0', port=3000)
```

Now that we have our Flask app ready to serve our application let's test it out.

## Step 6 - Running our Flask App

Finally, we can bring everything together and execute our app. 

First, we need to add our running application as an authorized handler for our Slackbot.

Navigate to the **Basic Information** section of your app in the [Slack UI](https://api.slack.com). Scroll down until you find the **App Credentials** section. 

![Slack Signing Secret](https://i.imgur.com/2amAaNk.png)

Copy the **Signing Secret** and export it as the environment variable *SLACK_EVENTS_TOKEN*.

```command
export SLACK_EVENTS_TOKEN="MY_SIGNING_SECRET_TOKEN"
```

With this we have all the necessary API tokens to run our app. Refer to Part 1 if you need a refresher on how to export your *SLACK_TOKEN*. Now we can start our app and verify that it is indeed running. Ensure that your virtual environment is activated and run the following command to start your Flask app.

```command
python3 app.py
```

You should see output similar to below:

```
(slackbot) [20:04:03] sammy:dadbot$ python app.py
 * Serving Flask app "app" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://0.0.0.0:3000/ (Press CTRL+C to quit)
 ```

To verify that our app is up curl the IP address of your server with the correct port at `/slack/events` as shown below:

```command
[15:06:33] sammy $ curl http://YOUR_IP_ADDRESS:3000/slack/events
These are not the slackbots you're looking for.
```

You should receive the message *These are not the slackbots you're looking for.* as a response, indicating that your app is up and running.

We can leave this Flask application running and finish configuring our app in the [Slack UI](https://api.slack.com).

We need to grant our app the appropriate permissions so our app will be able to listen to messages and respond accordingly. 

First, click on **Event Subscriptions** in the UI sidebar and toggle the **Enable Events** radio button. 

![Enable Events Button](https://i.imgur.com/qKT1zph.png)

Once you've done that, type in your IP address, port, and `/slack/events` endpoint into the **Request URL** field. Don't forget the *http* protocol prefix. Slack will make an attempt to connect to your endpoint. Once it has successfully done so you'll see a green check mark with the work **Verified** next to it.

![Event Subscriptions Request URL](https://i.imgur.com/9mtT9gH.png)

Next, we need to expand the **Subscribe to bot events** and add the `message.channels` permission to our app. This will allow our app to receive the messages from our channel and process them.

![Subscribe to bot events permissions](https://i.imgur.com/zX40jCn.png)

Once you've done this you should see the event listed in your **Subscribe to bot events** section. Next click the green **Save Changes** button in the bottom right hand corner.

![Confirm and Save changes](https://i.imgur.com/MeWBib7.png)

Once you do this you'll see a yellow banner across the top of the screen informing you that you'll need to reinstall your app for the following changes to apply. Every time you change permissions you'll have to reinstall your app. Click on the **reinstall your app** link in this banner to reinstall your app.

[Reinstall your app banner](https://i.imgur.com/N0QAj2R.png)

You'll be presented with a confirmation screen summarizing the permissions your bot will have and asking if you want to allow its installation. Click on the green **Allow** button to finish the installation process.

![Reinstall confirmation](https://i.imgur.com/ng0HIKd.png)

Now that you've done this your app should be ready. Go back to the channel that your bot is installed in and send a message containing the phrase *Hey Sammy, Tell me a joke* in it. Your bot should reply with a hilarious dad joke. Congrats! You've created a Slackbot!

![Hey Sammy, Tell me a joke](https://i.imgur.com/15GoRF1.png)

## Step 7 — Deploying the Application for Production
Once you are done developing your application and are ready to move it to production you'll need to deploy it to a server. This will be necessary since the Flask development server is not a secure production environment. You'll be better served if you deploy your app using a *WSGI* and maybe even securing a domain name and giving your server a DNS record. There are many options for deploying Flask applications, some of which are listed below. Follow one of the following articles to deploy your application to a server:

* [Deploy your Flask application to Ubuntu 20.04 using Gunicorn and Nginx](https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-gunicorn-and-nginx-on-ubuntu-20-04)
* [Deploy your Flask application to Ubuntu 20.04 using uWSGI and Nginx](https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-uwsgi-and-nginx-on-ubuntu-20-04)
* [Deploy your Flask Application Using Docker on Ubuntu 18.04](https://www.digitalocean.com/community/tutorials/how-to-build-and-deploy-a-flask-application-using-docker-on-ubuntu-18-04)

There are many more ways to deploy your application than just these. As always when it comes to deployments and infrastucture, do what works best for *you*.

## Conclusion
You now have a Slackbot that tells the best type of jokes, Dad jokes that you can deploy into your slack workspace to amuse your friends. 

You can take this base code and modify it to fit your needs, whether it be automated support, resource management, pictures of cats, or whatever you can think of. You can view the complete Python Slack API docs [here](https://slack.dev/python-slackclient/).