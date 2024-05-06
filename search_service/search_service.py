import pika
import requests

def search_books(book_title):
    # api endpoint for google books
    url = "https://www.googleapis.com/books/v1/volumes"

    # Parameters for the API request (search by book title)
    params = {
        "q": book_title,
        "maxResults": 5,  # Number of search results to return
        "key": "AIzaSyAc705-LF89q-Qr8h1c96ekILzwnzAtFcg"  
    }

    # Make the API request
    response = requests.get(url, params=params)

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        book_results = []
        for item in data.get("items", []):
            volume_info = item.get("volumeInfo", {})
            title = volume_info.get("title", "Unknown Title")
            authors = volume_info.get("authors", ["Unknown Author"])
            book_results.append({"title": title, "authors": authors})
        return book_results
    else:
        print("Error: Failed to fetch search results.")
        return []

def get_book_identifier(book_title):
    # Google Books API endpoint
    url = "https://www.googleapis.com/books/v1/volumes"

    # Parameters for the API request (search by book title)
    params = {
        "q": f'intitle:"{book_title}"',
        "maxResults": 1,  # Retrieve only the top result
        "key": "AIzaSyAc705-LF89q-Qr8h1c96ekILzwnzAtFcg"  
    }

    # Make the API request
    response = requests.get(url, params=params)

    # Debugging: Print the URL and status code
    print("Request URL:", response.url)
    print("Status Code:", response.status_code)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()

        # Extract book identifier from the response
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
        # Google Books API endpoint for retrieving detailed information about a book
        url = f"https://www.googleapis.com/books/v1/volumes/{book_identifier}"

        # Parameters for the API request
        params = {
            "key": "AIzaSyAc705-LF89q-Qr8h1c96ekILzwnzAtFcg"
        }

        # Make the API request
        response = requests.get(url, params=params)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the JSON response
            data = response.json()

            # Debugging: Print the response data
            print("Response data:", data)

            # Extract detailed information about the book
            book_details = data.get("volumeInfo", {})

            # Debugging: Print the extracted book details
            print("Book details:", book_details)

            # Extract specific fields from the book details
            extracted_details = extract_book_details(book_details)

            return extracted_details
        else:
            # Log the error message
            print(f"Failed to fetch book details. Status code: {response.status_code}")
            return {}
    except Exception as e:
        # Log the exception
        print(f"An error occurred: {str(e)}")
        return {}

def extract_book_details(book_details):
    # Extract specific fields from the book details
    extracted_details = {
        'title': book_details.get('title', ''),
        'authors': book_details.get('authors', []),
        'publisher': book_details.get('publisher', ''),
        'publishedDate': book_details.get('publishedDate', ''),
        'description': book_details.get('description', ''),
        # Add more fields as needed...
    }

    return extracted_details

def on_message(channel, method, properties, body):
    book_titles = body.decode().split(',')
    search_results = search_books(book_titles)

    # Print the search results with indices
    for i, result in enumerate(search_results, start=1):
        print(f"{i}. {result['title']} by {', '.join(result['authors'])}")

    # Prompt user to select a book
    selection = input("Enter the number of the book you want to view details for: ")

    try:
        selection_index = int(selection)
        selected_book = search_results[selection_index - 1]

        # Extract book details for the selected book
        book_identifier = get_book_identifier(selected_book['title'])
        book_details = get_book_details(book_identifier)

        # Display book details
        print("Title:", book_details['title'])
        print("Authors:", ', '.join(book_details['authors']))
        print("Description:", book_details['description'])

    except (ValueError, IndexError):
        print("Invalid selection. Please enter a valid number.")

    

def main():
    # Connect to RabbitMQ server
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    # Declare the exchange for search requests
    channel.exchange_declare(exchange='search_results', exchange_type='fanout', durable=True)

    # Declare a queue for receiving search requests
    result = channel.queue_declare(queue='', exclusive=True)
    queue_name = result.method.queue

    # Bind the queue to the exchange
    channel.queue_bind(exchange='book_search', queue=queue_name)

    # Define callback function for consuming messages
    channel.basic_consume(queue=queue_name, on_message_callback=on_message, auto_ack=True)

    print("Waiting for search requests...")

    # Start consuming messages
    channel.start_consuming()

    # Close the connection
    connection.close()

if __name__ == "__main__":
    main()



