# example4-extrafiles.py - get info about all files in first thread

import py8chan

def main():
    # grab the first thread on the board by checking first page
    v = py8chan.Board('v')
    threads = v.get_threads()
    print("Got %i threads" % len(threads))

    # pages on 8chan start at 0, not 1
    first_page = 0
    first_thread = threads[first_page]

    # display info about every file on the first thread, even extra files in posts
    for post in first_thread.all_posts:
        if post.has_file:
            print(":: Post #", post.post_number)
            for file in post.all_files():
                print("  ", file.filename)
                print("  ", file.file_md5_hex)
                print("  ", file.file_url)
                print("  ", file.thumbnail_url)
                print()

if __name__ == '__main__':
    main()
