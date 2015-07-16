from random import randrange
from time import sleep
from pprint import pprint as pp
from pprint import pformat as pf
import json

from slackclient import SlackClient

from config import *

def main():
    sc = SlackClient(API_KEY)
    if not sc.rtm_connect():
        print "connection failed"
        return False

    new_users = {}

    while True:
        #loop through rtm and check if a new user
        for m in [m for m in sc.rtm_read() if is_new_user(m)]:
            # open up a direct message
            channel_id = open_direct_message(m, sc)
            # send greeting
            send_greeting(sc, channel_id)
            # get the language response
            if is_message(m) and you_talkin_to_me(m):
                snippet_language = get_language_response(m)
            #send appropriate snippet
            send_snippet(sc, channel_id, snippet_language)
        sleep(2)

def send_message(sc, channel_id, text):
    sc.api_call('chat.postMessage',
                channel=channel_id,
                text = text,
                as_user = True)


def send_greeting(sc, channel_id):
    send_message(sc, channel_id, GREETING)


def send_snippet(sc, channel_id, language):
    send_message(sc, channel_id, format_snippet(language))


def format_snippet(language):
    message = '```'
    for k, v in SNIPPETS[language].iteritems():
        message = message + k, + v + '\n'
    message = message + '```'

    return message

    

def open_direct_message(message, sc):
    user_id = message['user']['id']
    chat = json.loads(sc.api_call("im.open", user = user_id))
    chat_id = chat['channel']['id']
    new_users[user_id] = chat_id
    return chat_id


def is_new_user(message):
    return 'type' in message 
        and message['type'] == 'team_join' 
        and message['user']['is_bot'] == False


def get_language_response(message):
    try:
        for l in SNIPPETS.keys():
            if l in message['text']:
                return l
    except:
        return "We don't have that language yet"



def is_message(message):
    return 'type' in message and message['type'] == 'message'


def you_talkin_to_me(message):
    try:
        return message['channel'] == channel_id 
            and message['text'][2:phrase.find('>')] == CONCIERGE_ID
    except:
        return False