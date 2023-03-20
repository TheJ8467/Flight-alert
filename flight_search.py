
from data_manager import DataManager
from flight_data import FlightData, Flight
import requests
import os
import time
from notification_manager import NotificationManager

KIWI_ENDPOINT = "https://api.tequila.kiwi.com"
KIWI_API_KEY = os.environ.get("EXPORTED_KIWI_API_KEY")
SHEETY_API_KEY = os.environ.get("EXPORTED_SHEETY_API_KEY")


kiwi_header = {
    "apikey": KIWI_API_KEY,
}

SHEETY_ENDPOINT = "https://api.sheety.co/8e61fad103ee672e340a7289fbc2b7d7/flightDeals8467/users"

sheety_header = {
    "Authorization": SHEETY_API_KEY
}



class FlightSearch:
    #This class is responsible for talking to the Flight Search API.
    def __init__(self):


        flight_data = FlightData()
        data_manager = DataManager()
        self.request = 0
        user_info = requests.get(SHEETY_ENDPOINT, headers=sheety_header)
        user_data_list = user_info.json()["users"]


        for num in range(9):

            try:
                # For saving requests
                # lowest_prices = [1116, 418, 589, 846, 355, 891, 1030, 433]
                if flight_data.best_deal[num] < lowest_prices[num]:

                    self.depart_city = "Incheon"
                    self.depart_IATA = "ICN"
                    self.arrival_city = flight_data.search_response_list[num]["arrival_city"]
                    self.arrival_IATA = flight_data.search_response_list[num]["arrival_IATA"]
                    self.price = flight_data.search_response_list[num]["price"]
                    self.depart_time_UTC = flight_data.search_response_list[num]["depart_time_UTC"]
                    self.arrival_time_UTC = flight_data.search_response_list[num]["arrival_time_UTC"]

                    general_alert = NotificationManager(self.depart_city, self.depart_IATA, self.arrival_city,
                                                               self.arrival_IATA, self.price, self.depart_time_UTC,
                                                               self.arrival_time_UTC)

                    for num in range(len(user_data_list)):
                        general_alert.send_general_email(user_data_list[num]["email"])
                    # general_alert.send_massage()

                else:

                    print(f"There's no special deal with {num} index")
                    flight = Flight()
                    flight_data.search_params["fly_to"] = data_manager.cities[num]
                    flight_data.search_params["max_stopovers"] = flight.stop_overs + 1

                    while True:

                        try:
                            self.alternative_response = requests.get(f"{KIWI_ENDPOINT}/search",
                                                                params=flight_data.search_params,
                                                                headers=kiwi_header)
                            self.alternative_response.raise_for_status()
                        except requests.exceptions.HTTPError as e:
                            if e.response.status_code == 429:
                                self.request += 1
                                print(
                                    f"Too many requests for searching on {num} for replaceable route, waiting for 5 secs, {self.request} requests")
                                time.sleep(5)
                            else:
                                raise e

                        else:

                            flight_data.search_response_list.append({
                                "via_city": self.alternative_response.json()["data"][0]["route"][0]["cityTo"],
                                "alt_price": self.alternative_response.json()["data"][0]["price"],
                                "arrival_city": self.alternative_response.json()["data"][0]["cityTo"],
                                "arrival_IATA":  self.alternative_response.json()["data"][0]["flyTo"],
                                "depart_time_UTC": flight_data.time_converter(self.alternative_response.json()["data"][0]["dTimeUTC"]).strftime(
                        '%m/%d/%Y %I:%M:%S %p'),
                                "arrival_time_UTC": flight_data.time_converter(self.alternative_response.json()["data"][0]["aTimeUTC"]).strftime(
                        '%m/%d/%Y %I:%M:%S %p'),
                            })


                            via_city = flight_data.search_response_list[-1]["via_city"]
                            alt_price = flight_data.search_response_list[-1]["alt_price"]

                            alternative_alert = NotificationManager(self.depart_city, self.depart_IATA,
                                                                    flight_data.search_response_list[num]['arrival_city'],
                                                                    flight_data.search_response_list[num]['arrival_IATA'], self.price,
                                                                    flight_data.search_response_list[num]['depart_time_UTC'],
                                                                    flight_data.search_response_list[num]['arrival_time_UTC'])

                            for num in range(len(user_data_list)):
                                alternative_alert.send_alternative_email(user_data_list[num]["email"], via_city, alt_price)
                            # alternative_alert.alt_message(via_city, alt_price)
                            break

            except IndexError:
                print(f"Error processing search response index {num}: {IndexError}")
                continue
