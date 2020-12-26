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


def store_access_token(access_token):
    """
    :param access_token: access_token of an account
    :return: boolean
    """
    template = '[dreamgraph]\naccess_token = {access_token}'
    data = template.format(access_token=access_token)
    open('./config.ini', 'w').write(data)
    return True


class Account:
    """
    The main class.
    Includes all necessary methods.
    """

    def __init__(self, data):
        method = 'getAccountInfo'
        if type(data) == str:
            request = r.get(url=API_URL + method, params={'access_token': data})
            json_object = json.loads(request.text)
            if 'result' in json_object.keys():
                self.access_token = data
                self.available_methods = [
                    'get_account_info', 'edit_account_info',
                    'revoke_access_token', 'create_page', 'edit_page',
                    'get_page', 'get_page_list', 'get_views'
                ]
            else:
                error = json_object['error']
                raise ValueError("Telegraph API raised an error: {}".format(error))
        else:
            raise ValueError("Please, provide string object, you've just used {} instad of string.".format(type(data)))
        json_object = json_object['result']
        keys = json_object.keys()
        if 'short_name' in keys:
            self.short_name = json_object['short_name'] if json_object['short_name'] != '' else None
        else:
            self.short_name = None
        if 'author_name' in keys:
            self.author_name = json_object['author_name'] if json_object['author_name'] != '' else None
        else:
            self.author_name = None
        if 'author_url' in keys:
            self.author_url = json_object['author_url'] if json_object['author_url'] != '' else None
        else:
            self.author_url = None
        if 'auth_url' in keys:
            self.auth_url = json_object['auth_url'] if json_object['auth_url'] != '' else None
        else:
            self.auth_url = None
        if 'page_count' in keys:
            self.page_count = json_object['page_count'] if json_object['page_count'] != '' else None
        else:
            self.page_count = None

    def edit_account_info(self, short_name=None, author_name=None, author_url=None):
        """
        :param short_name: optional, if not presented, the old one is used.
        :param author_name: optional, the name which is written in telegraph page as the author of the article.
        :param author_url: optional, the link which makes author_name clickable.
        :return: the object of Account class is returned on success.
        """
        method = 'editAccountInfo'
        data = {}
        if short_name:
            data['short_name'] = short_name
            self.short_name = short_name
        if author_name:
            data['author_name'] = author_name
            self.author_name = author_name
        if author_url:
            data['author_url'] = author_url
            self.author_name = author_name
        request = r.get(url=API_URL + method, params=data)
        json_object = json.loads(request.text)
        if 'result' in json_object.keys():
            return Account(json_object['result']['access_token'])
        else:
            error = json_object['error']
            raise ValueError("Telegraph API raised an error: {}".format(error))

    def get_account_info(self):
        """
        :return: the dict including all info about the account is returned on success.
        """
        method = 'getAccountInfo'
        data = {'access_token': self.access_token}
        result = r.get(url=API_URL + method, params=data)
        json_object = json.loads(result.text)
        keys = json_object.keys()
        if 'result' in keys:
            keys = json_object['result'].keys()
            if 'short_name' in keys:
                data['short_name'] = json_object['result']['short_name']
            if 'author_name' in keys:
                data['author_name'] = json_object['result']['author_name']
            if 'author_url' in keys:
                data['author_url'] = json_object['result']['author_url']
            if 'auth_url' in keys:
                data['auth_url'] = json_object['result']['auth_url']
            if 'page_count' in keys:
                data['page_count'] = json_object['result']['page_count']
            return data
        else:
            error = json_object['error']
            raise ValueError("Telegraph API raised an error: {}".format(error))

    def revoke_access_token(self):
        """
        :return: the object of Account class is returned on success.
        """
        method = 'revokeAccessToken'
        request = r.get(url=API_URL + method, params={'access_token': self.access_token})
        json_object = json.loads(request.text)
        if 'result' in json_object.keys():
            self.access_token = json_object['result']['access_token']
            store_access_token(self.access_token)
            return self.access_token
        else:
            error = json_object['error']
            raise ValueError("Telegraph API raised an error: {}".format(error))

    def create_page(self, title=str, content=list, author_name=None, author_url=None, return_content=True):
        """
        :param title: required, title of the article.
        :param content: required, the content of the article: list of Node elements.
        :param author_name: optional, the name which is ritten as the author of the article.
        :param author_url: optional, the link which makes author_name clickable.
        :param return_content: optional, if True, the content of the page is returned. By default it is True.
        :return: the object of Page class is returned on success.
        """
        method = 'createPage'
        data = {
            'access_token': self.access_token, 'title': title, 'content': json.dumps(content),
            'return_content': return_content
        }
        if author_name:
            data['author_name'] = author_name
        if author_url:
            data['author_url'] = author_url
        request = r.post(url=API_URL + method, params=data)
        json_object = json.loads(request.text)
        if 'result' in json_object.keys():
            return Page(json_object['result'])
        else:
            error = json_object['error']
            raise ValueError("Telegraph API raised an error: {}".format(error))

    def edit_page(self, path=str, title=str, content=list, author_name=None, author_url=None, return_content=False):
        """
        :param path: required, path to the article.
        :param title: required, the title of the article.
        :param content: required, the content of the article: Node elements.
        :param author_name: optional, the name which is ritten as the author of the article.
        :param author_url: optional, the link which makes author_name clickable.
        :param return_content: optional, if True, the content of the page is returned. By default it is True.
        :return: the object of Page class is returned on success.
        """
        method = 'editPage'
        data = {
            'access_token': self.access_token,
            'path': path,
            'title': title,
            'content': json.dumps(content),
            'return_content': return_content
        }
        if author_name:
            data['author_name'] = author_name
        if author_url:
            data['author_url'] = author_url
        request = r.get(url=API_URL + method, params=data)
        json_object = json.loads(request.text)
        if 'result' in json_object.keys():
            return Page(json_object['result'])
        else:
            error = json_object['error']
            raise ValueError("Telegraph API raised an error: {}".format(error))

    def get_page(self, path, return_content=True):
        """
        :param path: required, path to the article.
        :param return_content: optional, if True, the content of the page is returned. By default it is True.
        :return: the object of Page class is returned on success.
        """
        method = 'getPage'
        data = {'path': path, 'return_content': return_content}
        request = r.get(url=API_URL + method, params=data)
        json_object = json.loads(request.text)
        if 'result' in json_object.keys():
            return Page(json_object['result'])
        else:
            error = json_object['error']
            raise ValueError("Telegraph API raised an error: {}".format(error))

    def get_page_list(self, offset=0, limit=50):
        """
        :param offset: optional, sequential number of the first page to be returned. By default it is 0.
        :param limit: optional, limits the number of pages to be retrieved. By default it is 50.
        :return: the object of PageList class is returned on success.
        """
        method = 'getPageList'
        data = {'access_token': self.access_token, 'offset': offset, 'limit': limit}
        request = r.get(url=API_URL + method, params=data)
        json_object = json.loads(request.text)
        if 'result' in json_object.keys():
            return PageList(json_object['result'])
        else:
            error = json_object['error']
            raise ValueError("Telegraph API raised an error: {}".format(error))

    def get_views(self, path=str, year=int, month=int, day=int, hour=None):
        """
        :param path: required, path to the article.
        :param year: required if month is passed. If passed, the number of page views for the requested year is returned.
        :param month: required if day is passed. If passed, the number of page views for the requested month is returned.
        :param day: required if hour is passed. If passed, the number of page views for the requested day is returned.
        :param hour: optional, if passed, the number of page views for the requested hour is returned.
        :return: the object of PageViews class is returned on success.
        """
        method = 'getViews'
        data = {'path': path, 'year': year, 'month': month, 'day': day}
        if hour:
            data['hour'] = hour
        request = r.get(url=API_URL + method, params=data)
        json_object = json.loads(request.text)
        if 'result' in json_object.keys():
            return PageViews(json_object['result']['views'])
        else:
            error = json_object['error']
            raise ValueError("Telegraph API raised an error: {}".format(error))


