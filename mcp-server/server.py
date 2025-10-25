#(to add server to claude)mcp-server % uv run mcp install server.py
import argparse
from mcp.server.fastmcp import FastMCP 
import httpx 
from dotenv import load_dotenv 
import os 
import logging

mcp = FastMCP("Find Books")

load_dotenv()

# Constants
API_KEY = os.getenv("API_KEY")
API_KEY_URL_FORMAT = f"&key={API_KEY}"
BASE_URL = "https://www.googleapis.com/books/v1/volumes?q="
BOOK_FILE = os.path.join(os.path.dirname(__file__), "books_cache.txt")


logging.getLogger("httpx").setLevel(logging.WARNING)


@mcp.tool()
def get_book(book: str) -> list:
    '''
    Retrieves books from Google Books API.
    
    Args:
        book (str): Book title to be retrieved.

    Returns:
        str: A list of 5 books from Google Books API.
    '''
    from_cache = find_book_in_cache(book)
    if from_cache:
        return from_cache
        
    url = format_url(book)
    try:
        response = httpx.request('GET', url)
        json = response.json()
        bookInfo = json['items'][0]['volumeInfo']
        title = bookInfo['title']
        authors = parse_author(bookInfo['authors'])
        published_date = bookInfo['publishedDate']
        maturity_rating = bookInfo['maturityRating']
        formatted_string = format_response(title, authors, published_date, maturity_rating)
        write_to_file(formatted_string)
        logging.info("API Request")

        return formatted_string
    
    except Exception as e:
        return f"Error while retrieving books: {e}"
    


# Helper functions to get_book() tool

def find_book_in_cache(book: str) -> str:
    with open(BOOK_FILE, 'r') as f:
        lines = f.readlines()
        for i in range(len(lines)):
            if lines[i][:7] == "Title: ":
                possible_match = lines[i][7:].strip()[:-1]
                possible_match_to_list = possible_match.split()
                joined_possible_match = "".join(possible_match_to_list).lower()

                book_to_list = book.split()
                joined_book = "".join(book_to_list).lower()

                if len(joined_book) > len(joined_possible_match):
                    windows = len(joined_book) - len(joined_possible_match) + 1
                    l = 0
                    r = len(joined_possible_match)
                    for i in range(windows):
                        if joined_possible_match == joined_book[l:r]:
                            logging.info("Book info retrieved from cache.")
                            return "".join(lines[i:i+4])
                        else: 
                            l += 1
                            r += 1
                elif len(joined_possible_match) > len(joined_book):
                    windows = len(joined_possible_match) - len(joined_book) + 1
                    l = 0
                    r = len(joined_book)
                    for i in range(windows):
                        if joined_book == joined_possible_match[l:r]:
                            logging.info("Book info retrieved from cache.")
                            return "".join(lines[i:i+4])
                        else:
                            l += 1
                            r += 1
                else:
                    if joined_possible_match == joined_book:
                        logging.info("Book info retrieved from cache.")
                        return "".join(lines[i:i+4])

                
        return None
     

def format_url(book_str: str) -> str:
    book_title_list = book_str.split()
    book_title_url_format = ""
    for word in book_title_list:
        book_title_url_format += word +  "+"

    book_title_url_format = book_title_url_format[:-1]

    return BASE_URL + book_title_url_format + API_KEY_URL_FORMAT


def parse_author(authors: list) -> str:
    author_str = ""
    for author in authors:
        author_str += author + ","
    return author_str[:-1]


def format_response(title: str, authors: str, published_date: str, maturity_rating: str) -> str:
    response = f"""
Title: {title},
Author(s): {authors},
Published Date: {published_date},
Maturity Rating: {maturity_rating}
---------------------------------"""
    length_string = f"\nObject Length: {len(response)}"

    return length_string + response
    

def write_to_file(to_write: str) -> None:
    
    #clearing cache space if necessary
    current_books = count_books()

    if current_books == 100:
        lines = []
        with open(BOOK_FILE, 'r') as f:
            lines = f.readlines()

        with open(BOOK_FILE, 'w') as f:
            f.writelines(lines[7:])

    with open(BOOK_FILE, 'a') as f:
        f.write(to_write)



def count_books() -> int:
    count = 0
    with open(BOOK_FILE, 'r') as f:
        lines = f.readlines()
        for i in range(len(lines)):
            if lines[i][:6] =="Title:":
                count += 1
    return count


def book_in_cache(book: str) -> bool:
    content = retrieve_file()
    if not content:
        return False 
    
    word_list = content.split()
    joined_content = "".join(word_list).lower()

    book_title_list = book.split()  
    joined_book = "".join(book_title_list).lower()

    #implementing sliding window algorithm for match to book of interest
    file_length = len(joined_content)
    l = 0
    r = len(joined_book)
    windows = file_length - r
    for i in range(windows):
        if joined_book == joined_content[l:r]:
            return True 
        else: 
            l += 1
            r += 1
    
    return False


# Helper to book_in_cache()
def retrieve_file() -> str:
    with open(BOOK_FILE, 'r') as f:
        content = f.read()
        if not content:
            return None
        return content
    


@mcp.resource('books://latest')
def get_latest_book() -> str:
    '''
    Gets the latest book from the file

    Return:
        str: The latest book from the text file.
    '''

    with open(BOOK_FILE, 'r') as f:
        lines = f.readlines()

    return lines[-5][6:-2] if lines else "No books cached yet."



@mcp.prompt()
def note_summary_prompt() -> str:
    '''
    Generate a prompt to summarize the major themes of books in the current cache.
    
    Return:
        str: A summary of the themes in the book cache.
    '''
    with open(BOOK_FILE, 'r') as f:
        content = f.read()
        if not content:
            return "No books in cache yet."
    
    return f"Summarize the major themes of the books currently in the cache: {content}"



if __name__ == "__main__":

    #for testing
    # while True:
        # book = input("What books would you like?: \n")
        # if book == "quit":
            # break
        # get_book(book)

    logging.info("Starting Find Book Server")


    #debug mode
    # uv run mcp dev server.py 

    #production mode 
    # uv run server.py --server_type=sse 


    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--server_type", type=str, default="sse", choices=["sse", "stdio"]
    )

    args = parser.parse_args()
    mcp.run(args.server_type)

