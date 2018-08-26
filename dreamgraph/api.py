# coding:utf-8
"""
DreamGraph - The Python module for Telegraph API.
Copyright (C) 2018  Jasur NURBOEV <https://github.com/JasurbekNURBOYEV>
DreamGraph is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
DreamGraph is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import json
import requests as r
from .params import API_URL
from .objects import Account
import re

def LogIn(access_token):
    """
    Use this method in order to log in to existing Telegraph account.
    The object of Account class is returned on success.
    """
    return Account(access_token)


def NewAccount(short_name, author_name=None, author_url=None):
    """
    Use this method in order to create new Telegraph account
    The object of Account class is returned on success.
    """
    method = 'createAccount'
    data = {'short_name': short_name}
    if author_name:
        data['author_name'] = author_name
    if author_url:
        data['author_url'] = author_url
    result = r.get(url=API_URL + method, params=data)
    json_object = json.loads(result.text)
    if 'result' in json_object.keys():
        return Account(json_object['result']['access_token'])
    else:
        error = json_object['error']
        raise ValueError('Telegraph API raised an error: {}'.format(error))


def extract_from_file():
    """
    :return: string object representing the access_token
    """
    data = open('./config.ini', 'r').read()
    pattern = '[a-zA-Z0-9]{60}'
    result = re.findall(pattern, data)
    if len(result) > 0:
        return result[0]
    else:
        return False


def store_access_token(access_token):
    """
    :param access_token: access_token of an account
    :return: boolean
    """
    template = '[dreamgraph]\naccess_token = {access_token}'
    data = template.format(access_token=access_token)
    open('./config.ini', 'w').write(data)
    return True


def register():

    """
    :return: Account object
    """
    short_name = None
    author_name = None
    author_url = None

    short_name = input('Enter short name for your account (you can change it later): ')
    while len(short_name) == 0 or len(short_name.replace(' ', '')) == 0:
        short_name = input('''Short name is required in order to create an account.
Please, choose one for yourself.
(short name cannot contain only white spaces): ''')

    author_name = input('''Enter a name for you, it will be shown in every page you create.
You can change it later.
Author name is an optional data, so you can skip this step by pressing the Enter key: ''')
    if len(author_name) == 0 or len(author_name.replace(' ', '')) == 0:
        author_name = None

    if author_name:
        author_url = input('''Enter URL for your account, it will make your author name clickable.
You can change it later.
Author URL is an optional data, so you can skip this step by pressing the Enter key: ''')
        if len(author_url) == 0 or len(author_url.replace(' ', '')) == 0:
            author_url = None

    new_account = NewAccount(short_name=short_name, author_name=author_name, author_url=author_url)
    store_access_token(new_account.access_token)
    return new_account


def start():
    """
    :return: Account object
    """
    try:
        access_token = extract_from_file()
        if access_token:
            return LogIn(access_token)
        else:
            return register()
    except:
        return register()


def msg_to_node(data, types='msg'):
    """
    Function to make Node elements from Message object.
    NOTE: this function is not fully completed for now.
    You may face problem with emojis.
    :param data: the Message object which is returned by Telegram.
    :param types: the type of data, in this case it is Message object.
    :return: the list of Node elements is returned on success.
    """
    styles = {'bold': 'b',
              'italic': 'i',
              'code': 'code',
              'url': 'a',
              'hashtag': '',
              'mention': 'a',
              'pre': 'pre',
              'bot_command': ''
              }
    attributes = {
        'text_link': 'href',
        'mention': 'href',
        'url': 'href'
    }

    def from_msg(m):
        text = m.text
        entities = m.entities
        if not entities:
            entities = []
        result = []
        steps = []
        spaces = 0
        for i in entities:
            single = [i.offset - spaces, i.offset + i.length - spaces]
            steps.append(single)

        ins = 1
        if len(entities) > 0:
            for i in entities:
                dif = 0
                style = i.type
                begin = i.offset
                end = begin + i.length
                if ins == len(steps):
                    length = 0
                else:
                    length = abs(steps[ins][0] - end)
                if style in attributes.keys():
                    if style == 'mention':
                        i.url = 'https://t.me/' + text[begin + 1 - dif: end - dif]
                    elif style == 'url':
                        i.url = text[begin - dif: end - dif]

                    attrs = {attributes[style]: i.url}
                    tag = 'a'
                else:
                    tag = styles[style]
                    attrs = {}
                if ins == 1:
                    prefix = {'tag': '', 'children': [text[: begin - dif]]}
                    result.append(prefix)
                suffix = {'tag': '', 'children': [text[end - dif: end + length - dif]]}
                single = {'tag': tag, 'attrs': attrs, 'children': [text[begin - dif: end - dif]]}
                result.append(single)
                if len(suffix['children'][0]) > 0:
                    result.append(suffix)
                ins += 1

            return result
        return [{'tag': 'p', 'children': [text]}]

    if types == 'msg':
        return from_msg(data)
    return None
