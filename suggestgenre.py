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

def add_genre_to_list(user_input):
    genre = ["Fantasy", "Science Fiction", "Mystery",
              "Romance", "Thriller", "Historical Fiction"]
    genre.append(user_input)
    return genre






if __name__ == "__main__":
    # Logging for backend server
    # Check for empty strings or string with only spaces

    user_input = input()
    print(user_input)



