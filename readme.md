# E-Ink Calendar Display

# Setup
## Linux Dependencies
`sudo apt-get update`
`sudo apt-get install`
*Pillow dependencies*
- python3-dev
- python3-setuptools
- libtiff4-dev
- libjpeg8-dev
- zlib1g-dev 
- libfreetype6-dev
- liblcms2-dev
- libwebp-dev
- tcl8.5-dev
- tk8.5-dev
- python-tk

<!-- - python-dev -->
- python-smbus
- python-serial
- python-imaging
- python-rpi.gpio
- wiringpi
- python-spidev
- fonts-freefont-ttf

## Python Dependencies
- google-api-python-client
- oauth2client
- pillow

# Auth
POST
`https://accounts.google.com/o/oauth2/device/code`
`client_id: 635286573706-22bvqd3vc034afg5vn9nopi6n6jed7sn.apps.googleusercontent.com`
`scope: https://www.googleapis.com/auth/calendar.readonly`

# Resources
(WaveShare E-Ink 7.5" Display Wiki)[https://www.waveshare.com/wiki/7.5inch_e-Paper_HAT]
(WaveShare E-Ink 7.5" Display Drivers)[https://www.waveshare.com/wiki/Pioneer600#Libraries_Installation_for_RPi]
(Google Calendar API Authentication)[https://developers.google.com/identity/protocols/OAuth2ForDevices#allowedscopes]

# TODO
- `virtualenv` doesn't take into consideration OS package dependencies i.e. `jpeg` for `Pillow`. Use Docker?