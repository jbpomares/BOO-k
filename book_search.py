# book_search.py

def print_banner():
    print("d8888b.  .d88b.   .d88b.  db db   dD ")
    print("88  `8D .8P  Y8. .8P  Y8. 88 88 ,8P'")
    print("88oooY' 88    88 88    88 YP 88,8P")
    print("88~~~b. 88    88 88    88    88`8b")
    print("88   8D `8b  d8' `8b  d8' db 88 `88.")
    print("Y8888P'  `Y88P'   `Y88P'  YP YP   YD")
    print("Welcome to BOO!k - Your FREE command-line book searching tool")
    print("Enter book names below to find a book to add to your reading list.")
    print("This tool will return books based on your search from the Google Books API.")
    print("Type 'help' to see a list of commands.")
    print("Type 'exit' to quit the program.")

def search_book():
    book_title = input("Enter the title of a book: ")
    return book_title

def main():
    print_banner()
    book_title = search_book()
    print(f"You entered: {book_title}")

if __name__ == "__main__":
    main()
