import grovepi
import time
import math

# set I2C to use the hardware bus
grovepi.set_bus("RPI_1")

ultrasonic_ranger = 3  # The Ultrasonic Ranger goes on digital port D3
sensor = 2  # The Sensor goes on digital port D2


def distance():
    try:
        # Read distance value from Ultrasonic
        return grovepi.ultrasonicRead(ultrasonic_ranger)

    except Exception as e:
        print("Error:{}".format(e))


def MovementDetection():
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


def main():
    if(MovementDetection()):
        tempAndHum = temperatureAndHumidity()
        temp = tempAndHum[0]
        hum = tempAndHum[1]
        print("temp = %.02f C humidity = %.02f%%" % (temp, hum))


main()
