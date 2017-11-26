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
import log_utils
import rpc
from constants import DISPATCHER, MODES

from urllib2 import unquote

requests = rpc.Library()
i18n = kodi.i18n


@DISPATCHER.register(MODES.MAIN, kwargs=['content_type'])
def main_route(content_type=''):
    kodi.show_settings()


@DISPATCHER.register(MODES.PLAY, args=['video_type', 'title', 'year'], kwargs=['trakt_id', 'show_id', 'season', 'episode', 'ep_title'])
def play_route(video_type, title, year, trakt_id=None, show_id=None, season=None, episode=None, ep_title=None):
    title = unquote(title)
    if ep_title is not None:
        ep_title = unquote(ep_title)
    file_path = None

    if video_type == 'episode':
        if season and episode:
            tvshow_id = requests.get_tvshow_id(title, year)
            if tvshow_id is not None:
                file_path = requests.find_episode(tvshow_id, season, episode)
            if not file_path:
                str_season = '0' + str(season) if len(season) == 1 else str(season)
                str_episode = '0' + str(episode) if len(episode) == 1 else str(episode)
                label = '%s - S%sE%s' % (title, str_season, str_episode)
                kodi.notify(msg=i18n('not_found_') % label)
    elif video_type == 'movie':
        file_path = requests.find_movie(title, year)
        if not file_path:
            label = '%s (%s)' % (title, str(year))
            kodi.notify(msg=i18n('not_found_') % label)

    if file_path:
        play_item = kodi.create_item(file_path, ep_title if ep_title else title, is_playable=True)
        kodi.Player().play(file_path, play_item)


@DISPATCHER.register(MODES.OPEN, args=['video_type', 'title', 'year'], kwargs=['trakt_id', 'show_id', 'season', 'episode', 'ep_title'])
def open_route(video_type, title, year, trakt_id=None, show_id=None, season=None, episode=None, ep_title=None):
    if (video_type != 'episode') and (video_type != 'movie'):
        title = unquote(title)
        if ep_title is not None:
            ep_title = unquote(ep_title)

    if video_type == 'episode':
        play_route(video_type, title, year, trakt_id, show_id, season, episode, ep_title)
    elif video_type == 'movie':
        play_route(video_type, title, year, trakt_id, show_id, season, episode, ep_title)
    elif video_type == 'season':
        if season:
            tvshow_id = requests.get_tvshow_id(title, year)
            season_exists = False
            if tvshow_id is not None:
                season_exists = requests.season_exists(tvshow_id, season)
                if season_exists:
                    kodi.execute_builtin('ActivateWindow(Videos,videodb://tvshows/titles/%s/%s/?tvshowid=%s)' % (str(tvshow_id), str(season), str(tvshow_id)))
            if not season_exists:
                str_season = '0' + str(season) if len(season) == 1 else str(season)
                label = '%s - S%s' % (title, str_season)
                kodi.notify(msg=i18n('not_found_') % label)

    elif video_type == 'show':
        tvshow_id = requests.get_tvshow_id(title, year)
        if tvshow_id is not None:
            kodi.execute_builtin('ActivateWindow(Videos,videodb://tvshows/titles/%s/)' % str(tvshow_id))
        else:
            label = '%s (%s)' % (title, str(year))
            kodi.notify(msg=i18n('not_found_') % label)
