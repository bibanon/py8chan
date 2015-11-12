# credits to Anarov for improved example.py
import py8chan

def main():
	# grab the first thread on the board by checking first page
	v = py8chan.Board('v')
	threads = v.get_threads()
	print("Got %i threads" % len(threads))
	thread = threads[0]

	# thread information
	print(thread)
	print('Sticky?', thread.sticky)
	print('Closed?', thread.closed)

	# topic information
	topic = thread.topic
	print('Topic Repr', topic)
	print('Postnumber', topic.post_number)
	print('Timestamp',  topic.timestamp)
	print('Datetime',   repr(topic.datetime))
	print('Subject',    topic.subject)
	print('Comment',    topic.text_comment)
	print('Replies',    thread.replies)

	# file information
	if topic.has_file:
		for file in topic.all_files():
			print('Filename', file.filename)
			print('  Filemd5hex', file.file_md5_hex)
			print('  Fileurl', file.file_url)
			print('  Thumbnailurl', file.thumbnail_url)
			print()


if __name__ == '__main__':
	main()
