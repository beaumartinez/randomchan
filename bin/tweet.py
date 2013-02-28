#! /usr/bin/env python

from sys import path

import requests
from requests.auth import OAuth1

path.insert(0, '.')

from randomchan import random_formatted_tweetable_post


def _tweet(content):
    client_key = u'El04Ou8ZJPhBtmJeCf2KA'
    client_secret = u'iiLjxG0cpf9TL7lyJEeuQOxm87fUWnMwzpXxjLEK8E'
    resource_owner_key = u'968749950-251WsvFviXmcob2qg6LRkxybRjlBrlwuYEHga3Eq'
    resource_owner_secret = u'Vzn0guHbJKiIPjaGvy3UOdebPnanVP79080rfWK2TI'

    oauth = OAuth1(client_key, client_secret, resource_owner_key,
                   resource_owner_secret, signature_type='auth_header')

    response = requests.post('https://api.twitter.com/1.1/statuses/'
                             'update.json', data={
                                 'status': content,
                             }, auth=oauth)

    print response.status_code, response.content


if __name__ == '__main__':
    post = random_formatted_tweetable_post('v')
    _tweet(post)
