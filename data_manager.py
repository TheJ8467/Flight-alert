import sys

import requests
import os
from dotenv import load_dotenv
import time

class DataManager:
    #This class is responsible for talking to the Google Sheet.
    def __init__(self):
        # For saving requests for Sheety
        self.city_codes = ["PAR", "BER", "TYO", "SYD", "IST", "KUL", "NYC", "SFO", "CPT" ,"DPS"]
        self.cities = ["Paris", "Berlin", "Tokyo", "Sydney", "Istanbul", "Kuala Lumpur", "New York", "San Francisco",
                       "Cape Town", "Bali"]
        load_dotenv()
        self.kiwi_header = {"apikey": os.environ.get("EXPORTED_KIWI_API_KEY")}
        self.sheety_header = {"Authorization": os.environ.get("EXPORTED_SHEETY_API_KEY")}
        self.KIWI_ENDPOINT = "https://api.tequila.kiwi.com"
        self.SHEETY_ENDPOINT = "https://api.sheety.co/3195a9561f0219ec864578b13b2f6b62/flightDeals8467"

        self.sheety_prices_status = requests.get(f'{self.SHEETY_ENDPOINT}/prices', headers=self.sheety_header)
        self.sheety_prices_status.raise_for_status()
        self.sheety_users_status = requests.get(f'{self.SHEETY_ENDPOINT}/users', headers=self.sheety_header)
        self.sheety_users_status.raise_for_status()
        self.sheety_prices = requests.get(f'{self.SHEETY_ENDPOINT}/prices', headers=self.sheety_header).json()
        self.sheety_users = requests.get(f'{self.SHEETY_ENDPOINT}/users', headers=self.sheety_header).json()

        #self.cities = [self.sheety_respons_get.json()["prices"][n]["city"] for n in range(len(self.sheety_prices[prices]))]
        # for city in self.cities:
        #     time.sleep(3)
        #     params = {
        #         "term": city,
        #         "location_types": "airport",
        #     }
        #     kiwi_response = requests.get(f"{self.KIWI_ENDPOINT}/locations/query", headers=self.kiwi_header, params=params)
        #     self.city_codes.append(kiwi_response.json()["locations"][0]["city"]["code"])
        #     print(self.city_codes)
