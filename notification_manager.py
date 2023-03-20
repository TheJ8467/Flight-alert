from twilio.rest import Client
import os
from dotenv import load_dotenv
import smtplib

load_dotenv()

TWILLIO_SID = os.environ.get("EXPORTED_TWILLIO_SID")
TWILLIO_AUTH_TOKEN = os.environ.get("EXPORTED_TWILLIO_AUTH_TOKEN")

account_sid = TWILLIO_SID
auth_token = TWILLIO_AUTH_TOKEN

client = Client(account_sid, auth_token)

class NotificationManager():
    #This class is responsible for sending notifications with the deal flight details.
    def __init__(self, depart_city, depart_IATA, arrival_city, arrival_IATA, price, depart_time_UTC, arrival_time_UTC):
        self.depart_city = depart_city
        self.depart_IATA = depart_IATA
        self.arrival_city = arrival_city
        self.arrival_IATA = arrival_IATA
        self.price = price
        self.depart_time_UTC = depart_time_UTC
        self.arrival_time_UTC = arrival_time_UTC


    def send_massage(self):

        message = client.messages \
            .create(
            body=f"Nice deal alert!\n"
                 f"{self.depart_city}({self.depart_IATA}) to {self.arrival_city} ({self.arrival_IATA})\n"
                 f"Price: {self.price}\n"
                 f"TOD: {self.depart_time_UTC}(UTC)\n"
                 f"TOA: {self.arrival_time_UTC}(UTC)\n",
            from_='+15673716735',
            to='+821094395262'
        )

        print(message.sid)

    def alt_message(self, via_city, alt_price):

        self.via_city = via_city
        self.alt_price = alt_price

        message = client.messages \
            .create(
            body=f"Nice deal alert!\n"
                 f"{self.depart_city}({self.depart_IATA}) to {self.arrival_city}({self.arrival_IATA})\n via {self.via_city}\n"
                 f"Price: {self.alt_price}\n"
                 f"TOD: {self.depart_time_UTC}(UTC)\n"
                 f"TOA: {self.arrival_time_UTC}(UTC)\n",
            from_='+15673716735',
            to='+821094395262'
        )

        print(message.sid)

    def send_general_email(self, receiver):

        my_email = "bgkt211@gmail.com"
        password = "uuzxyupaignnurbq"

        with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
            connection.starttls()
            connection.login(user=my_email, password=password)
            connection.sendmail(
                from_addr=my_email,
                to_addrs=receiver,
                msg=f"Subject:Nice deal found!"
                    f"\n\n{self.depart_city}({self.depart_IATA}) to {self.arrival_city} ({self.arrival_IATA})\n"
                    f"Price: {self.price}\n"
                    f"TOD: {self.depart_time_UTC}(UTC)\n"
                    f"TOA: {self.arrival_time_UTC}(UTC)\n"
                .encode('utf-8')
            )

    def send_alternative_email(self, receiver, via_city, alt_price):

        my_email = "bgkt211@gmail.com"
        password = "uuzxyupaignnurbq"
        self.via_city = via_city
        self.alt_price = alt_price

        with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
            connection.starttls()
            connection.login(user=my_email, password=password)
            connection.sendmail(
                from_addr=my_email,
                to_addrs=receiver,
                msg=f"Subject:Nice deal found!"
                    f"\n\n{self.depart_city}({self.depart_IATA}) to {self.arrival_city}({self.arrival_IATA})\n via {self.via_city}\n"
                    f"Price: {self.alt_price}\n"
                    f"TOD: {self.depart_time_UTC}(UTC)\n"
                    f"TOA: {self.arrival_time_UTC}(UTC)\n".encode('utf-8')
            )


