:class:`py8chan.Board` – 8chan Boards
==========================================

:class:`py8chan.Board` provides access to a 8chan board including checking if threads exist, retrieving appropriate :class:`py8chan.Thread` objects, and returning lists of all the threads that exist on the given board.

Example
-------

Here is a sample application that grabs and uses Board information::

    from __future__ import print_function
    import py8chan

    board = py8chan.Board('tg')
    thread_ids = board.get_all_thread_ids()
    str_thread_ids = [str(id) for id in thread_ids]  # need to do this so str.join below works
    print('There are', len(all_ids), 'active threads on /tg/:', ', '.join(str_thread_ids))

Basic Usage
-----------

.. autoclass:: py8chan.Board

Methods
-------

    .. automethod:: py8chan.Board.__init__

    .. automethod:: py8chan.Board.thread_exists

    .. automethod:: py8chan.Board.get_thread

    .. automethod:: py8chan.Board.get_threads

    .. automethod:: py8chan.Board.get_all_threads

    .. automethod:: py8chan.Board.get_all_thread_ids

    .. automethod:: py8chan.Board.refresh_cache

    .. automethod:: py8chan.Board.clear_cache
