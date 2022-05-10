from datetime import datetime
import smtplib
import requests
import time

MY_EMAIL = "akdjsjhsk@gmail.com"
PASSWORD = "jjhelulseuilwe"
MY_LAT = 7.348720
MY_LNG = 3.879290
parameter = {
    "lat": MY_LAT,
    "lng": MY_LNG,
    "formatted": 0,
}


def is_night():
    weather = requests.get(url="https://api.sunrise-sunset.org/json", params=parameter)
    weather.raise_for_status()
    w_data = weather.json()
    sunrise = int(w_data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(w_data["results"]["sunset"].split("T")[1].split(":")[0])

    time_mow = datetime.now()
    current_hour = time_mow.hour
    if current_hour >= sunset or current_hour <= sunrise:
        return True


def iss_overhead():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()

    data = response.json()
    longitude = float(data["iss_position"]["longitude"])
    latitude = float(data["iss_position"]["latitude"])
    """if my location is withing +5 or -5 degree of the iss current location"""
    if MY_LAT - 5 <= latitude <= MY_LAT + 5 and MY_LNG - 5 <= longitude <= MY_LNG + 5:
        return True


while True:
    time.sleep(60)
    if iss_overhead() and iss_overhead():
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=MY_EMAIL, password=PASSWORD)
            connection.sendmail(from_addr=MY_EMAIL,
                                to_addrs=MY_EMAIL,
                                msg=f"subject: ISS is up\n\nLook Up!")
