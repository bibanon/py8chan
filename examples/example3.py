# credits to Anarov for improved example.py
import py8chan

board = py8chan.Board('v')
threads = board.get_threads()
print("Got %i threads" % len(threads))
first_thread = threads[0]
print("First thread: %r" % first_thread)
print("Replies: %r" % first_thread.replies)
print("Updating first thread...")
first_thread.update()
print("First thread now: %r" % first_thread)
for post in first_thread.replies:
    print(post.url)
