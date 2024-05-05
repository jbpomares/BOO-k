import requests
import book_details_service

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
        book_identifiers = [item["id"] for item in data.get("items", [])]

        return book_results, book_identifiers
    else:
        print("Error: Failed to fetch search results.")
        return [], []

def main():
    # Prompt the user to enter a book title to search for
    search_query = input("Enter the title of a book to search for: ")

    # Search for books and get search results and identifiers
    search_results, book_identifiers = search_books(search_query)

    # Display search results to the user
    print("Search Results:")
    for i, result in enumerate(search_results, start=1):
        print(f"{i}. {result}")

    # Prompt the user to choose a book from the search results
    choice = int(input("Enter the number of the book you want more details about: "))

    # Get the ISBN or identifier of the selected book
    selected_book_identifier = book_identifiers[choice - 1]

    # Call the function from the book_details_service.py script to retrieve details about the selected book
    book_details = book_details_service.get_book_details(selected_book_identifier)

    # Print the detailed information about the selected book
    print("Detailed Information about the selected book:")
    print(book_details)

if __name__ == "__main__":
    main()

