# main

# TODO:
# - event['start']['dateTime'] & event['end']['dateTime'] may span a few days
# - On multi-day event, if date is start day, display "Starts @ 7:30AM"
# - On multi-day event, if date is end day, display "Ends @ 10:30PM"
# - Show "Today" & populate accordingly
# - Show "X more events this week"

import calendar
import epd7in5
import datetime
import json
# import os
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from pprint import pprint
import requests
# import sys
import time

# print(os.getcwd())  # current working directory, absolute path
# print(sys.argv[0])  # working directory

def main():
    print('main')
    init()
    
    with open('./credentials.json') as f:
        global creds
        creds = json.load(f)

    # try:
    #     with open('./token.json') as f:
    #         global token
    #         token = f
    # except:
    #     auth()

    # Auth.auth_request()
    # Auth.auth_poll()
    Auth().auth_refresh()

    Events().fetch_events()
    Draws().draw_calendar()
    Draws().draw_date()
    Draws().draw_events()
    render()

def init():
    global EPD_WIDTH
    EPD_WIDTH = 640
    global EPD_HEIGHT
    EPD_HEIGHT = 384

    # Initialize E-Paper Display inferface
    global epd
    epd = epd7in5.EPD()
    epd.init()

    # For simplicity, the arguments are explicit numerical coordinates
    global image
    image = Image.new('1', (EPD_WIDTH, EPD_HEIGHT), 1)    # 1: clear the frame
    global draw
    draw = ImageDraw.Draw(image)

class Auth:
    print('auth')

    auth_response = None
    device_code = None

    def auth_request(self):
        print('auth request')
        global creds

        # Initial request
        auth_response = requests.post(creds['auth_url'], data = {
            'client_id': creds['client_id'],
            'scope': creds['scopes']
        }).json()

        # {
        #   'device_code': 'AH-1Ng1BzvzcVPXWrakudSRlaBkKTm5otqDWNT0u0p5J9mjXR1hMiS-rUS5D7Ss7LvDvAumcQReo_ME9N30vcEWiLbMQq0ORCw',
        #   'expires_in': 1800,
        #   'interval': 5,
        #   'user_code': 'KQTW-SDMD',
        #   'verification_url': 'https://www.google.com/device'
        # }

        device_code = auth_response['device_code']

        # Render device auth codes
        group_top = 116

        draw.text((24, group_top), 'Visit', font = getFont(18, 'Regular'), fill = 0)
        draw.text((24, 32 + group_top), auth_response['verification_url'], font = getFont(24, 'Bold'), fill = 0)
        draw.text((24, 90 + group_top), 'and enter', font = getFont(18, 'Regular'), fill = 0)
        draw.text((24, 122 + group_top), auth_response['user_code'], font = getFont(32, 'Bold'), fill = 0)

        render()

    def auth_poll(self):
        print('auth poll')
        global creds
        
        # Poll Google API for auth confirmation token (after user accepts on separate device)
        # interval = auth_response['interval']
        interval = 30
        time.sleep(interval)

        def request_token():
            # Token polling
            return requests.post(creds['token_url'], data = {
                'client_id': creds['client_id'],
                'client_secret': creds['client_secret'],
                'code': creds['device_code'],
                'grant_type': creds['grant_type']
            })

        token_response = request_token()

        # {
        #     "access_token":"1/fFAGRNJru1FTz70BzhT3Zg",
        #     "expires_in":3920,
        #     "token_type":"Bearer",
        #     "refresh_token":"1/xEoDL4iW3cxlI7yDbSRFYNG01kVKM2C-259HOF2aQbI"
        # }

        i = 0

        while i < auth_response['expires_in'] and not token_response.ok:
            token_response = request_token()

            if token_response.ok:
                break
            # elif token_response == 403 or token_response == 400
            else:
                time.sleep(interval)
                i += interval

        # Store token
        print('success!')
        
        with open('token.json', 'w') as fp:
            json.dump(token_response.json(), fp)

    def auth_refresh(self):
        print('auth refresh')

        refresh_token = requests.post(creds['refresh_url'], data = {
            'client_id': creds['client_id'],
            'client_secret': creds['client_secret'],
            'grant_type': 'refresh_token',
            'refresh_token': creds['refresh_token']
        }).json()

        # {
        #     "access_token":"1/fFAGRNJru1FTz70BzhT3Zg",
        #     "expires_in":3920,
        #     "token_type":"Bearer"
        # }

        global token
        token = refresh_token

        with open('token.json', 'w') as fp:
            json.dump(refresh_token, fp)

