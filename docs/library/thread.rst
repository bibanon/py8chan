:class:`py8chan.Thread` – 8chan Threads
============================================

:class:`py8chan.Thread` allows for standard access to a 8chan thread, including listing all the posts in the thread, information such as whether the thread is locked and stickied, and lists of attached file URLs or thumbnails.

Basic Usage
-----------

.. autoclass:: py8chan.Thread

Methods
-------

    Thread objects are not instantiated directly, but instead through the appropriate :class:`py8chan.Board` methods such as :meth:`py8chan.Board.get_thread`.

    .. automethod:: py8chan.Thread.files

    .. automethod:: py8chan.Thread.thumbs

    .. automethod:: py8chan.Thread.filenames

    .. automethod:: py8chan.Thread.thumbnames

    .. automethod:: py8chan.Thread.update

    .. automethod:: py8chan.Thread.expand
