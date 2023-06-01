# Connected Mirror

The Connected Mirror is a device that allows its user to be informed every day of various informations:

- Date and hour
- Weather: Suoralnshine, Temperature and Humidity
- Real-time commuting time home-work
- News of the day
- Random motivational quote

The principle is as follows: When the user approaches the mirror, our device intercepts the movement using an ultrasonic sensor. From then on, the outdoor temperature, humidity and sunshine data are collected in real time by sensors placed outside the user's home. Then the latest news and a motivational quote are fetched via APIs. Finally, all this information is processed and displayed on the user's mirror. Furthermore, using a push button the user can change the color of the interface.

## Features

- Choose type of news
- Change color
- Fullscreen mode

## Installation

Before processing the installation you need:
- A transparent acrylic glass plate
- A one-way film
- A computer screen
- An HDMI cable
- A Raspberry Pi 3
- Grove Shield for Raspberry
- Sensors
- A push button
- A humidity/temperature sensor
- An ultrasonic sensor
- A light intensity sensor
- An ethernet cable
- A power charger

### Step 1

- Connect the power cable and the ethernet cable to the Raspberry Pi 3.
- Put the Grove Shield on the Raspberry Pi 3 

### Step 2

Connect the various sensors to the Grove shield on the following ports:
- Light intensity sensor: A0
- Humidity/temperature sensor: D2
- Ultrasonic sensor: D3

Connect the following to the Raspberry (not the Grove Shield):
- Computer screen: HDMI port
- Keyboard (not mandatory, see next step): USB port
- Mouse (not mandatory, see next step): USB port

### Step 3

Clone the project on your Raspberry Pi 3

```bash
  git clone git@github.com:bastian-albaut/Connected-mirror.git
```
Update your personnal informations on the file [config.txt](https://github.com/bastian-albaut/Connected-mirror/blob/main/config.txt)

## Run

To run this project type the following command:

```bash
  /bin/python3 /home/pi/Documents/miroir/main.py
```
