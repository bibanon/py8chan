#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 8chan URL generator. Inherit and override this for derivative classes  (e.g. 420chan API, 8chan/vichan API)
class Url(object):
    # default value for board in case user wants to query board list
    def __init__(self, board, https=False):
        self._board = board
        self._protocol = 'https://' if https else 'http://'
        self._site_url = "8ch.net"
        
        # Examples
        # Site - http://8ch.net/
        # Board (HTML) - http://8ch.net/newspaper/
        # Thread (HTML) - http://8ch.net/newspaper/res/30.html
        # Thread (JSON) - http://8ch.net/newspaper/res/30.html
        #
        # Page (JSON) - http://8ch.net/newspaper/1.json
        # List (JSON) - http://8ch.net/newspaper/threads.json
        # Catalog (JSON) - http://8ch.net/newspaper/catalog.json
        #
        # Image (old) - https://8ch.net/newspaper/src/1421068790600.jpg
        # Thumb (old) - https://8ch.net/newspaper/thumb/1421068790600.jpg
        # Image (new) - https://media.8ch.net/file_store/bf2f563fe4394ee60e5288b1193c87e40c54f3fb57894db3b141b88b9e79ca7c.jpg
        # Thumb (new) - https://media.8ch.net/file_store/thumb/bf2f563fe4394ee60e5288b1193c87e40c54f3fb57894db3b141b88b9e79ca7c.jpg
        #
        # Static - http://8ch.net/static/blank.gif
        
        # API URL Subdomains
        DOMAIN = {
            'api': self._protocol + self._site_url,   # API subdomain
            'boards': self._protocol + self._site_url, # HTML subdomain
            'file': self._protocol + "media." + self._site_url,  # file (image) host
            'static': self._protocol + self._site_url + "/static" # static host
        }
        
        # API URL Templates
        TEMPLATE = {
            'api': {  # URL structure templates
                'board': DOMAIN['api'] + '/{board}/{page}.json',
                'thread': DOMAIN['api'] + '/{board}/res/{thread_id}.json'
            },
            'http': { # Standard HTTP viewing URLs
                'board': DOMAIN['boards'] + '/{board}/{page}.html',
                'thread': DOMAIN['boards'] + '/{board}/res/{thread_id}.html'
            },
            'data': {
                'file': DOMAIN['file'] + '/file_store/{tim}{ext}',
                'thumbs': DOMAIN['file'] + '/file_store/thumb/{tim}{ext}',
                'old_file': DOMAIN['file'] + '/{board}/src/{tim}{ext}',
                'old_thumbs': DOMAIN['file'] + '/{board}/thumb/{tim}.jpg',
                'static': DOMAIN['static'] + '/{item}'
            }
        }
        
        # API Listings
        LISTING = {
            'board_list': DOMAIN['api'] + '/boards.json',
            'thread_list': DOMAIN['api'] + '/{board}/threads.json',
            'archived_thread_list': None,          # not used by 8chan/vichan
            'catalog': DOMAIN['api'] + '/{board}/catalog.json'
        }
        
        # combine all dictionaries into self.URL dictionary
        self.URL = TEMPLATE
        self.URL.update({'domain': DOMAIN})
        self.URL.update({'listing': LISTING})
    
    # generate boards listing URL
    def board_list(self):
        return self.URL['listing']['board_list']
    
    # generate board page URL
    def page_url(self, page):
        return self.URL['api']['board'].format(
            board=self._board,
            page=page
            )
    
    # generate catalog URL
    def catalog(self):
        return self.URL['listing']['catalog'].format(
            board=self._board
            )
    
    # generate threads listing URL
    def thread_list(self):
        return self.URL['listing']['thread_list'].format(
            board=self._board
            )
    
    # 8chan/vichan does not implement archives as far as we know.
    # must be enabled when BASC_py4chan begins to use this feature,
    # Maybe raise an AttributeError? Maybe set URL class to properties?
    #	def archived_thread_list():
    #		return None
    
    # generate API thread URL
    def thread_api_url(self, thread_id):
        return self.URL['api']['thread'].format(
            board=self._board,
            thread_id=thread_id
            )
    
    # generate HTTP thread URL
    def thread_url(self, thread_id):
        return self.URL['http']['thread'].format(
            board=self._board,
            thread_id=thread_id
            )
    
    # generate file URL
    def file_url(self, tim, ext):
        # new or old file URL
        if len(tim) == 64:
            return self.URL['data']['file'].format(
                tim=tim,
                ext=ext
                )
        else:
            return self.URL['data']['old_file'].format(
                board=self._board,
                tim=tim,
                ext=ext
                )

    # generate thumb URL
    def thumb_url(self, tim, ext):
        # new or old file URL
        if len(tim) == 64:
            # PNGs are not converted to JPGs
            thumb_ext = '.jpg'
            if ext == '.png':
                thumb_ext = '.png'

            return self.URL['data']['thumbs'].format(
                tim=tim,
                ext=thumb_ext
                )
        else:
            return self.URL['data']['old_thumbs'].format(
                board=self._board,
                tim=tim
                )
    
    # return entire URL dictionary
    @property
    def site_urls(self):
        return self.URL

"""
# 4chan Static Data (Unique to 4chan, needs implementation)
STATIC = {
    'flags': DOMAIN['static'] + '/image/country/{country}.gif',
    'pol_flags': DOMAIN['static'] + '/image/country/troll/{country}.gif',
    'spoiler': { # all known custom spoiler images, just fyi
        'default': DOMAIN['static'] + '/image/spoiler.png',
        'a': DOMAIN['static'] + '/image/spoiler-a.png',
        'co': DOMAIN['static'] + '/image/spoiler-co.png',
        'mlp': DOMAIN['static'] + '/image/spoiler-mlp.png',
        'tg': DOMAIN['static'] + '/image/spoiler-tg.png',
        'tg-alt': DOMAIN['static'] + '/image/spoiler-tg2.png',
        'v': DOMAIN['static'] + '/image/spoiler-v.png',
        'vp': DOMAIN['static'] + '/image/spoiler-vp.png',
        'vr': DOMAIN['static'] + '/image/spoiler-vr.png'
    }
}
"""