class Events:
    def fetch_events(self):
        print('fetch events')
        global creds
        global events
        global token

        events_url = 'https://www.googleapis.com/calendar/v3/calendars/{}/events'.format(creds['calendar_id'])
        now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time

        events_response = requests.get(events_url, 
            headers = {
                'Authorization': '{} {}'.format(token['token_type'], token['access_token'])
            },
            params = {
                'maxResults': 10,
                'orderBy': 'startTime',
                'singleEvents': True,
                'timeMin': now
            }
        ).json()['items']

        events = self.format_events(events_response)

    def format_events(self, events):
        print('format_events')
        events_format = {}

        for event in events:
            event_YMD = ''

            # Get our date, formatted as YYYY-MM-DD
            try:
                event_YMD = datetime.datetime.strptime(event['start']['dateTime'][0:10], '%Y-%m-%d').strftime('%Y-%m-%d')
            except:
                event_YMD = datetime.datetime.strptime(event['start']['date'][0:10], '%Y-%m-%d').strftime('%Y-%m-%d')

            # Format a new dictionary with the date as key & events list as value
            try:
                events_format[event_YMD].append(event)
            except:
                events_format[event_YMD] = [event]

        return events_format

def getFont(size, weight):
        return ImageFont.truetype('/home/pi/python_programs/pi-cal/src/fonts/OpenSans-{}.ttf'.format(weight), size)

