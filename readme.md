# E-Ink Calendar Display
I've built an E-Ink Calendar Display to show my upcoming Google Calendar events in a nice picture frame, hung on the wall.

![Chicken cat helping me with the Raspberry Pi E-Ink Calendar Display](./img/chicken_calendar.jpg)

I had a [Raspberry Pi 3b](https://www.raspberrypi.org/products/raspberry-pi-3-model-b/) lying around that I wanted to do something with. Once I caught wind of the [Waveshare E-Ink Display](https://www.waveshare.com/7.5inch-e-paper-hat.htm), I thought this would be a great application for it.

E-Ink is the same screen technology used in Amazon's Kindle devices. E-Ink screens are composed of millions of tiny black & white particles, charged according to their color and resting just beneath the glass display screen. When exposed to a complex electric field, the particles are pulled towards or pushed away from the surface of the screen, resulting in variations of black and white pixels that compose an image. E-Ink displays don't need any current to maintain an image, which is one of their unique characteristics. Its refresh rate is very slow, however - taking seconds to render new images. This does not make them ideal for displaying videos or for high-frequency interaction like we have in phones. Read more abou E-Ink technology [here](https://www.eink.com/electronic-ink.html).

Think of it as a high-tech Etch-a-Sketch!

# Setup
**Linux Dependencies**
`sudo apt-get update` to update package list
`sudo apt-get install` the following Linux libraries:
* `libjpeg-dev`
* `zlib1g-dev`

**E-Ink Display dependencies**
- `python-smbus`
- `python-serial`
- `python-imaging`
- `python-rpi.gpio`
- `wiringpi`
- `python-spidev`

**Python Dependencies**
`pip install` the following Python libraries:
- `Pillow`
- `RPi.GPIO`
- `requests`
- `spidev`

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
`0 8-23 * * * cd /home/pi/python_programs/pi-cal/src && python3 pi-cal.py`
to run a cronjob every hour from 8AM to 11PM

# TODO:
* [ ] event['start']['dateTime'] & event['end']['dateTime'] may span a few days
* [ ] On multi-day event, if date is start day, display "Starts @ 7:30AM"
* [ ] On multi-day event, if date is end day, display "Ends @ 10:30PM"
* [x] Show "Today" & populate accordingly
* [ ] Show "X more events this week"
