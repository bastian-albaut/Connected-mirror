import grovepi
import time
import math

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


def light():
    try:
        # Récupérer l'humidité pour ajouter la pluie
        # Pour récupérer le levé/couché du soleil
        # https://github.com/SatAgro/suntime
        # Pour récupérer latitude / longitude:
        # https://developers.google.com/maps/documentation/geocoding/overview

        sensor_value = grovepi.analogRead(light_sensor)

        if(sensor_value > 15000 or (sensor_value > 350 and "levé ou couché du soleil")):
            return "Soleil"
        else:
            return "Nuage"

    except IOError:
        print("Error")


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


def main():
    if(movementDetection()):
        while(True):
            # tempAndHum = temperatureAndHumidity()
            # temp = tempAndHum[0]
            # hum = tempAndHum[1]
            # print("temp = %.02f C humidity = %.02f%%" % (temp, hum))
            sensor_value = light()
            print("sensor_value = %d" % sensor_value)
            # print("sensor_value = %d resistance = %.2f" %
            #   (sensor_value,  resistance))

            # if(buttonDetection2()) { 2eme boutton poussoire
            #     Changer l'affichage du lcd
            # }
            time.sleep(30)


main()
