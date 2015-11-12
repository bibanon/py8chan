Tutorial
========

When using py8chan, it can be a bit hard to find where to begin. Here, we run through how to create and use the various objects available in this module.


Boards
------
:mod:`py8chan.Board` is the first thing you create when using py8chan. Everything else is created through that class. The most basic way to create a board is as below::

    board = py8chan.Board('v')

This creates a :mod:`py8chan.Board` object that you can then use to create :mod:`py8chan.Thread` and :mod:`py8chan.Post` objects.

But what sort of things does a :mod:`py8chan.Board` object let you do?

Here's a short code snippet of us printing out how many threads are active on a board::

    board = py8chan.Board('v')
    thread_ids = board.get_all_thread_ids()
    str_thread_ids = [str(id) for id in thread_ids]  # need to do this so str.join below works
    print('There are', len(all_ids), 'active threads on /tg/:', ', '.join(str_thread_ids))


Threads
-------
Listing how many threads exist on a board is all well and good, but most people want to actually get threads and do things with them. Here, we'll describe how to do that.

All :mod:`py8chan.Thread` objects are created by a :mod:`py8chan.Board` object, using one of the :meth:`py8chan.Board.get_thread` methods.

For this example, we have a user ask us about "thread 1234", and we return information about it::

    thread_id = 1234
    board = py8chan.Board('v')

    if board.thread_exists(thread_id):
        thread = board.get_thread(thread_id)

        # print thread information
        print('Thread', thread_id)
        if thread.closed:
            print('  is closed')
        if thread.sticky
            print('  is a sticky')

        # information from the OP
        topic = thread.topic
        print('  is named:', topic.subject)
        print('  and was made by:', name, email)
