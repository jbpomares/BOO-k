import pika
import requests
import logging

# Configure logging
logging.basicConfig(level=logging.ERROR)

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

            # Extract detailed information about the book
            book_details = data.get("volumeInfo", {})

            # Extract specific fields from the book details
            extracted_details = extract_book_details(book_details)

            return extracted_details
        else:
            # Log the error message
            logging.error(f"Failed to fetch book details. Status code: {response.status_code}")
            return {}
    except Exception as e:
        # Log the exception
        logging.error(f"An error occurred: {str(e)}")
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

def get_book_identifier(book_title):
    # Google Books API endpoint
    url = "https://www.googleapis.com/books/v1/volumes"

    # Parameters for the API request (search by book title)
    params = {
        "q": f'intitle:"{book_title}"',
        "maxResults": 1,  # Retrieve only the top result
        "key": "YOUR_API_KEY"  # Replace "YOUR_API_KEY" with your actual API key
    }

    # Make the API request
    response = requests.get(url, params=params)

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
    
def on_message(channel, method, properties, body):
    # Convert message body to string (assuming it contains book titles)
    book_titles = body.decode().split(',')

    # For each book title received, get its book identifier
    for book_title in book_titles:
        # Trim leading and trailing spaces
        book_title = book_title.strip()

        # Remove square brackets and quotation marks
        book_title = book_title.strip("[]").strip("'").strip('"')

        # Get book identifier using the Google Books API
        book_identifier = get_book_identifier(book_title)
        
        # Get book details if identifier is found
        if book_identifier:
            # Get book details
            book_details = get_book_details(book_identifier)

            # Connect to RabbitMQ server
            connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
            channel = connection.channel()

            # Declare the exchange for book details
            channel.exchange_declare(exchange='book_details', exchange_type='fanout', durable=True)

            # Publish book details message
            channel.basic_publish(exchange='book_details', routing_key='', body=str(book_details))

            print(f"Book details for '{book_title}' have been sent to RabbitMQ.")

            # Close the connection
            connection.close()
        else:
            print(f"Failed to fetch book identifier for '{book_title}'. Skipping...")


def main():
    # Connect to RabbitMQ server
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    # Declare the exchange for search results
    channel.exchange_declare(exchange='search_results', exchange_type='fanout', durable=True)

    # Declare a queue for receiving search results
    result = channel.queue_declare(queue='', exclusive=True)
    queue_name = result.method.queue

    # Bind the queue to the exchange
    channel.queue_bind(exchange='search_results', queue=queue_name)

    # Define callback function for consuming messages
    channel.basic_consume(queue=queue_name, on_message_callback=on_message, auto_ack=True)

    print("Waiting for search results...")

    # Start consuming messages
    channel.start_consuming()

if __name__ == "__main__":
    main()




