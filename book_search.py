import pika

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
    print("You can search for books by title, author, or ISBN number.")
    print("You will be given a list of search results in the search service window.")
    print("Select a number associated with the result to get the details on the book")
    print("Type 'help' to see a list of commands.")
    print("Type 'exit' to quit the program.")

def search_book():
    book_title = input("Enter the title of a book: ")
    return book_title

def main():
    print_banner()
    while True:
        book_title = search_book()

        if book_title.lower() == 'exit':
            break

        # connect to RabbitMQ server
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()

        # declare exchange
        channel.exchange_declare(exchange='book_search', exchange_type='fanout', durable=True)

        # publish search request message
        channel.basic_publish(exchange='book_search', routing_key='', body=book_title)

        print(f"Search request for '{book_title}' has been sent to RabbitMQ.")

        # close connection
        connection.close()

if __name__ == "__main__":
    main()