class Draws():
    print('draw')
    
    def draw_calendar(self):
        print('draw calendar')

        now = datetime.datetime.now()
        today = now.day
        year = now.year
        month = now.month
        month_str = now.strftime('%B')
        calendar_top = 200


        # calendar.setfirstweekday(calendar.SUNDAY)
        cal = calendar.Calendar(calendar.SUNDAY)
        days_in_weeks = cal.monthdayscalendar(year, month)

        # Title
        draw.text((24, calendar_top), '{} {}'.format(month_str, year), font = getFont(20, 'Regular'), fill = 0)
        
        # Weekdays
        draw.text((24, 30 + calendar_top), 'Su', font = getFont(18, 'Bold'), fill = 0)
        draw.text((56, 30 + calendar_top), 'M', font = getFont(18, 'Bold'), fill = 0)
        draw.text((82, 30 + calendar_top), 'T', font = getFont(18, 'Bold'), fill = 0)
        draw.text((112, 30 + calendar_top), 'W', font = getFont(18, 'Bold'), fill = 0)
        draw.text((138, 30 + calendar_top), 'Th', font = getFont(18, 'Bold'), fill = 0)
        draw.text((168, 30 + calendar_top), 'F', font = getFont(18, 'Bold'), fill = 0)
        draw.text((194, 30 + calendar_top), 'S', font = getFont(18, 'Bold'), fill = 0)

        date_height = 0

        # Weeks
        for week in days_in_weeks:
            date_spacing = 0

            for day in week:
                day_text = day

                if day == today:
                    draw.rectangle((
                        20 + date_spacing,                   # x0
                        56 + calendar_top + date_height,     # y0
                        46 + date_spacing,                  # x1
                        76  + calendar_top + date_height),  # y1
                    fill = 0)
                    font_weight = 'Bold'
                    font_fill = 255
                else:
                    font_weight = 'Regular'
                    font_fill = 0

                if day == 0:
                    day_text = '-'
                
                draw.text((24 + date_spacing, 56 + calendar_top + date_height), str(day_text), font = getFont(15, font_weight), fill = font_fill)
                date_spacing += 28
            
            date_height += 22
    
    def draw_date(self):
        print('draw date')
        day = datetime.datetime.now().strftime('%A')
        date = datetime.datetime.now().strftime('%-d')

        draw.text((24, 8), day, font = getFont(32, 'Regular'), fill = 0)
        draw.text((24, 8), date, font = getFont(148, 'Regular'), fill = 0)

    def draw_events(self):
        print('draw events')
        global events
        line_height = 16

        # Render "Today"
        draw.text((260, 16), 'TODAY', font = getFont(15, 'Regular'), fill = 0)   # Day
        draw.text((325, 16), 'Not much going on!', font = getFont(15, 'Italic'), fill = 0)  # Details

        # Sort formatted events by date
        dates_sort = [ datetime.datetime.strptime(event_key, '%Y-%m-%d') for event_key in events.keys() ]
        dates_sort.sort()
        dates_sort = [ datetime.datetime.strftime(date_key, '%Y-%m-%d') for date_key in dates_sort ]

        for date in dates_sort:
            # Event Group Date
            event_datetime = datetime.datetime.strptime(date, '%Y-%m-%d')
            event_date = event_datetime.strftime('%d')
            event_day = event_datetime.strftime('%a').upper()

            # If event isn't this week or month
            event_week = event_datetime.strftime('%U')
            event_month = event_datetime.strftime('%b').upper()

            if event_week != datetime.datetime.now().strftime('%U'):
                week_day = int(event_datetime.strftime('%w'))
                week_of = 6 - week_day

                draw.text((325, 36 + line_height), event_month, font = getFont(15, 'Regular'), fill = 0)   # Month
                line_height += 16

            # Draw date & day
            draw.text((255, 36 + line_height), event_date, font = getFont(42, 'Regular'), fill = 0)   # Date
            draw.text((260, 88 + line_height), event_day, font = getFont(15, 'Regular'), fill = 0)   # Day

            for event in events[date]:
                # print(event['summary'])
                event_summary = event['summary']

                # Event Location
                try:
                    event_location = '@ ' + event['location']
                except:
                    event_location = ''

                # Time
                try:
                    # print('try')
                    event_datetime_start = datetime.datetime.strptime(event['start']['dateTime'][0:19], '%Y-%m-%dT%H:%M:%S')
                    event_datetime_end = datetime.datetime.strptime(event['end']['dateTime'][0:19], '%Y-%m-%dT%H:%M:%S')
                    event_time_start = event_datetime_start.strftime('%-I') + ':' + event_datetime_start.strftime('%M') + event_datetime_start.strftime('%p')       # "7:30AM'
                    event_time_end = event_datetime_end.strftime('%-I') + ':' + event_datetime_end.strftime('%M') + event_datetime_end.strftime('%p')     # "10:30PM"

                    # For multi-day events
                    if event['start']['dateTime'][0:10] == event['end']['dateTime'][0:10]:
                        # print('Same day')
                        event_time = '{} - {} '.format(event_time_start, event_time_end)     # "7:30AM - 10:45PM"

                    else :
                        # print('Different days')
                        event_time = ''

                except:
                    # print('except')
                    event_datetime_start = datetime.datetime.strptime(event['start']['date'], '%Y-%m-%d')
                    event_datetime_end = datetime.datetime.strptime(event['end']['date'], '%Y-%m-%d')
                    event_time = ''

                # Truncate long descriptions
                if len(event_summary) > 24:
                    event_summary = event_summary[0:24] + '...' 
                
                if len(event_location) > 20:
                    event_location = event_location[0:20] + '...' 
                
                # Draw summary & details
                draw.text((325, 48 + line_height), event_summary, font = getFont(15, 'Bold'), fill = 0)   # Summary
                draw.text((325, 68 + line_height), event_time + event_location, font = getFont(15, 'Regular'), fill = 0)  # Details

                line_height += 32

                # if line_height > EPD_HEIGHT:
                #     break

            line_height += 48
            
            # if line_height > EPD_HEIGHT:
            #         break

def render():
    # Render
    epd.display_frame(epd.get_frame_buffer(image))

if __name__ == '__main__':
    main()
