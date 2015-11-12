:class:`py8chan.Post` – 8chan Post
=======================================

:class:`py8chan.Post` allows for standard access to a 8chan post.

Example
-------

Here is a sample application that grabs and prints :class:`py8chan.Thread` and :class:`py8chan.Post` information:

.. code-block:: python

    # credits to Anarov for improved example
    from __future__ import print_function
    import py8chan

    # get the board we want
    board = py8chan.Board('v')

    # select the first thread on the board
    all_thread_ids = board.get_all_thread_ids()
    first_thread_id = all_thread_ids[0]
    thread = board.get_thread(first_thread_id)

    # print thread information
    print(thread)
    print('Sticky?', thread.sticky)
    print('Closed?', thread.closed)
    print('Replies:', len(thread.replies))

    # print topic post information
    topic = thread.topic
    print('Topic Repr', topic)
    print('Postnumber', topic.post_number)
    print('Timestamp', topic.timestamp)
    print('Datetime', repr(topic.datetime))
    print('Filemd5hex', topic.file_md5_hex)
    print('Fileurl', topic.file_url)
    print('Subject', topic.subject)
    print('Comment', topic.comment)
    print('Thumbnailurl', topic.thumbnail_url)

Basic Usage
-----------

.. autoclass:: py8chan.Post

    Post objects are not instantiated directly, but through a :class:`py8chan.Thread` object with an attribute like :attr:`py8chan.Thread.all_posts`.
