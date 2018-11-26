#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime

from .url import Url
from .util import clean_comment_body
from .file import File


class Post(object):
    """Represents a 4chan post.

    Attributes:
        post_id (int): ID of this post. Eg: ``123123123``, ``456456456``.
        poster_id (int): Poster ID.
        name (string): Poster's name.
        email (string): Poster's email.
        tripcode (string): Poster's tripcode.
        subject (string): Subject of this post.
        comment (string): This comment, with the <wbr> tag removed.
        html_comment (string): Original, direct HTML of this comment.
        text_comment (string): Plaintext version of this comment.
        is_op (bool): Whether this is the OP (first post of the thread)
        timestamp (int): Unix timestamp for this post.
        datetime (:class:`datetime.datetime`): Datetime time of this post.
        first_file (File): The first file of the post.
        all_files (File): Returns the File objects of all files in the post.
        extra_files (File): Returns the File objects of all extra files in the post, if any.
        has_file (bool): Whether this post has a file attached to it.
        has_extra_files (bool): Whether this post has more than one file attached to it.
        url (string): URL of this post.
    
    Undefined Attributes (Not implemented in 8chan API. Do not use.): 
        poster_id (int): Poster ID.
        file_deleted (bool): Whether the file attached to this post was deleted after being posted.
        semantic_url (string): URL of this post, with the thread's 'semantic' component.
        semantic_slug (string): This post's 'semantic slug'.
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
    number = num = no = post_number = post_id

    # (May Change) 8chan/vichan does not use administrative IDs
    @property
    def poster_id(self):
        raise AttributeError( "'py8chan.Post' object has no attribute 'poster_id'" )

    @property
    def name(self):
        return self._data.get('name')

    @property
    def email(self):
        return self._data.get('email')

    @property
    def tripcode(self):
        return self._data.get('trip')

    @property
    def subject(self):
        return self._data.get('sub')

    @property
    def html_comment(self):
        return self._data.get('com', '')

    @property
    def text_comment(self):
        return clean_comment_body(self.html_comment)

    @property
    def comment(self):
        return self.html_comment.replace('<wbr>', '')

    @property
    def timestamp(self):
        return self._data['time']

    @property
    def datetime(self):
        return datetime.fromtimestamp(self._data['time'])

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
        return '%s#p%i' % (self._thread.url, self.post_number)
    
    # 8chan/vichan does not use semantic urls
    @property
    def semantic_url(self):
        raise AttributeError( "'py8chan.Post' object has no attribute 'semantic_url'" )
    
    # 8chan/vichan does not use semantic slugs
    @property
    def semantic_slug(self):
        raise AttributeError( "'py8chan.Post' object has no attribute 'semantic_slug'" )

    def __repr__(self):
        return '<Post /%s/%i#%i, has_file: %r, has_extra_files: %r>' % (
            self._thread._board.name,
            self._thread.id,
            self.post_number,
            self.has_file,
            self.has_extra_files
        )
