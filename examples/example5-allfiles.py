# example4-extrafiles.py - get info about all files in first thread

import py8chan

def main():
	# grab the first thread on the board by checking first page
	v = py8chan.Board('v')
	threads = v.get_threads()
	print("Got %i threads" % len(threads))

	# pages on 8chan start at 0, not 1
	first_page = 0
	first_thread = v.get_thread(6919133)

	# display the url of every file on the first thread, even extra files in posts
	for url in first_thread.files():
		print(url)

if __name__ == '__main__':
	main()
