#! /usr/bin/env python

from sys import argv, path

import requests
from requests_oauthlib import OAuth1

path.insert(0, '.')

from randomchan import random_formatted_tweetable_post


def _tweet(keys, content):
    oauth = OAuth1(*keys)

    response = requests.post('https://api.twitter.com/1.1/statuses/'
                             'update.json', data={
                                 'status': content,
                             }, auth=oauth)

    print response.status_code, response.content


if __name__ == '__main__':
    keys = argv[1:5]
    keys = tuple(unicode(key) for key in keys)

    post = random_formatted_tweetable_post('v')
    post = '{} #4chan #Shit4chanSays'.format(post)

    _tweet(keys, post)
