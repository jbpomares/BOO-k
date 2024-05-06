import pika
import requests

def search_books(book_title):
    # api endpoint for google books
    url = "https://www.googleapis.com/books/v1/volumes"

    # parameters for API request
    params = {
        "q": book_title,
        "maxResults": 5,  # Number of search results to return
        "key": "AIzaSyAc705-LF89q-Qr8h1c96ekILzwnzAtFcg"  
    }

    # api request
    response = requests.get(url, params=params)

    # check if request was successful
    if response.status_code == 200:
        data = response.json()
        book_results = []
        for item in data.get("items", []):
            volume_info = item.get("volumeInfo", {})
            title = volume_info.get("title", "Unknown Title")
            authors = volume_info.get("authors", ["Unknown Author"])
            book_results.append({"title": title, "authors": authors})
        return book_results
    # error message
    else:
        print("Error: Failed to fetch search results.")
        return []

def get_book_identifier(book_title):
    # google books API endpoint
    url = "https://www.googleapis.com/books/v1/volumes"

    # params for API request
    params = {
        "q": f'intitle:"{book_title}"',
        "maxResults": 1,  # Retrieve only the top result
        "key": "AIzaSyAc705-LF89q-Qr8h1c96ekILzwnzAtFcg"  
    }

    # make API request
    response = requests.get(url, params=params)

    # check if request was successful
    if response.status_code == 200:
        # parse JSON response
        data = response.json()

        # extract book identifier from response
        if data.get("items"):
            book_identifier = data["items"][0]["id"]
            return book_identifier
        else:
            print(f"No book identifier found for '{book_title}'.")
            return None
    else:
        print(f"Failed to fetch book identifier for '{book_title}'.")
        return None

def get_book_details(book_identifier):
    try:
        # google books API endpoint for retrieving book details
        url = f"https://www.googleapis.com/books/v1/volumes/{book_identifier}"

        # params for API request
        params = {
            "key": "AIzaSyAc705-LF89q-Qr8h1c96ekILzwnzAtFcg"
        }

        # make API request
        response = requests.get(url, params=params)

        # check if the request was successful
        if response.status_code == 200:
            # parse the JSON response
            data = response.json()

            # extract book detals
            book_details = data.get("volumeInfo", {})


            # extract specific fields from the book details
            extracted_details = extract_book_details(book_details)

            return extracted_details
        else:
            # log error message
            print(f"Failed to fetch book details. Status code: {response.status_code}")
            return {}
    except Exception as e:
        # log exception
        print(f"An error occurred: {str(e)}")
        return {}

def extract_book_details(book_details):
    # get specific fields from book details
    extracted_details = {
        'title': book_details.get('title', ''),
        'authors': book_details.get('authors', []),
        'publisher': book_details.get('publisher', ''),
        'publishedDate': book_details.get('publishedDate', ''),
        'description': book_details.get('description', ''),
    
    }

    return extracted_details

def on_message(channel, method, properties, body):
    book_titles = body.decode().split(',')
    search_results = search_books(book_titles)

    # Print the search results
    for i, result in enumerate(search_results, start=1):
        print(f"{i}. {result['title']} by {', '.join(result['authors'])}")

    while True:
        # Prompt the user to select a book via a number
        selection = input("Enter the number of the book you want to view details for: ")

        try:
            selection_index = int(selection)
            selected_book = search_results[selection_index - 1]

            # Get book details for the book the user chose
            book_identifier = get_book_identifier(selected_book['title'])
            book_details = get_book_details(book_identifier)

            # Create bold font
            BOLD = '\033[1m'
            END_BOLD = '\033[0m'

            # Print book details
            print(f"{BOLD}Title:{END_BOLD} {book_details['title']}")
            print(f"{BOLD}Authors:{END_BOLD} {', '.join(book_details['authors'])}")
            print(f"{BOLD}Description:{END_BOLD} {book_details['description']}")
            print("Return back to book search screen to input another search")

            break  # Exit the loop if the input is valid

        except (ValueError, IndexError):
            print("Invalid selection. Please enter a valid number.")


    

def main():
    # connect to RabbitMQ server
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    # declare xchange for search requests
    channel.exchange_declare(exchange='search_results', exchange_type='fanout', durable=True)

    # declare queue for receiving search requests
    result = channel.queue_declare(queue='', exclusive=True)
    queue_name = result.method.queue

    # bind queue to exchange
    channel.queue_bind(exchange='book_search', queue=queue_name)

    # define callback function for consuming messages
    channel.basic_consume(queue=queue_name, on_message_callback=on_message, auto_ack=True)

    print("Waiting for search requests...")

    # start consuming messages
    channel.start_consuming()

    # close connection
    connection.close()

if __name__ == "__main__":
    main()



