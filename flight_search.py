import sys
from data_manager import DataManager
from flight_data import FlightData
import requests
import time
from notification_manager import NotificationManager

class FlightSearch:
    #This class is responsible for talking to the Flight Search API.

    def __init__(self):
        self.flight_data = FlightData()
        self.data_manager = DataManager()
        self.request = 0
        self.via_city = ''
        self.depart_city = "Incheon"
        self.depart_IATA = "ICN"

        self.search_flights()

    def search_flights(self):
        for num, (deal, sheety_price) in enumerate(zip(self.flight_data.best_deal, self.data_manager.sheety_prices['prices'])):
            if deal < sheety_price["lowestPrice"]:
                self.send_general_alert(num)
            else:
                self.search_alternative_flights(num)

    def send_general_alert(self, num):
        arrival_city = self.flight_data.search_response_list[num]["arrival_city"]
        arrival_IATA = self.flight_data.search_response_list[num]["arrival_IATA"]
        price = self.flight_data.search_response_list[num]["price"]
        depart_time_UTC = self.flight_data.search_response_list[num]["depart_time_UTC"]
        arrival_time_UTC = self.flight_data.search_response_list[num]["arrival_time_UTC"]

        general_alert = NotificationManager(self.depart_city, self.depart_IATA, arrival_city,
                                            arrival_IATA, price, depart_time_UTC,
                                            arrival_time_UTC)

        for user in self.data_manager.sheety_users['users']:
            general_alert.send_general_email(user["email"])

    def search_alternative_flights(self, num):
        while True:
            try:
                self.flight_data.alt_request(self.data_manager.cities[num])
            except requests.exceptions.HTTPError as e:
                if e.response.status_code == 429:
                    self.request += 1
                    print(
                        f"Too many requests for searching on {num} for replaceable route, waiting for 5 secs, {self.request} requests")
                    time.sleep(5)
                else:
                    raise e
            else:
                if self.flight_data.via_city != '':
                    self.send_alternative_alert(num)
                    break
                else:
                    break

    def send_alternative_alert(self, num):
        arrival_city = self.flight_data.search_response_list[num]['arrival_city']
        arrival_IATA = self.flight_data.search_response_list[num]['arrival_IATA']
        price = self.flight_data.search_response_list[num]['price']
        depart_time_UTC = self.flight_data.search_response_list[num]['depart_time_UTC']
        arrival_time_UTC = self.flight_data.search_response_list[num]['arrival_time_UTC']

        alternative_alert = NotificationManager(self.depart_city, self.depart_IATA,
                                                arrival_city, arrival_IATA, price,
                                                depart_time_UTC, arrival_time_UTC)

        for user in self.data_manager.sheety_users['users']:
            alternative_alert.send_alternative_email(user["email"], self.flight_data.via_city, self.flight_data.alt_price)
