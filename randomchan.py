from itertools import ifilter
from itertools import imap
from random import choice
from re import sub

from lxml.html import fromstring
import requests


FRONT_PAGE_TEMPLATE = 'http://api.4chan.org/{}/0.json'
POST_URL_TEMPLATE = 'http://boards.4chan.org/{}/res/{}#p{}'


def _format_element(element):
    '''Return the passed lxml.Element formatted in plain text.'''
    # JESUS CHRIST LXML WHY THE FUCK DO YOU MAKE THIS SO COMPLICATED

    formatted_element = list()

    text = [element.text, element.tail]

    if element.tag == 'br':
        text[0] = u'\n'

    text = ifilter(lambda x: x, text)

    text = u' '.join(text)

    formatted_element.append(text)

    for child in element:
        formatted_child = _format_element(child)

        formatted_element.append(formatted_child)

    formatted_element = u' '.join(formatted_element)
    formatted_element = formatted_element.strip()
    formatted_element = sub(u' +', u' ', formatted_element)

    return formatted_element


def get_posts(board):
    '''Return all posts of the board's front page.'''
    url = FRONT_PAGE_TEMPLATE.format(board)

    response = requests.get(url)

    threads = response.json
    threads = threads['threads']
    threads = imap(lambda x: x['posts'], threads)

    parsed_posts = list()

    for thread in threads:
        op = thread[0]

        for post in thread:
            url = POST_URL_TEMPLATE.format(board, op['no'], post['no'])

            try:
                content = post['com']
            except KeyError:
                content = ''
            else:
                content = fromstring(content)
                content = _format_element(content)

            parsed_posts.append({
                'content': content,
                'url': url,
            })

    return parsed_posts


def get_tweetable_posts(board):
    '''Return all tweetable posts (those whose content is less than 120
    characters) of the board's front page.

    '''
    posts = get_posts(board)

    posts = ifilter(lambda x: x['content'], posts)
    posts = ifilter(lambda x: len(x['content']) < 120, posts)

    return posts


def random_formatted_tweetable_post(board):
    '''Return a random tweetable post of the boards front page, formatted to be
    tweeted.

    '''
    posts = get_tweetable_posts(board)
    posts = map(lambda x: u'{} {}'.format(x['content'], x['url']), posts)

    post = choice(posts)

    return post
