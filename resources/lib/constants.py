# -*- coding: utf-8 -*-
"""
     
    Copyright (C) 2016 anxdpanic
    
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
    GNU General Public License for more details.
    
    You should have received a copy of the GNU General Public License
    along with this program. If not, see <http://www.gnu.org/licenses/>.
"""

import kodi
from url_dispatcher import URL_Dispatcher


def __enum(**enums):
    return type('Enum', (), enums)


DISPATCHER = URL_Dispatcher()

MODES = __enum(
    MAIN='main',
    PLAY='play',
    OPEN='open'
)

DIRECTORIES = __enum(
    DATA=kodi.translate_path('special://profile/addon_data/%s/' % kodi.get_id())
)

ICONS = __enum(
    ADDON=kodi.translate_path('special://home/addons/{0!s}/icon.png'.format(kodi.get_id()))
)
