# brand new class to handle 8chan/vichan's multiple files per post
# supersedes py4chan's file generators in Thread and Post

class File(object):
	""" Represents File objects and their thumbnails.
	
	Constructor:
		post (py8chan.Post) - parent Post object.
		data (dict) - The extra_files dict from the 8chan API.
	
	Attributes:
		file_md5 (string): MD5 hash of the file attached to this post.
		file_md5_hex (string): Hex-encoded MD5 hash of the file attached to this post.
		filename (string): Original name of the file attached to this post.
		file_url (string): URL of the file attached to this post.
		file_extension (string): Extension of the file attached to this post. Eg: ``png``, ``webm``, etc.
		file_size (int): Size of the file attached to this post.
		file_width (int): Width of the file attached to this post.
		file_height (int): Height of the file attached to this post.
		file_deleted (bool): Whether the file attached to this post was deleted after being posted.
		thumbnail_width (int): Width of the thumbnail attached to this post.
		thumbnail_height (int): Height of the thumbnail attached to this post.
		thumbnail_fname (string): Filename of the thumbnail attached to this post.
		thumbnail_url (string): URL of the thumbnail attached to this post.
		has_file (bool): Whether this post has a file attached to it.
		url (string): URL of this post.
	"""
	
	def __init__(self, post, data):
		self._post = post
		self._data = data
		self._url = Url(board=self._post._thread._board.name, https=self._post._thread._board.https)       # 8chan URL generator
		
	@property
	def file_md5(self):
		if not self.has_file:
			return None

		return self._data['md5'].decode('base64')

	@property
	def file_md5_hex(self):
		if not self.has_file:
			return None

		return self.file_md5.encode('hex')

	@property
	def filename(self):
		if not self.has_file:
			return None

		board = self._thread._board
		
		return '%i%s' % (
			self._data['tim'],
			self._data['ext']
		)

	@property
	def file_url(self):
		if not self.has_file:
			return None

		board = self._thread._board
		return self._url.file_url(
			self._data['tim'],
			self._data['ext']
		)

	@property
	def file_extension(self):
		return self._data.get('ext')

	@property
	def file_size(self):
		return self._data.get('fsize')

	@property
	def file_width(self):
		return self._data.get('w')

	@property
	def file_height(self):
		return self._data.get('h')

	@property
	def file_deleted(self):
		return self._data.get('filedeleted') == 1

	@property
	def thumbnail_width(self):
		return self._data.get('tn_w')

	@property
	def thumbnail_height(self):
		return self._data.get('tn_h')

	@property
	def thumbnail_fname(self):
		if not self.has_file:
			return None

		board = self._thread._board

		return '%is.jpg' % (
			self._data['tim']
		)

	@property
	def thumbnail_url(self):
		if not self.has_file:
			return None

		board = self._thread._board
		return self._url.thumb_url(
			self._data['tim']
		)

	def file_request(self):
		return self._thread._board._requests_session.get(self.file_url)

	def thumbnail_request(self):
		return self._thread._board._requests_session.get(self.thumbnail_url)