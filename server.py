from flask import Flask, render_template, request
from waitress import serve
from book import get_book_author_details

app = Flask(__name__)


@app.route("/")
@app.route("/index")
def index():
    return render_template('index.html')


@app.route("/book")
def get_details():
    defaultflag = False
    genre = request.args.get('genre')
    if not bool(genre.strip()):
        defaultflag = True
        genre = 'Python'

    details = get_book_author_details(genre)
    # if not details['cod'] == 200:
    #     return
    author_name = details[0]
    book_title = details[1]
    book_page_or_price = details[2]
    top_work = details[3]

    return render_template("book.html", flag=defaultflag, author_name=details[0],
                           book_title=details[1],
                           book_page_or_price=details[2],
                           top_work=details[3])


if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=8000)
