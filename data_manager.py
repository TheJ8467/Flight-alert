import requests
import os
from dotenv import load_dotenv

load_dotenv()

SHEETY_API_KEY = os.environ.get("EXPORTED_SHEETY_API_KEY")
KIWI_API_KEY = os.environ.get("EXPORTED_KIWI_API_KEY")
KIWI_ENDPOINT = "https://api.tequila.kiwi.com"
SHEETY_ENDPOINT = "https://api.sheety.co/8e61fad103ee672e340a7289fbc2b7d7/flightDeals8467/prices"

kiwi_header = {
    "apikey": KIWI_API_KEY,
}

sheety_header = {
    "Authorization": SHEETY_API_KEY
}

class DataManager:
    #This class is responsible for talking to the Google Sheet.
    def __init__(self):
        self.sheety_respons_get = requests.get(SHEETY_ENDPOINT)
        self.sheety_respons_get.raise_for_status()
        self.cities = [self.sheety_respons_get.json()["prices"][n]["city"] for n in range(9)]
        # self.cities = ["PAR", "TYO", "SYD", "IST", "KUL", "NYC", "SFO", "DPS"]
        #
        self.city_codes = []

        for city in self.cities:
            params = {
                "term": city,
                "location_types": "airport",
            }
            kiwi_response = requests.get(f"{KIWI_ENDPOINT}/locations/query", headers=kiwi_header, params=params)
            self.city_codes.append(kiwi_response.json()["locations"][0]["city"]["code"])
