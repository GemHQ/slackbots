from random import randrange
from time import sleep
from pprint import pprint as pp
from pprint import pformat as pf

from requests import get
from slackclient import SlackClient

from config import *

def main():
    sc = SlackClient(API_KEY)
    watching = {}
    if not sc.rtm_connect():
        print "connection failed"
        return False

    while True:
        for m in [m for m in sc.rtm_read() if is_message(m)]:
            if you_talkin_to_me(m):
                reply = process_command(m, watching)
                print reply
                if not reply: reply = process_message(m)
                if reply: sc.rtm_send_message(m['channel'], reply)
        poll_watching(watching)
        sleep(2)


def process_command(m, watching):
    try:
        parts = m['text'].split(' ')[1:]
        command = parts[0]
        network, item = parse_network(parts[1])
        print command
        if command == 'watch':
            reply = watch(network, item, m['channel'], watching)
        elif command == 'unwatch':
            reply = unwatch(item, watching)
        elif command in ['txinfo', 'tx', 'address', 'addr', 'info']:
            reply = info(network, item)
        else:
            reply = None
        return reply
    except:
        return None


def watch(network, item, channel, watching):
    try:
        watching[item] = {'channel': channel, 'confs': -1, 'network': network}
    except Exception as e:
        print e
    return confirm()


def unwatch(item, watching):
    if item in watching: del watching[item]
    return confirm()


def process_message(m):
    try:
        raise
    except Exception as e:
        reply = USAGE
    return reply


def is_message(message):
    return 'type' in message and message['type'] == 'message'


def you_talkin_to_me(message):
    try:
        return message['text'][0:5] in ['adhoc', '@adho', 'ringo', '@ring']
    except:
        return False
