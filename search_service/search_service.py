# search_service.py
import pika
import requests

def search_books(book_title):
    # Google Books API endpoint
    url = "https://www.googleapis.com/books/v1/volumes"

    # Parameters for the API request (search by book title)
    params = {
        "q": book_title,
        "maxResults": 5,  # Number of search results to return
        "key": "AIzaSyAc705-LF89q-Qr8h1c96ekILzwnzAtFcg"  # Replace "YOUR_API_KEY" with your actual API key
    }

    # Make the API request
    response = requests.get(url, params=params)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()

        # Extract relevant information from the response (e.g., book titles and identifiers)
        book_results = [item["volumeInfo"]["title"] for item in data.get("items", [])]
        return book_results
    else:
        print("Error: Failed to fetch search results.")
        return []

def on_message(channel, method, properties, body):
    # Convert message body to string (assuming it contains book title)
    book_title = body.decode()

    # Perform book search
    search_results = search_books(book_title)

    # Connect to RabbitMQ server
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    # Declare the exchange for search results
    channel.exchange_declare(exchange='search_results', exchange_type='fanout', durable=True)

    # Publish search results message
    channel.basic_publish(exchange='search_results', routing_key='', body=str(search_results))

    print(f"Search results for '{book_title}' have been sent to RabbitMQ.")

    # Close the connection
    connection.close()

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

if __name__ == "__main__":
    main()

