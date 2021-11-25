import grovepi
import time

# set I2C to use the hardware bus
grovepi.set_bus("RPI_1")

# Connect the Grove Ultrasonic Ranger to digital port D3
# SIG,NC,VCC,GND
ultrasonic_ranger = 3


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

MovementDetection()
