#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime

from .url import Url
from .util import clean_comment_body
from .file import File


class Post(object):
    """Represents an 8chan post. See the following Swagger definition for more details.
    https://gitlab.com/N3X15/8chan-API/blob/master/definitions/Post.json

    Attributes:
        post_id (int): ID of this post. Eg: ``123123123``, ``456456456``.
        resto (int): Reply to. 0 is a thread OP.
        name (string): Poster's name.
        poster_id (string) Hexadecimal ID used to differentiate between posters.  Only on boards with `poster_ids` set to `true`.
        tripcode (string): Poster's tripcode.
        subject (string): Subject of this post.
        comment (string): This comment, with the <wbr> tag removed.
        html_comment (string): Original, direct HTML of this comment.
        text_comment (string): Plaintext version of this comment.
        is_op (bool): Whether this is the OP (first post of the thread)
        sticky (bool): 1 if post is stickied, 0 if not.
        locked (bool): 1 if post is locked, 0 if not.
        cyclical (bool): 8ch Swagger docs say: "UNKNOWN! FIX ME!"
        bumplocked (string): Presumably 1 if the thread can no longer be bumped, 0 if not.
        timestamp (int): Unix timestamp for this post.
        datetime (:class:`datetime.datetime`): Datetime time of this post.
        first_file (File): The first file of the post.
        all_files (File): Returns the File objects of all files in the post.
        extra_files (File): Returns the File objects of all extra files in the post, if any.
        has_file (bool): Whether this post has a file attached to it.
        has_extra_files (bool): Whether this post has more than one file attached to it.
        url (string): URL of this post.
    """
    def __init__(self, thread, data):
        self._thread = thread
        self._data = data
        self._url = Url(board=self._thread._board.name, https=thread.https)        # 4chan URL generator
        
        # add file objects if they exist
        if self.has_file:
            self.file1 = File(self, self._data)

    @property
    def is_op(self):
        return self == self._thread.topic

    @property
    def post_id(self):
        return self._data.get('no')
    number = num = no = post_number = post_id  # allows post_id to exist as multiple different names

    @property
    def resto(self):
        return self._data.get('resto')

    @property
    def subject(self):
        return self._data.get('sub')

    @property
    def html_comment(self):
        return self._data.get('com', '')

    # TODO: This seems like unessential code. Consider removing
    @property
    def comment(self):
        return self.html_comment.replace('<wbr>', '')

    @property
    def text_comment(self):
        return clean_comment_body(self.html_comment)

    @property
    def name(self):
        return self._data.get('name')

    @property
    def timestamp(self):
        return self._data.get('time')

    @property
    def datetime(self):
        if self._data.get('time') is not None:
            return datetime.fromtimestamp(self._data.get('time'))
        else:
            return None

    @property
    def last_modified(self):
        return self._data.get('last_modified')

    @property
    def poster_id(self):
        return self._data.get('id')

    @property
    def sticky(self):
        return self._data.get('sticky')

    @property
    def locked(self):
        return self._data.get('locked')

    @property
    def cyclical(self):
        return self._data.get('cyclical')

    @property
    def bumplocked(self):
        return self._data.get('bumplocked')

    @property
    def first_file(self):
        if not self.has_file:
            return None
        
        return self.file1

    def all_files(self):
        """Returns the File objects of all files in the post."""
        # append first file if it exists
        if self.has_file:
            yield self.file1
        
        # append extra files if they exist
        if self.has_extra_files:
            for item in self._data['extra_files']:
                yield File(self, item)

    def extra_files(self):
        """Returns the File objects of all extra files in the post, if any."""
        # append extra files if they exist
        if self.has_extra_files:
            for item in self._data['extra_files']:
                yield File(self, item)

    @property
    def has_file(self):
        return 'filename' in self._data

    @property
    def has_extra_files(self):
        if 'extra_files' in self._data:
            return True
        else:
            return False

    @property
    def url(self):
        return '%s#%i' % (self._thread.url, self.post_id)
    
    def __repr__(self):
        return '<Post /%s/%i#%i, has_file: %r, has_extra_files: %r>' % (
            self._thread._board.name,
            self._thread.id,
            self.post_id,
            self.has_file,
            self.has_extra_files
        )
