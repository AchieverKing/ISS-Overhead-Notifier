import time
from datetime import datetime
import smtplib
import requests
import decimal

MY_LAT = 7.348720
MY_LNG = 3.879290
MY_EMAIL = "akdjsjhsk@gmail.com"
PASSWORD = "jjhelulseuilwe"
parameter = {
    "lat": MY_LAT,
    "lng": MY_LNG,
    "formatted": 0,
}

"""generating a random float number for the iss location tracker"""


def float_range(start, stop, step):
    while start < stop:
        yield float(start)
        start += decimal.Decimal(step)


weather = requests.get(url="https://api.sunrise-sunset.org/json", params=parameter)
weather.raise_for_status()
w_data = weather.json()
sunrise = int(w_data["results"]["sunrise"].split("T")[1].split(":")[0])
sunset = int(w_data["results"]["sunset"].split("T")[1].split(":")[0])

time_mow = datetime.now()
current_hour = time_mow.hour

response = requests.get(url="http://api.open-notify.org/iss-now.json")
response.raise_for_status()

data = response.json()
longitude = float(data["iss_position"]["longitude"])
latitude = float(data["iss_position"]["latitude"])


"""if the ISS location is close to my current location"""
my_lat = list(float_range(7, 8, 0.0001))
my_lng = list(float_range(3, 4, 0.0001))
while True:
    time.sleep(60)
    if latitude in my_lat and longitude in my_lng:
        """if it is currently dark"""
        if current_hour >= sunset:
            """send email to tell me to look up"""
            with smtplib.SMTP("smtp.gmail.com") as connection:
                connection.starttls()
                connection.login(user=MY_EMAIL, password=PASSWORD)
                connection.sendmail(from_addr=MY_EMAIL,
                                    to_addrs=MY_EMAIL,
                                    msg=f"subject: ISS is up\n\nLook Up!")
