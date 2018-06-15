#coding:utf-8
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
    json_object = json.loads(result.text)
    if 'result' in json_object.keys():
        return Account(json_object['result'])
    else:
        error = json_object['error']
        raise ValueError('Telegraph API raised an error: {}'.format(error))
        
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
