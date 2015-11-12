This file documents all changes made to py8chan, based on py4chan.

Currently, as of v0.0.1, there should be enough features to get the BASC-Archiver working, as a drop-in replacement (Only the Post Class was changed significantly, which does not affect the BASC-Archiver). 

However, there are still a few unimplemented things.

## To Do

* **BASC-Archiver Support** - The BASC-Archiver now needs to have an Eightchan Class to allow py8chan to work on it.
* **Documentation Overhaul** - The documentation must be changed completely to match the 8chan API.
* **YouTube Embed Support** - There are some thread JSON with an `embed` item, and no image. This embed item has standard youtube embed HTML.
* **8chan Board List Support** - Obviously, 8chan has a very large list of public boards. It can be obtained if need be.
* **8chan Catalog Support** - 8chan has a catalog format that is completely different from 4chan's. Complete overhaul will be necessary.

## Differences from 4chan API

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

## Changes

* `Url` Class
  * All URLs have been set to 8chan's URL scheme. Though even though it is totally compatible with other vichan APIs, this doesn't really make it a vichan wrapper then...
  * (Future) - Maybe make it possible to load custom URL schemes into the wrapper?
* `Board` Class
  * `get_threads()` 8chan/vichan board pages actually start at 0, not 1!
* `File` Class
  * New `File` Class. This takes all the file attributes out of the Posts class and into a File class, so it can support multiple files per post (as seen on 8chan).
* `Post` Class
  * File attributes removed from Post class, replaced with `all_files()` and `extra_files()` generators, that yield all files in the Post.
  * (Backport to py4chan) - In py4chan, to maintain compatibility with scripts, the File attributes will remain in Post. It's doubtful that 4chan will implement multiple files per post, but File objects make it easy to grab all attributes of every File in a Thread using `file_objects()`, so we should backport it.
* `Thread` Class
  * New `file_objects()` function. This allows you to grab all File objects in the thread.
  * `_from_json()` - There's no `replies` or `images` item in 8chan/vichan's thread JSON.

### 8chan Catalog Format

8chan uses a unique catalog format, unlike 4chan. It shows a preview of the thread. However, this means that we have to reformulate the Board class to deal with it.

### Differences from 4chan API

* Not implemented yet
  * poster_id (int): Poster ID.
  * file_deleted (bool): Whether the file attached to this post was deleted after being posted.
* Unsupported Functions
  * replies and images (in OP) - Infuriatingly, the OP post in a thread doesn't list how many replies there are in a thread.
  * semantic_url (string): URL of this post, with the thread's 'semantic' component.
  * semantic_slug (string): This post's 'semantic slug'.

## Bugs in py4chan

The file_md5 string does not convert into base64 correctly in python3. This is because Python3 treats all string literals as unicode, but decode only works on ASCII. You can't use a Python3 compatible command, because python2 wouldn't work with it.

Thus, instead of using `.encode()` or `.decode()`, use the included Python libraries base64 and binascii, which abstract away the issues. [More info at StackOverflow.](http://stackoverflow.com/a/16033232)

```
from base64 import b64decode
from binascii import hexlify

@property
def file_md5(self):
	# Py 2/3 compatible equivalent of:
	#return self._data['md5'].decode('base64')
	# More info: http://stackoverflow.com/a/16033232
	# returns a bytestring
	return b64decode('NOetrLVnES3jUn1x5ZPVAg==')
	
@property
def file_md5_hex(self):
	return hexlify(self.file_md5).decode('ascii')
```

### Feature Fixes in py4chan

In py4chan, there was no need for a File class because a post could only have one file. Now with py8chan, there are multiple files, so each file needs to be encapsulated in it's own class.

This could be backported just for consistency to py4chan.