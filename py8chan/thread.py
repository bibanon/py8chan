#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .post import Post
from .url import Url


class Thread(object):
    """Represents a thread.

    Attributes:
        closed (bool): Whether the thread has been closed.
        sticky (bool): Whether this thread is a 'sticky'.
        topic (:class:`py8chan.Post`): Topic post of the thread, the OP.
        posts (list of :class:`py8chan.Post`): List of all posts in the thread, including the OP.
        all_posts (list of :class:`py8chan.Post`): List of all posts in the thread, including the OP and any omitted posts.
        url (string): URL of the thread, not including semantic slug.
        
	Undefined Attributes (Not implemented in 8chan API. Do not use.):
        replies and images: Infuriatingly, the OP post in a thread
        doesn't list how many replies there are in a thread.
        semantic_url (string): URL of this post, with the thread's 'semantic' component.
        semantic_slug (string): This post's 'semantic slug'.
    """
    def __init__(self, board, id):
        self._board = board
        self._url = Url(board=board.name, https=board.https)       # 8chan URL generator
        self.id = self.number = self.num = self.no = id
        self.topic = None
        self.replies = []
        self.is_404 = False
        self.last_reply_id = 0
        self.omitted_posts = 0
        self.omitted_images = 0
        self.want_update = False

    def __len__(self):
        return self.num_replies

    @property
    def _api_url(self):
        return self._url.thread_api_url(self.id)

    @property
    def closed(self):
        return self.topic._data.get('closed') == 1

    @property
    def sticky(self):
        return self.topic._data.get('sticky') == 1

    # 8chan puts last modified in JSON instead of the HTTP header
    @property
    def _last_modified(self):
        return self.topic._data.get('last-modified')

    @classmethod
    def _from_request(cls, board, res, id):
        if res.status_code == 404:
            return None

        res.raise_for_status()

        return cls._from_json(res.json(), board, id)

    @classmethod
    def _from_json(cls, json, board, id=None):
        t = cls(board, id)

        posts = json['posts']
        head, rest = posts[0], posts[1:]

        t.topic = t.op = Post(t, head)
        t.replies.extend(Post(t, p) for p in rest)

        t.id = head.get('no', id)
        t.num_replies = len(posts) - 1	# There's no "replies" item in OP on 8ch!
        t.num_images = 0				# There's no "images" item in OP on 8ch!
        t.omitted_images = head.get('omitted_images', 0)
        t.omitted_posts = head.get('omitted_posts', 0)

        if id is not None:
            if not t.replies:
                t.last_reply_id = t.topic.post_id
            else:
                t.last_reply_id = t.replies[-1].post_id

        else:
            t.want_update = True

        return t

    def files(self):
        """Returns the URLs of all files attached to posts in the thread."""
        # yield all from the topic
        if self.topic.has_file:
            for item in self.topic.all_files():
                yield item.file_url

        # yield all from other posts
        for reply in self.replies:
            if reply.has_file:
                for item in reply.all_files():
                    yield item.file_url

    def thumbs(self):
        """Returns the URLs of all thumbnails in the thread."""
        # yield all from the topic
        if self.topic.has_file:
            for item in self.topic.all_files():
                yield item.thumbnail_url

        # yield all from other posts
        for reply in self.replies:
            if reply.has_file:
                for item in reply.all_files():
                    yield item.thumbnail_url

    def filenames(self):
        """Returns the filenames of all files attached to posts in the thread."""
        # yield all from the topic
        if self.topic.has_file:
            for item in self.topic.all_files():
                yield item.filename

        # yield all from other posts
        for reply in self.replies:
            if reply.has_file:
                for item in reply.all_files():
                    yield item.filename

    def thumbnames(self):
        """Returns the filenames of all thumbnails in the thread."""
        # yield all from the topic
        if self.topic.has_file:
            for item in self.topic.all_files():
                yield item.thumbnail_fname

        # yield all from other posts
        for reply in self.replies:
            if reply.has_file:
                for item in reply.all_files():
                    yield item.thumbnail_fname

    def file_objects(self):
        """Returns the :class:`py8chan.File` objects of all files attached to posts in the thread."""
        # yield all from the topic
        if self.topic.has_file:
            for item in self.topic.all_files():
                yield item

        # yield all from other posts
        for reply in self.replies:
            if reply.has_file:
                for item in reply.all_files():
                    yield item

    def update(self, force=False):
        """Fetch new posts from the server.

        Arguments:
            force (bool): Force a thread update, even if thread has 404'd.

        Returns:
            int: How many new posts have been fetched.
        """

        # The thread has already 404'ed, this function shouldn't do anything anymore.
        if self.is_404 and not force:
            return 0

        if self._last_modified:
            headers = {'If-Modified-Since': self._last_modified}
        else:
            headers = None

        # random connection errors, just return 0 and try again later
        try:
            res = self._board._requests_session.get(self._api_url, headers=headers)
        except:
            # try again later
            return 0

        # 304 Not Modified, no new posts.
        if res.status_code == 304:
            return 0

        # 404 Not Found, thread died.
        elif res.status_code == 404:
            self.is_404 = True
            # remove post from cache, because it's gone.
            self._board._thread_cache.pop(self.id, None)
            return 0

        elif res.status_code == 200:
            # If we somehow 404'ed, we should put ourself back in the cache.
            if self.is_404:
                self.is_404 = False
                self._board._thread_cache[self.id] = self

            # Remove
            self.want_update = False
            self.omitted_images = 0
            self.omitted_posts = 0

            posts = res.json()['posts']

            original_post_count = len(self.replies)
            self.topic = Post(self, posts[0])

            if self.last_reply_id and not force:
                self.replies.extend(Post(self, p) for p in posts if p['no'] > self.last_reply_id)
            else:
                self.replies[:] = [Post(self, p) for p in posts[1:]]

            new_post_count = len(self.replies)
            post_count_delta = new_post_count - original_post_count
            if not post_count_delta:
                return 0

            self.last_reply_id = self.replies[-1].post_id

            return post_count_delta

        else:
            res.raise_for_status()

    def expand(self):
        """If there are omitted posts, update to include all posts."""
        if self.omitted_posts > 0:
            self.update()

    @property
    def posts(self):
        return [self.topic] + self.replies

    @property
    def all_posts(self):
        self.expand()
        return self.posts

    @property
    def https(self):
        return self._board._https

    @property
    def url(self):
        return self._url.thread_url(self.id)

    # 8chan/vichan does not use semantic urls
    @property
    def semantic_url(self):
        raise AttributeError( "'py8chan.Thread' object has no attribute 'semantic_url'" )
    
    # 8chan/vichan does not use semantic slugs
    @property
    def semantic_slug(self):
        raise AttributeError( "'py8chan.Thread' object has no attribute 'semantic_slug'" )

    def __repr__(self):
        extra = ''
        if self.omitted_images or self.omitted_posts:
            extra = ', %i omitted images, %i omitted posts' % (
                self.omitted_images, self.omitted_posts
            )

        return f'<Thread {self._board.name}, {self.id}  replies {len(self.replies)}>'
