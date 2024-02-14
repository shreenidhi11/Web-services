#####################################################################
#Author: Shreenidhi Acharya (sa8267)
#Description: The randombook.py file serves as the core of this flask based
#application. It contains the operators to be performed when the user
#submits the form(for endpoint /book). This file contains the logic
#for handling API requests. This file implements the necessary
#business logic and displays the appropriate responses to user
#####################################################################
from dotenv import load_dotenv
from pprint import pprint as pp
import requests
import os
from zeep import Client
import random


# Loads the env variables
load_dotenv()

def generate_genre_list(num_genres=10):

    genres = [
        "Action",
        "Adventure",
        "Comedy",
        "Drama",
        "Fantasy",
        "Horror",
        "Mystery",
        "Romance",
        "Science Fiction",
        "Thriller",
        "Historical Fiction",
        "Crime",
        "Documentary",
        "Animation",
        "Biography",
        "Family",
        "Musical",
        "Western",
        "War",
        "Sports",
    ]

    # Shuffle the list to get a random order
    random.shuffle(genres)
    return random.choice(genres)



def get_random_book_author_details():
    """
    Description: Fetch data related to entered genre such as author name,
    book title, price, page count and topwork
    return: author name, book title, price or page count of book and topwork of author
    """

    flag = False
    genre = generate_genre_list()
    print(genre)

    # RESTAPI Call to Google Books API
    requestData = requests.get(
        "https://www.googleapis.com/books/v1/volumes?q={}&key={}".format(genre, os.getenv("GOOGLE_KEY")))
    result = requestData.json()

    # condition for deciding whether to return pagcount or price of the book 
    if not ('listPrice' in result['items'][0]['saleInfo']):
        flag = True
        pageCount = result['items'][0]['volumeInfo']['pageCount']
    else:
        amount = result['items'][0]['saleInfo']['listPrice']['amount']
        resultamount = None

    # fetching author and title
    author = result['items'][0]['volumeInfo']['authors']
    title = result['items'][0]['volumeInfo']['title']

    # SOAP API Call to Data Access
    client = Client(
        'https://www.dataaccess.com/webservicesserver/numberconversion.wso?WSDL')
    
    # condition for returning page count or price of the book based on flag value
    if flag:
        resultPageCount = (client.service.NumberToWords(
            pageCount) + " pages").capitalize()
    else:
        resultamount = client.service.NumberToDollars(amount)
        if not resultamount:
            resultamount = "Zero dollar"
        else:
            resultamount = resultamount.capitalize()

    # RESTAPI Call to Open Library API
    authorData = requests.get(
        "https://openlibrary.org/search/authors.json?q={}".format(author[0]))
    resultauthor = authorData.json()

    pp(resultauthor['docs'][0]['key']+"-M.jpg")


    #  return the first author, title of the book, page count or price of the book and top work of the first author
    return author[0], title, resultamount if not flag else resultPageCount, resultauthor['docs'][0]['top_work'], resultauthor['docs'][0]['key']+"-M.jpg"


if __name__ == "__main__":
    # Logging for backend server
    # Check for empty strings or string with only spaces


    # Get the details
    book_data = get_random_book_author_details()
    print("\n")
    pp(book_data)
