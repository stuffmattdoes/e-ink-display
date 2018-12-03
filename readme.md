# E-Ink Calendar Display
I've built an E-Ink Calendar Display to show my upcoming Google Calendar events in a nice picture frame, hung on the wall.

![Chicken cat helping me with the Raspberry Pi E-Ink Calendar Display](./img/chicken_calendar.jpg)

I had a [Raspberry Pi 3b](https://www.raspberrypi.org/products/raspberry-pi-3-model-b/) lying around that I wanted to do something with. Once I caught wind of the [Waveshare E-Ink Display](https://www.waveshare.com/7.5inch-e-paper-hat.htm), I thought this would be a great application for it.

If you're unfamiliar with what an E-Ink display is, it is the same screen technology used in Amazon's Kindle devices. Its refresh rate is very slow, which does not make it ideal for showing quick imagery or videos; however, it doesn't need any current to maintain an image on its display. Think of it as a high-tech Etch-a-Sketch.

# Setup
## Linux Dependencies
`sudo apt-get update` to update package list
`sudo apt-get install` the following libraries:

**Pillow dependencies**
* `libjpeg-dev`
* `zlib1g-dev`
<!-- - jpeg-dev
- zlib-dev
- freetype-dev
- lcms2-dev
- openjpeg-dev
- tiff-dev
- tk-dev
- tcl-dev -->

<!-- - python3-dev
- python3-setuptools
- libtiff4-dev
- libjpeg8-dev
- zlib1g-dev 
- libfreetype6-dev
- liblcms2-dev
- libwebp-dev
- tcl8.5-dev
- tk8.5-dev
- python-tk -->

<!-- - python-dev -->
**E-Ink Display dependencies**
- python-smbus
- python-serial
- python-imaging
- python-rpi.gpio
- wiringpi
- python-spidev
- fonts-freefont-ttf

**Python Dependencies**
- google-api-python-client
- oauth2client
- pillow

# Resources
* [WaveShare E-Ink 7.5" Display Wiki](https://www.waveshare.com/wiki/7.5inch_e-Paper_HAT)
* [WaveShare E-Ink 7.5" Display Drivers](https://www.waveshare.com/wiki/Pioneer600#Libraries_Installation_for_RPi)
* [Google Calendar API Authentication](https://developers.google.com/identity/protocols/OAuth2ForDevices#allowedscopes)
* [Google Calendar API](https://developers.google.com/calendar/v3/reference/events/list?apix_params=%7B%22calendarId%22%3A%22lkopeh0sr1m9svqcggd0pms2ug%40group.calendar.google.com%22%2C%22orderBy%22%3A%22startTime%22%7D)
* [openweathermap.org API](https://openweathermap.org/current#list)
* [openweathermap.org Weather Conditions](https://openweathermap.org/weather-conditions)

# Cronjob
`crontab -e`
and enter
`0 8-0 * * * cd /home/pi/python_programs/pi-cal/src && python3 pi-cal.py`
to run a cronjob every hour from 8AM to midnight

# TODO:
* [ ] event['start']['dateTime'] & event['end']['dateTime'] may span a few days
* [ ] On multi-day event, if date is start day, display "Starts @ 7:30AM"
* [ ] On multi-day event, if date is end day, display "Ends @ 10:30PM"
* [x] Show "Today" & populate accordingly
* [ ] Show "X more events this week"