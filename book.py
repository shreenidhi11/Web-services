from dotenv import load_dotenv
from pprint import pprint as pp
import requests
import os
from zeep import Client

load_dotenv()


def get_book_author_details(genre="Python"):
    flag = False
    requestData = requests.get(
        "https://www.googleapis.com/books/v1/volumes?q={}&key={}".format(genre, os.getenv("GOOGLE_KEY")))
    result = requestData.json()

    if not ('listPrice' in result['items'][0]['saleInfo']):
        print("went here")
        flag = True
        pageCount = result['items'][0]['volumeInfo']['pageCount']
        # print("pagecount is", pageCount)
    else:
        amount = result['items'][0]['saleInfo']['listPrice']['amount']
        resultamount = None

    author = result['items'][0]['volumeInfo']['authors']
    title = result['items'][0]['volumeInfo']['title']

    client = Client(
        'https://www.dataaccess.com/webservicesserver/numberconversion.wso?WSDL')
    if flag:
        resultPageCount = (client.service.NumberToWords(
            pageCount) + "pages").capitalize()

    else:
        resultamount = client.service.NumberToDollars(amount)
        print(resultamount)
        if not resultamount:
            resultamount = "Zero dollar"
        else:
            resultamount = resultamount.capitalize()

    authorData = requests.get(
        "https://openlibrary.org/search/authors.json?q={}".format(author[0]))
    resultauthor = authorData.json()

    return author[0], title, resultamount if not flag else resultPageCount, resultauthor['docs'][0]['top_work']


if __name__ == "__main__":
    print('\n*** Get your favourite genre *** \n')
    genre = input("\n Please enter the genre name")

    # Check for empty strings or string with only spaces
    if not bool(genre.strip()):
        genre = 'Python'

    book_data = get_book_author_details(genre)
    print("\n")
    pp(book_data)
