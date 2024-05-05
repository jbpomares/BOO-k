# book_details_service.py
import requests

def get_book_details(book_identifier):
    # Google Books API endpoint for retrieving detailed information about a book
    url = f"https://www.googleapis.com/books/v1/volumes/{book_identifier}"

    # Parameters for the API request
    params = {
        "key": "AIzaSyAc705-LF89q-Qr8h1c96ekILzwnzAtFcg"  # Replace "YOUR_API_KEY" with your actual API key
    }

    # Make the API request
    response = requests.get(url, params=params)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()

        # Extract detailed information about the book (e.g., title, authors, description, etc.)
        book_details = data.get("volumeInfo", {})

        return book_details
    else:
        print("Error: Failed to fetch book details.")
        return {}

# Test the get_book_details function
if __name__ == "__main__":
    book_identifier = input("Enter the identifier of the book to get details: ")
    details = get_book_details(book_identifier)
    print("Book Details:")
    print(details)
