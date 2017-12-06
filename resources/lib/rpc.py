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
import json


class Library:
    @staticmethod
    def find_movie(title, year, imdb):
        request = {
            'jsonrpc': '2.0',
            'params': {
                'sort': {
                    'method': 'title',
                    'order': 'ascending',
                    'ignorearticle': True
                },
                'filter': {
                    'and': [
                        {'operator': 'contains',
                         'field': 'title',
                         'value': title},
                        {'operator': 'is',
                         'field': 'year',
                         'value': year}
                    ]
                },
                'properties': [
                    'file',
                    'imdbnumber'
                ],
                'limits': {
                    'start': 0,
                    'end': 25
                }
            },
            'method': 'VideoLibrary.GetMovies',
            'id': 'libMovies'
        }
        response = kodi.execute_jsonrpc(request)
        log_utils.log('GetMovies Response |%s|' % json.dumps(response, indent=4))

        result = response.get('result', {})
        movies = result.get('movies', [{'file': None, 'imdbnumber': None}])
        file_path = None
        for movie in movies:
            if imdb == movie.get('imdbnumber', None):
                file_path = movie.get('file', None)
                break

        return file_path

    @staticmethod
    def get_tvshow_id(title, year, imdb):
        request = {
            'jsonrpc': '2.0',
            'params': {
                'sort': {
                    'method': 'title',
                    'order': 'ascending',
                    'ignorearticle': True
                },
                'filter': {
                    'and': [
                        {'operator': 'contains',
                         'field': 'title',
                         'value': title},
                        {'operator': 'is',
                         'field': 'year',
                         'value': year}
                    ]
                },
                'properties': [
                    'imdbnumber'
                ],
                'limits': {
                    'start': 0,
                    'end': 25
                }
            },
            'method': 'VideoLibrary.GetTVShows',
            'id': 'libTVShows'
        }
        response = kodi.execute_jsonrpc(request)
        log_utils.log('GetTVShows Response |%s|' % json.dumps(response, indent=4))

        result = response.get('result', {})
        tvshows = result.get('tvshows', [{'tvshowid': None, 'imdbnumber': None}])
        tvshow_id = None
        for show in tvshows:
            if imdb == show.get('imdbnumber', None):
                tvshow_id = show.get('tvshowid', None)
                break

        return tvshow_id

    @staticmethod
    def season_exists(show_id, season):
        request = {
            'jsonrpc': '2.0',
            'params': {
                'tvshowid': int(show_id),
                'sort': {
                    'method': 'label',
                    'order': 'ascending',
                    'ignorearticle': True
                },
                'properties': [
                    'season'
                ]
            },
            'method': 'VideoLibrary.GetSeasons',
            'id': 'libTVShows'
        }

        response = kodi.execute_jsonrpc(request)
        log_utils.log('GetSeasons Response |%s|' % json.dumps(response, indent=4))

        result = response.get('result', {})
        seasons = result.get('seasons', [])

        exists = False
        for s in seasons:
            if s.get('season') == int(season):
                exists = True
                break

        return exists

    @staticmethod
    def find_episode(show_id, season, episode):
        request = {
            'jsonrpc': '2.0',
            'params': {
                'tvshowid': int(show_id),
                'season': int(season),
                'sort': {
                    'method': 'label',
                    'order': 'ascending',
                    'ignorearticle': True
                },
                'filter': {
                    'operator': 'is',
                    'field': 'episode',
                    'value': str(episode)
                },
                'properties': [
                    'file'
                ],
                'limits': {
                    'start': 0,
                    'end': 1
                }
            },
            'method': 'VideoLibrary.GetEpisodes',
            'id': 'libTVShows'
        }

        response = kodi.execute_jsonrpc(request)
        log_utils.log('GetEpisodes Response |%s|' % json.dumps(response, indent=4))

        result = response.get('result', {})
        episode = result.get('episodes', [{'file': None}])[0]
        file_path = episode.get('file', None)

        return file_path
