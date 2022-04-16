8chan/vichan Python Library
===========================

The Bibliotheca Anonoma’s **complete Python Wrapper for the 8chan API.**
Uses requests, respects if-modified-since headers on updating threads.
Caches thread objects. Fun stuff.

An absolute must if you want to interface with or scrape from 8chan or
other vichan-based imageboards/textboards, using a Python script.

`Hosted
Documentation <http://py8chan.readthedocs.org/en/latest/index.html>`__

`Github Repository <https://github.com/bibanon/py8chan>`__

You can install this library `straight from
PyPi <https://pypi.python.org/pypi/py8chan>`__ with:

::

   pip install py8chan

Getting Help
------------

If you want help, or you have some trouble using this library,
put a issue on our `Github Issue Tracker <https://github.com/bibanon/py8chan>`__
and we’ll respond as soon as we can!

--------------

Usage
-----

.. code:: python

   import py8chan
   board = py8chan.Board('v')
   thread = board.get_thread(423491034)

   print(thread)

   # supports displaying extra files in one post as well!
   for file in thread.file_objects():
       print(file.file_url)
       
   # In a while...
   print("I fetched", thread.update(), "new replies.")

Documentation
-------------

This library mostly extends the classes of
`BASC-py4chan <https://github.com/bibanon/BASC-py4chan>`__, but has some
slight but major differences. See the py8chan documentation for more
info.

`py8chan
Documentation <http://py8chan.readthedocs.org/en/latest/index.html>`__

`The official 8chan Swagger API documentation can be found
here. <https://gitlab.com/N3X15/8chan-API/blob/master/definitions>`__

License
-------

::

               DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
                       Version 2, December 2004

    Copyright (C) 2004 Sam Hocevar <sam@hocevar.net>

    Everyone is permitted to copy and distribute verbatim or modified
    copies of this license document, and changing it is allowed as long
    as the name is changed.

               DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
      TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION

     0. You just DO WHAT THE FUCK YOU WANT TO.
