import requests
from data_manager import DataManager
from dateutil.relativedelta import relativedelta
import datetime as dt
import time

data_manager = DataManager()

class FlightData:
    # This class is responsible for structuring the flight data.
    def __init__(self):
        self.best_deal = []
        self.search_response_list = []
        self.today = dt.datetime.now().date()
        self.after_6months = self.today + relativedelta(months=6)
        self.query_request = 0
        self.search_request = 0
        self.search_params = {}
        self.number = []
        self.via_city = ''
        self.alt_price = ''
        self.request_search()

    def request_search(self):
        for code in data_manager.city_codes:
            while True:
                try:
                    self.search_response = requests.get(f"{data_manager.KIWI_ENDPOINT}/search", params={
                        "fly_from": "ICN",
                        "fly_to": code,
                        "date_from": self.today.strftime("%d/%m/%Y"),
                        "date_to": self.after_6months.strftime("%d/%m/%Y"),
                        "limit": 10,
                        "max_stopovers": 0
                    }, headers=data_manager.kiwi_header)
                    self.search_response.raise_for_status()

                    try:
                        self.best_deal.append(self.search_response.json()["data"][0]["price"])
                    except IndexError:
                        self.best_deal.append(1116)
                    break

                except requests.exceptions.HTTPError as e:
                    if e.response.status_code == 429:
                        self.search_request += 1
                        print(
                            f"Too many requests for searching on {code}, waiting for 5 secs, {self.search_request} requests")
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

                    "arrival_time_UTC": self.time_converter(
                        self.search_response.json()["data"][0]["aTimeUTC"]).strftime(
                        '%m/%d/%Y %I:%M:%S %p'),
                })
            except:
                self.search_response_list.append({
                    "arrival_IATA": code,
                    "arrival_city":"",
                    "price": 1116,
                    "depart_time_UTC":"",
                    "arrival_time_UTC":"",
                })

    def time_converter(self, time):
        return dt.datetime.fromtimestamp(time)

    def alt_request(self, code):
        self.search_response = requests.get(f"{data_manager.KIWI_ENDPOINT}/search", params={
            "fly_from": "ICN",
            "fly_to": code,
            "date_from": self.today.strftime("%d/%m/%Y"),
            "date_to": self.after_6months.strftime("%d/%m/%Y"),
            "limit": 10,
            "max_stopovers": 1
        }, headers=data_manager.kiwi_header)
        try:
            self.search_response_list.append({
                                    "via_city": self.search_response.json()["data"][0]["route"][0]["cityTo"],
                                    "alt_price": self.search_response.json()["data"][0]["price"],
                                    "arrival_city": self.search_response.json()["data"][0]["cityTo"],
                                    "arrival_IATA":  self.search_response.json()["data"][0]["flyTo"],
                                    "depart_time_UTC": self.time_converter(self.search_response.json()["data"][0]["dTimeUTC"]).strftime(
                            '%m/%d/%Y %I:%M:%S %p'),
                                    "arrival_time_UTC": self.time_converter(self.search_response.json()["data"][0]["aTimeUTC"]).strftime(
                            '%m/%d/%Y %I:%M:%S %p'),
                                })

            via_city = self.search_response_list[-1]["via_city"]
            alt_price = self.search_response_list[-1]["alt_price"]
        except KeyError:
            print(f"Thers's no flight for {code} even with 1 stopover")

