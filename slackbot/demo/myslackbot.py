# This code is based on these works
# 1) https://www.fullstackpython.com/blog/build-first-slack-bot-python.html
# 2) http://www.craftplustech.com/blog/?p=1434

import os
import time
from slackclient import SlackClient

import random
import requests
from xml.etree import ElementTree

key='XXXXXX' # Seoul Open API key
url1='http://openAPI.seoul.go.kr:8088/'
url2='/xml/SemaPsgudInfoEng/1/1000/'
url = url1 + key + url2

req = requests.request('GET', url)
tree = ElementTree.fromstring(req.content)

# myslackbot's ID as an environment variable
BOT_ID = os.environ.get("BOT_ID")

# constants
AT_BOT = "<@" + BOT_ID + ">"
do_COMMAND = "do"
pic_COMMAND = "pic"

# instantiate Slack & Twilio clients
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))

def handle_command(command, channel):
    response = "Not sure what you mean. Use the *" + do_COMMAND +" or "+ pic_COMMAND +\
               "* command with numbers, delimited by spaces."
    if command.startswith(do_COMMAND):
        response = unicode('두둠칫 ','utf-8') + command
    elif command.startswith(pic_COMMAND):
        response = tree[random.randint(1,1000)][17].text
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
