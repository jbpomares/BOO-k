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

        # Extract detailed information about the book
        book_details = data.get("volumeInfo", {})

        # Extract specific fields from the book details
        extracted_details = extract_book_details(book_details)

        return extracted_details
    else:
        print("Error: Failed to fetch book details.")
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

# Test the get_book_details function
if __name__ == "__main__":
    book_identifier = input("Enter the identifier of the book to get details: ")
    details = get_book_details(book_identifier)
    print("Book Details:")
    print(details)

