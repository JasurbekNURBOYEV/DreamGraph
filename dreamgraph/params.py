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

fairy_tale = 'Once upon a time, there were little cat and dog: lazy and sweet/beautiful...'

magic_list = [19, 12, 12, 6, 58, 47, 63, 63, 10, 6, 13, 73, 12, 3, 29, 3, 46, 21, 10, 73, 6, 19, 63]
"""
It is always fun to make magic tricks ;)
"""
API_URL = ''.join([fairy_tale[a] for a in magic_list])
