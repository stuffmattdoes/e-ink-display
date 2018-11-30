# E-Ink Calendar Display

# Setup
## Linux Dependencies
`sudo apt-get update`
`sudo apt-get install`

**Pillow dependencies**
`sudo apt-get install libjpeg-dev zlib1g-dev`
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
(WaveShare E-Ink 7.5" Display Wiki)[https://www.waveshare.com/wiki/7.5inch_e-Paper_HAT]
(WaveShare E-Ink 7.5" Display Drivers)[https://www.waveshare.com/wiki/Pioneer600#Libraries_Installation_for_RPi]
(Google Calendar API Authentication)[https://developers.google.com/identity/protocols/OAuth2ForDevices#allowedscopes]
(Google Calendar API)[https://developers.google.com/calendar/v3/reference/events/list?apix_params=%7B%22calendarId%22%3A%22lkopeh0sr1m9svqcggd0pms2ug%40group.calendar.google.com%22%2C%22orderBy%22%3A%22startTime%22%7D]
(Cron job for Raspberry Pi)[https://www.dexterindustries.com/howto/auto-run-python-programs-on-the-raspberry-pi/]

# TODO:
[ ] event['start']['dateTime'] & event['end']['dateTime'] may span a few days
[ ] On multi-day event, if date is start day, display "Starts @ 7:30AM"
[ ] On multi-day event, if date is end day, display "Ends @ 10:30PM"
[x] Show "Today" & populate accordingly
[ ] Show "X more events this week"