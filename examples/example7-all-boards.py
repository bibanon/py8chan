# This example demonstrates the use of the get_all_boards function
import py8chan

def main():
    # Get a list of all boards
    boards = py8chan.get_all_boards()
    # Sort boards by the number of posts
    boards.sort(key=lambda x: x.num_posts, reverse=True)
    # Print the title and subtitle of the first 10 boards
    for i in range(0, 10):
        print(boards[i].title + ": " + boards[i].subtitle)

if __name__ == '__main__':
    main()
