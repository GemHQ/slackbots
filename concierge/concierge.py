from random import randrange
from time import sleep
from pprint import pprint as pp
from pprint import pformat as pf

from slackclient import SlackClient

from config import *

def main():
    sc = SlackClient(API_KEY)
    if not sc.rtm_connect():
        print "connection failed"
        return False

    while True:
        #loop through rtm and check if a new user
        for m in [m for m in sc.rtm_read() if is_new_user(m)]:
            # open up a direct message
            # send greeting
            # get the language response
            #send appropriate snippet

            if you_talkin_to_me(m):
        sleep(2)


def process_message(m):
    try:
        raise
    except Exception as e:
        reply = USAGE
    return reply


def is_new_user(message):
    return 'type' in message 
        and message['type'] == 'team_join' 
        and message['is_bot'] == False


def you_talkin_to_me(message):
    try:
        return message['text'][0:5] in ['adhoc', '@adho', 'ringo', '@ring']
    except:
        return False
