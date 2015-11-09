Status
------

This py8chan wrapper inherits the classes of BASC_py4chan and overrides some of it's functions, since the APIs are very similar (but not exactly the same). 

This way, we reduce redundant work and make it possible to create wrappers for other similar imageboard APIs, such as py420chan or even pyFuuka.

However, we face some unique challenges by doing this. I've managed to get py8chan obtaining JSON data from the 8chan API, but it's unable to grab replies from threads, and has some strange quirks when retrieving thread objects.

And I'm getting the feeling that it might not be a bad idea to maintain different codebases instead of inheriting, (when it comes to the 8chan API). The 8chan API preserves many legacy quirks of the 4chan API and may end up requiring different strategies to parse.

In the end, if you find this too difficult or inelegant, we can just have BASC-Archiver use this existing 8chan API.

https://github.com/danjmercurio/eightchanAPI

Modifications to BASC_py4chan
-----------------------------

Some modifications to py4chan are necessary. Some I've done, some I haven't.

* Make Url Generator accessible to anyone. This way, I can define my own URL generator in py8chan and override the existing one. I've already pushed this to the repository.
* `boards.json` - 8chan uses a completely different `boards.json` format compared to 4chan. An entirely new way of processing it will be necessary. But until then, we've disabled the feature entirely.
  * py4chan's Board Listing system consists of some strange functions outside of the Board class. These need to be packed as static methods in a List class or something. Until py4chan's Board Listing system is redesigned, it will not be possible to override board metadata methods effectively. This is why in the current wrapper, I raise Attribute Errors for board metadata.

What to fix
-----------

* Sometimes the thread object is not obtained. The best way for me to get a thread object is to first run `board.get_all_threads()`, which then allows me to grab a thread object: but only once (???)
* `replies` and `images` (integer) - Infuriatingly there is no replies enumerator in the thread json on 8chan, unlike 4chan. You have to count the amount of objects in the thread yourself, or grab it from the board's thread listing.
  * As a result of this, no replies are stored in the thread object at all. Why?

Features to Add
---------------

* `extra_files` (dict) - Multiple files can be uploaded in one post on 8chan. This can be a challenge to get working.

Differences from 4chan API
--------------------------

The basc_py4chan library required some modifications to make this possible. In particular, the introduction of a Url Class generator that could be inherited.

vichan's API tries to stick to the 4chan API standard, but it has some differences, `listed here. <https://github.com/vichan-devel/vichan-API/>`_

* **Incompatibilities** - Type differences to watch out for.
  * `tim` (string) - UNIX timestamp + microseconds. This is a string instead of an integer on 4chan API, since it is actually only used by image filenames. Python converts types on it's own, so no need to worry about this.
* **Not Implemented Yet** - Might become a feature in the future, so note it when overriding.
  * `id` (string) - text (8 characters), Mod, Admin, Developer, Founder. Seems a bit redundant when we have the capcode.
  * `filedeleted` (integer) - 0 or 1, states if file was deleted.
  * `spoiler` (integer) - 0 or 1, states if file was spoilered.
* **Does Not Exist** - It's not used and won't be for the foreseeable future.
  * `archived` - A integer with either 0 or 1.
  * `now` - Date and timestamp used by 4chan based on EST/EDT timezone. Vichan autogenerates this from UNIX `tim` instead, since everyone's timezone can differ.
  * `custom_spoiler` - No custom spoilers, let alone spoilers of any kind yet.
  * `bumplimit` - No limit.
  * `imagelimit` - No limit.
  * `capcode_replies` - Not used.
  * `tag` - Not used.
  * `semantic_url` - Not used.