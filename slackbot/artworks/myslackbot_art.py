# This code is based on this article
# https://www.fullstackpython.com/blog/build-first-slack-bot-python.html

import os
import time
from slackclient import SlackClient

import pandas as pd

df_raw = pd.read_csv('https://raw.githubusercontent.com/kmangyo/slack_app/master/slackbot/artworks/text_pic_title_en.csv')

def show(word):
    df=df_raw[df_raw["description"].apply(str).str.contains(word)]
    if len(df)> 0:
        df_r1 = df.sample(n=1)
        return (repr(df_r1['show'].tolist())+"\n"+repr(df_r1['title'].tolist()))
    else:
        df_r2 = df_raw.sample(n=1)
        return ("Sorry... No result. I will give you another artwork\n"+repr(df_r2['show'].tolist())+"\n"+repr(df_r2['title'].tolist()))

# myslackbot's ID as an environment variable
BOT_ID = os.environ.get("BOT_ID")

# constants
AT_BOT = "<@" + BOT_ID + ">"
show_COMMAND = "show"

# instantiate Slack & Twilio clients
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))

def handle_command(command, channel):
    response = "Not sure what you mean. Use the *" + show_COMMAND +"*"
    if command.startswith(show_COMMAND):
        response = show(command[5:len(command)])
    slack_client.api_call("chat.postMessage", channel=channel,
                          text=response, as_user=True)

def parse_slack_output(slack_rtm_output):
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and AT_BOT in output['text']:
                # return text after the @ mention, whitespace removed
                return output['text'].split(AT_BOT)[1].strip().lower(), \
                       output['channel']
    return None, None

if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
    if slack_client.rtm_connect():
        print("StarterBot connected and running!")
        while True:
            command, channel = parse_slack_output(slack_client.rtm_read())
            if command and channel:
                handle_command(command, channel)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")
