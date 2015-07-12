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

def info(network, item):
    blockrl = 'http://{}.blockr.io/api/v1/tx/raw/{}' if len(item) > 40 else 'http://{}.blockr.io/api/v1/address/info/{}'
    url = blockrl.format(network, item)
    try:
        reply =  '```{}```'.format(pf(get(url).json()))
    except Exception as e:
        print e

    print reply
    return reply

def process_message(m):
    try:
        raise
    except Exception as e:
        reply = USAGE
    return reply


def poll_watching(hashes):
    for h, data in hashes.iteritems():
        print h
        print data
        try:
            r = requests.get('http://{}.blockr.io/api/v1/tx/raw/{}'.format(data['network'], h))
            print r.json()
            if r.json()['data']['tx']['confirmations'] != data['confs']:
                hashes[h]['confs'] = r.json()['data']['tx']['confirmations']
                sc.rtm_send_message(data['channel'], "TX {} has {} confirmations".format(h, hashes[h]['confs']))
        except:
            pass
        sleep(1)


def is_message(message):
    return 'type' in message and message['type'] == 'message'

def you_talkin_to_me(message):
    try:
        return message['text'][0:5] in ['adhoc', '@adho', 'ringo', '@ring']
    except:
        return False


# Parse "[(btc|tbtc):]transaction_hash|address" into (btc, hash|address)
def parse_network(nethash):
    nethash = nethash.split(':')
    if len(nethash) == 1:
        network = 'btc'
        hsh = nethash[0]
    else:
        network = nethash[0]
        hsh = nethash[1]
    return (network, hsh)


def confirm(attitude=None):
    if attitude in ATTITUDES.keys():
        return ATTITUDES[attitude][randrange(0, len(ATTITUDES[attitude]))]
    return CONFS[randrange(0, len(CONFS))]


        # if m['type'] == 'message' and m['user'] == USERS['memmaniac']:
        #     if randrange(10) < 3:
        #         sc.rtm_send_message(m['channel'], "Your time has come.")
        #     for i in range(0, randrange(0,20)):
        #         sc.rtm_send_message(m['channel'], "slothify this")

        # if m['type'] == 'user_typing' and m['user'] == USERS['James'] and randrange(10) == 5:
        #     sc.rtm_send_message(m['channel'], "James is droppin' some knowledge, y'all")
        # if m['user'] == USERS['elitistbot'] and randrange(5) == 1:
        #     sc.rtm_send_message(m['channel'], "Wow. profound.")