class PageList:
    """
    This class includes only two attributes: total count of articles (total_count)
    and the list of objects of Page class (pages).
    """

    def __init__(self, data):
        self.total_count = data['total_count']
        pages = []
        for i in data['pages']:
            pages.append(Page(i))
        self.pages = pages

    def __new__(cls, data=dict):
        cls.total_count = data['total_count']
        pages = []
        for i in data['pages']:
            pages.append(Page(i))
        cls.pages = pages
        return cls


class Page:
    """
    This class is one of the main classes.
    It represents all necessary attributes of the article.
    """

    def __init__(self, data=dict):
        """
        :param data: required, the data which is returned by Telegraph API
        """
        keys = data.keys()
        self.path = data['path']
        self.url = data['url']
        self.title = data['title']
        self.description = data['description']
        self.author_name = data['author_name'] if 'author_name' in keys else None
        self.image_url = data['image_url'] if 'image_url' in keys else None
        self.author_url = data['author_url'] if 'author_url' in keys else None
        self.content = data['content'] if 'content' in keys else None
        self.views = data['views'] if 'views' in keys else None
        self.can_edit = data['can_edit'] if 'can_edit' in keys else False

    def __new__(cls, data=dict):
        """
        :param data: required, the data which is returned by Telegraph API.
        :return: the object of current class is returned.
        """
        keys = data.keys()
        cls.path = data['path']
        cls.url = data['url']
        cls.title = data['title']
        cls.description = data['description']
        cls.author_name = data['author_name'] if 'author_name' in keys else None
        cls.image_url = data['image_url'] if 'image_url' in keys else None
        cls.author_url = data['author_url'] if 'author_url' in keys else None
        cls.content = data['content'] if 'content' in keys else None
        cls.views = data['views'] if 'views' in keys else None
        cls.can_edit = data['can_edit'] if 'can_edit' in keys else False
        return cls


class PageViews:
    """
    This class has only one attribute: number of views for the page (views).
    """

    def __init__(self, views):
        """
        :param views: required, number of views for the page (views).
        """
        self.views = views

    def __new__(cls, views):
        cls.views = views
        return cls
