#coding:utf8
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
    result = json.loads(result.text)
    return Account(result['result'])


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
              'url': ''
              }
    attributes = {
        'text_link': 'src',
    }

    def from_msg(m):
        text = m['message']['text']
        entities = m['message']
        if 'entities' in entities.keys():
            entities = entities['entities']
        else:
            entities = []
        result = []
        steps = []
        for i in entities:
            single = [i['offset'], i['offset'] + i['length']]
            steps.append(single)
        ins = 1
        if len(entities) > 0:
            for i in entities:
                style = i['type']
                begin = i['offset']
                end = begin + i['length']
                if ins == len(steps):
                    length = 0
                else:
                    length = abs(steps[ins][0] - end)
                if style in attributes.keys():
                    attrs = {attributes[style]: i['url']}
                    tag = ''
                else:
                    tag = styles[style]
                    attrs = {}
                single = {'tag': tag, 'attrs': attrs, 'children': [text[begin:end] + ' ' * length]}
                result.append(single)
                ins += 1
            ending = {'tag': 'p', 'children': [text[steps[-1][1]:]]}
            result.append(ending)
            result = result[::-1]
            result.append(text[:steps[0][0]])
            return result[::-1]
        return [{'tag': 'p', 'children': [text]}]

    if types == 'msg':
        return from_msg(data)
    return None
