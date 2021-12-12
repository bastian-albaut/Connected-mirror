import grovepi
import time
import math
import datetime
from suntime import Sun, SunTimeException
import requests
from driverI2C import *
import pytz


# set I2C to use the hardware bus
grovepi.set_bus("RPI_1")

ultrasonic_ranger = 3  # The Ultrasonic Ranger goes on digital port D3
sensor = 2  # The Sensor goes on digital port D2
light_sensor = 0  # The Light Sensor on analog port A0
led = 4  # The LED on digital port D4
button = 6  # The Grove Button on digital port D6

grovepi.pinMode(light_sensor, "INPUT")
grovepi.pinMode(led, "OUTPUT")
grovepi.pinMode(button, "INPUT")


def distance():
    try:
        # Read distance value from Ultrasonic
        return grovepi.ultrasonicRead(ultrasonic_ranger)

    except Exception as e:
        print("Error:{}".format(e))


def movementDetection():
    mvtDetected = False
    dist1 = distance()
    while not mvtDetected:
        dist2 = distance()
        print("Distance mesurée = %.1f cm" % dist2)
        if(abs(dist1-dist2) > 25):
            mvtDetected = True
        time.sleep(0.1)  # don't overload the i2c bus
    return True


# temp_humidity_sensor_type
# Grove Base Kit comes with the blue sensor.
blue = 0    # The Blue colored sensor.
white = 1   # The White colored sensor.

def temperatureAndHumidity():
    try:
        # This example uses the blue colored sensor.
        # The first parameter is the port, the second parameter is the type of sensor.
        [temp, humidity] = grovepi.dht(sensor, blue)
        if math.isnan(temp) == False and math.isnan(humidity) == False:
            return [temp, humidity]
    except IOError:
        print("Error")


# Turn on LED once sensor exceeds threshold resistance
threshold = 10

# def getLatitudeLongitude():
#     response = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address=1600+Amphitheatre+Parkway,+Mountain+View,+CA')
#     resp_json_payload = response.json()
#     print(resp_json_payload['results'][0]['geometry']['location'])


def getSunriseSunset():
    latitude = 43.37
    longitude = 03.52

    sun = Sun(latitude, longitude)

    # Get today's sunrise and sunset in UTC
    today_sr = sun.get_sunrise_time()
    today_ss = sun.get_sunset_time()
    return {"sunrise": today_sr, "sunset": today_ss}
    # print('Today at Warsaw the sun raised at {} and get down at {} UTC'.
    #   format(today_sr.strftime('%H:%M'), today_ss.strftime('%H:%M')))


def isSunrise(sunrise):
    # Récupérer l'heure actuelle
    current_time = datetime.datetime.now()
    current_time = pytz.utc.localize(current_time)
    afterSunrise = sunrise + datetime.timedelta(minutes=30)
    print(type(current_time))
    return current_time < afterSunrise and current_time >= sunrise


def isSunset(sunset):
    # Récupérer l'heure actuelle
    current_time = datetime.datetime.now()
    current_time = pytz.utc.localize(current_time)
    beforeSunset = sunset - datetime.timedelta(minutes=30)

    return current_time > beforeSunset and current_time <= sunset


def light():
    try:
        # Récupérer l'humidité pour ajouter la pluie

        sunriseAndSunset = getSunriseSunset()

        sensor_value = grovepi.analogRead(light_sensor)

        if(sensor_value > 15000 or (sensor_value > 350 and (isSunrise(sunriseAndSunset["sunrise"]) or isSunset(sunriseAndSunset["sunset"])))):
            return "Soleil"
        else:
            return "Nuage"

    except IOError:
        print("Error")

def traffic():
    homeAdress = "Montpellier"
    workAdress = "Toulouse"
    key = "AIzaSyDFPpnVB6UO9Zu2rbDvGP-scDnakK_dFd8"
    url = "https://maps.googleapis.com/maps/api/distancematrix/json?"
    request = requests.get(url + "origins=" + homeAdress + "&destinations=" + workAdress + "&language=fr" + "&key=" + key)

    return request.json()["rows"][0]["elements"][0]["duration"]["text"]

def getData():
    tempAndHum = temperatureAndHumidity()
    return {
        "temperature" : tempAndHum[0],
        "humidity" : tempAndHum[1],
        "weather" : light(),
        "traffic" : traffic(),
    }

def pushButton():
    try:
        return grovepi.digitalRead(button)
    except IOError:
        print("Error")


def buttonDetection():
    btnDetected = False
    btnState = pushButton()
    while not btnDetected:
        btnState2 = pushButton()
        print("Etat du bouton = %d" % btnState2)
        if btnState2 != btnState:
            btnDetected = True
        time.sleep(0.5)  # don't overload the i2c bus
    return True


def displayInformations(data):
    setText(data["temperature"])
    setText(data["weather"])
    setText(data["humidity"])
    setText(data["traffic"])

def main():
    while(movementDetection()):
        # Récupération des données via les capteurs
        data = getData()

        # Affichage des données
        displayInformations(data)

        # print("temp = %.02f C humidity = %.02f%%" % (temp, hum))

        time.sleep(30)

    if(buttonDetection()):
        setRGB(15,227,20) # Affichage en vert


main()
