import grovepi
import time
import math
import datetime
from suntime import Sun, SunTimeException
import requests
from driverI2C import *
import pytz
import random
from googletrans import Translator
from flask import Flask, render_template

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
    print("En attente d'un mouvement...")
    dist1 = distance()
    print("Distance de départ = %.1f cm" % dist1)
    while not mvtDetected:
        dist2 = distance()
        print("Distance mesurée = %.1f cm" % dist2)
        if(abs(dist1-dist2) > 40):
            mvtDetected = True
        time.sleep(0.5)  # don't overload the i2c bus
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
        if(sensor_value > 10000 or (sensor_value > 350 and (isSunrise(sunriseAndSunset["sunrise"]) or isSunset(sunriseAndSunset["sunset"])))):
            return "Ensoleillé"
        else:
            return "Nuageux"

    except IOError:
        print("Error")


def traffic(homeAdress, workAdress):
    key = "AIzaSyDFPpnVB6UO9Zu2rbDvGP-scDnakK_dFd8"
    url = "https://maps.googleapis.com/maps/api/distancematrix/json?origins=" + \
        homeAdress + "&destinations=" + workAdress + "&language=fr" + "&key=" + key

    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)

    return response.json()["rows"][0]["elements"][0]["duration"]["text"]


def randomQuote():
    # making the get request
    response = requests.get(
        "http://api.quotable.io/random?maxLength=120")
    if response.status_code == 200:
        # extracting the core data
        data = response.json()
        translator = Translator()
        translate_text = translator.translate(data['content'], dest='fr')
        random_quote = translate_text.text
        author = data['author']

        return {
            "quote": random_quote,
            "author": author
        }
    else:
        print("Error while getting quote")


def dayNews(categoryNews):
    numberofNews = 2
    key = "1947a8a49b8a3d3adb51d97d8f458c1d"
    url = "http://api.mediastack.com/v1/news?access_key=" + \
        key + "&countries=fr&languages=fr&sort=published_desc&categories=-" + \
        categoryNews

    response = requests.request("GET", url)
    listNews = {}
    i = 0
    n = 0
    while(i < numberofNews):
        if response.json()["data"][n]["title"] != response.json()["data"][n]["description"]:
            listNews["news{0}".format(i)] = {
                "title": response.json()["data"][n]["title"],
                "description": response.json()["data"][n]["description"],
                "image": response.json()["data"][n]["image"],
                "source": response.json()["data"][n]["source"]
            }
            i += 1
        n += 1

    return listNews


def getData(homeAdress, workAdress, categoryNews):
    tempAndHum = temperatureAndHumidity()
    return {
        "temperature": tempAndHum[0],
        "humidity": tempAndHum[1],
        "weather": light(),
        "traffic": traffic(homeAdress, workAdress),
        "quoteWithAuthor": randomQuote(),
        "listNews": dayNews(categoryNews),
        "datetime": datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
    }


def getDataClient():
    filin = open("/home/pi/Documents/miroir/config.txt", "r")
    lignes = filin.readlines()
    i = 1
    data = ""
    for ligne in lignes:
        if i % 2 == 0:
            data += ligne
        i += 1
    return data


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
    print("News:")
    setText("News:")
    print(data["listNews"]["news0"]["title"] + "\n" +
          data["listNews"]["news0"]["description"])
    print(data["listNews"]["news1"]["title"] + "\n" +
          data["listNews"]["news1"]["description"])
    # time.sleep(4)
    # print("Citation: " + data["quoteWithAuthor"]["quote"])
    # print("Auteur: " + data["quoteWithAuthor"]["author"])
    # setText("Citation: " + data["quoteWithAuthor"]["quote"])
    # setText("Auteur: " + data["quoteWithAuthor"]["author"])
    # time.sleep(4)
    # print("temperature:%.02f" % data["temperature"])
    # setText("temperature:%.02f" % data["temperature"])
    # time.sleep(4)
    # print("Meteo:" + data["weather"])
    # setText("Meteo:" + data["weather"])
    # time.sleep(4)
    # print("Humidite:%.02f" % data["humidity"])
    # setText("Humidite:%.02f" % data["humidity"])
    # time.sleep(4)
    # print("Temps trajet:" + data["traffic"])
    # setText("Temps trajet:" + data["traffic"])


def flaskApplication(data, colorClient):

    print("Affichage de l'écran sur le mirroir en cours...")
    # setText("Affichage de l'écran sur le mirroir en cours...")

    app = Flask(__name__)

    @app.route('/')
    @app.route('/index')
    def index():
        return render_template('index.html', data=data, color=colorClient)

    if __name__ == "__main__":
        app.run()


def setColor():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    setRGB(r, g, b)


def main():
    dataClient = getDataClient()
    homeAdress = dataClient.splitlines()[0]
    workAdress = dataClient.splitlines()[1]
    colorClient = dataClient.splitlines()[2]
    categoryNews = dataClient.splitlines()[3]
    print(categoryNews)
    setColor()
    # if(movementDetection()):
    # Récupération des données via les capteurs/api
    data = getData(homeAdress, workAdress, categoryNews)

    # Affichage des données sur le lcd
    displayInformations(data)

    # Création de l'app web et affichage
    flaskApplication(data, colorClient)


main()
