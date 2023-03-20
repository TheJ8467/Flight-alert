import requests
from data_manager import DataManager
from dateutil.relativedelta import relativedelta
import datetime as dt
import os
from dotenv import load_dotenv
import time
import pprint


load_dotenv()

KIWI_ENDPOINT = "https://api.tequila.kiwi.com"
KIWI_API_KEY = os.environ.get("EXPORTED_KIWI_API_KEY")

kiwi_header = {
    "apikey": KIWI_API_KEY,
}

class FlightData:
    #This class is responsible for structuring the flight data.
    def __init__(self):
        self.best_deal = []
        self.search_response_list = []
        self.sheety_response = DataManager()
        self.today = dt.datetime.now().date()
        self.after_6months = self.today + relativedelta(months=6)
        self.city_codes = []
        self.city_codes = ["PAR", "TYO", "SYD", "IST", "KUL", "NYC", "SFO", "DPS"]
        self.query_request = 0
        self.search_request = 0
        self.search_params = {}
        self.number = []
        self.call_codes()
        self.define_params()
        self.request_search()

    def call_codes(self):
        for city in self.sheety_response.cities:
            self.params = {
                "term": city,
                "location_types": "airport",
            }

            while True:
                try:
                    self.kiwi_response = requests.get(f"{KIWI_ENDPOINT}/locations/query", headers=kiwi_header, params=self.params)
                    self.kiwi_response.raise_for_status()
                except requests.exceptions.HTTPError as e:
                    if e.response.status_code == 429:
                        self.query_request += 1
                        print(f"Too many requests for query, waiting for 5 secs, {self.query_request} requests")
                        time.sleep(5)
                    else:
                        raise e
                else:
                    self.city_codes.append(self.kiwi_response.json()["locations"][0]["city"]["code"])
                    print(f"city_codes is {self.city_codes}")
                    break

    def define_params(self):
        for code in self.city_codes:
            self.search_params = {
                "fly_from": "ICN",
                "fly_to": code,
                "date_from": self.today.strftime("%m/%d/%Y"),
                "date_to": self.after_6months.strftime("%m/%d/%Y"),
                "limit": 10,
                "max_stopovers": 0
            }
            self.number.append(code)


    def request_search(self):
        for code in self.city_codes:
            self.search_params["fly_to"] = code
            while True:
                try:
                    self.search_response = requests.get(f"{KIWI_ENDPOINT}/search", params=self.search_params, headers=kiwi_header)
                    self.search_response.raise_for_status()
                    self.best_deal.append(self.search_response.json()["data"][0]["price"])
                    break

                except requests.exceptions.HTTPError as e:
                    if e.response.status_code == 429:
                        self.search_request += 1
                        print(f"Too many requests for searching on {code}, waiting for 5 secs, {self.search_request} requests")
                        time.sleep(5)
                    else:
                        raise e


            try:
                self.search_response_list.append({
                    "arrival_IATA": self.search_response.json()["data"][0]["flyTo"],
                    "arrival_city": self.search_response.json()["data"][0]["cityTo"],
                    "price": self.search_response.json()["data"][0]["price"],
                    "depart_time_UTC": self.time_converter(self.search_response.json()["data"][0]["dTimeUTC"]).strftime(
                        '%m/%d/%Y %I:%M:%S %p'),

                    "arrival_time_UTC": self.time_converter(self.search_response.json()["data"][0]["aTimeUTC"]).strftime(
                        '%m/%d/%Y %I:%M:%S %p'),
                    })
            except:
                if "arrival_IATA" == None:
                    continue



    def time_converter(self, time):
        return dt.datetime.fromtimestamp(time)


class Flight(FlightData):

    def __init__(self):
        super().__init__()
        self.stop_overs = 0
        self.via_city = ""
        self.define_params()






