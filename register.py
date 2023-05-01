user_fname = input("What us your first name?")
user_lname = input("What us your last name?")
user_email = input("What us your email?")
user_email_confirm = input("Type your email again.")

if user_email == user_email_confirm:
  print("You're in the club!")
else:
  print("Please type your email correctly")

import requests
import os


SHEETY_ENDPOINT = "https://api.sheety.co/8e61fad103ee672e340a7289fbc2b7d7/flightDeals8467"

SHEETY_AUTH_TOKEN = os.environ.get("EXPORTED_SHEETY_AUTH_TOKEN")

sheety_header = {
    "Authorization": SHEETY_AUTH_TOKEN
}

user_params = {
  "user": {
    "firstName": user_fname,
    "lastName": user_lname,
    "email": user_email,
  }
}

response = requests.post(f'{SHEETY_ENDPOINT}/users', json=user_params, headers=sheety_header)

print(response.json())
