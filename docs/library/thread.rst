:class:`basc_py4chan.Thread` – Access to 4chan Boards
==================================================

:class:`basc_py4chan.Thread` allows for standard access to a 4chan thread, including listing all the posts in the thread, information such as whether the thread is locked and stickied, and lists of attached file URLs or thumbnails.


.. autoclass:: basc_py4chan.Thread

    Thread objects are not instantiated directly, but instead through the appropriate :class:`basc_py4chan.Board` methods such as :meth:`basc_py4chan.Board.get_thread`.

    .. automethod:: basc_py4chan.Thread.files

    .. automethod:: basc_py4chan.Thread.thumbs

    .. automethod:: basc_py4chan.Thread.filenames

    .. automethod:: basc_py4chan.Thread.thumbnames

    .. automethod:: basc_py4chan.Thread.update

    .. automethod:: basc_py4chan.Thread.expand
