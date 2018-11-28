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
import os
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from pprint import pprint
import requests
import sys

print(os.getcwd())  # current working directory, absolute path
print(sys.argv[0])  # working directory

with open('./data.json') as f:
    events = json.load(f)

def main():
    init()
    auth()
    # fetchEvents()
    # draw()

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

def auth():
    print('auth')

    AUTH_URL = 'https://accounts.google.com/o/oauth2/device/code'
    CLIENT_ID = '635286573706-22bvqd3vc034afg5vn9nopi6n6jed7sn.apps.googleusercontent.com'
    CLIENT_SECRET = 'Mc17FgVoPBYoxxaIPlboNBYn'
    GRANT_TYPE = 'http://oauth.net/grant_type/device/1.0.'
    SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'    # If modifying these scopes, delete the file token.json.
    TOKEN_URL = 'https://www.googleapis.com/oauth2/v4/token'

    # Initial request
    r = requests.post(AUTH_URL, data = {
        'client_id': CLIENT_ID,
        'scope': SCOPES
    }).json()

    # {
    #   'device_code': 'AH-1Ng1BzvzcVPXWrakudSRlaBkKTm5otqDWNT0u0p5J9mjXR1hMiS-rUS5D7Ss7LvDvAumcQReo_ME9N30vcEWiLbMQq0ORCw',
    #   'expires_in': 1800,
    #   'interval': 5,
    #   'user_code': 'KQTW-SDMD',
    #   'verification_url': 'https://www.google.com/device'
    # }

    DEVICE_CODE = r['device_code']

    group_top = 116

    draw.text((24, group_top), 'Visit', font = getFont(18, 'Regular'), fill = 0)
    draw.text((24, 32 + group_top), r['verification_url'], font = getFont(24, 'Bold'), fill = 0)
    draw.text((24, 90 + group_top), 'and enter', font = getFont(18, 'Regular'), fill = 0)
    draw.text((24, 122 + group_top), r['user_code'], font = getFont(32, 'Bold'), fill = 0)

    render()

    # Token polling
    # token = requests.post(TOKEN_URL, data = {
    #     'client_id': CLIENT_ID,
    #     'client_secret': CLIENT_SECRET,
    #     'code': DEVICE_CODE,
    #     'grant_type': GRANT_TYPE
    # })

    # {
    #     "access_token":"1/fFAGRNJru1FTz70BzhT3Zg",
    #     "expires_in":3920,
    #     "token_type":"Bearer",
    #     "refresh_token":"1/xEoDL4iW3cxlI7yDbSRFYNG01kVKM2C-259HOF2aQbI"
    # }


def fetchEvents():
    print('fetchEvents')
    # Shows basic usage of the Google Calendar API.
    # Prints the start and name of the next 10 events on the user's calendar.

    # store = file.Storage('token.json')
    # creds = store.get()

    # if not creds or creds.invalid:
    #     flow = client.flow_from_clientsecrets('e-ink_home_display-dcb881b9fb01.json', SCOPES)
    #     creds = tools.run_flow(flow, store)
    # service = build('calendar', 'v3', http=creds.authorize(Http()))

    # # Call the Calendar API
    # now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    
    # print('Getting the upcoming 10 events')
    
    # events_result = service.events().list(
    #     calendarId='lkopeh0sr1m9svqcggd0pms2ug@group.calendar.google.com',
    #     maxResults=10,
    #     orderBy='startTime',
    #     singleEvents=True,
    #     timeMin=now
    # ).execute()
    
    # global events
    # events = events_result.get('items', [])

    # if not events:
    #     print('No upcoming events found.')
    
    # for event in events: 
    #     start = event['start'].get('dateTime', event['start'].get('date'))

def formatEvents(events):
    print('formatEvents')

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

def draw():
    print('drawEvents')
    
    def drawCalendar():
        print('drawCalendar')

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
    
    def drawDate():
        print('drawDate')
        day = datetime.datetime.now().strftime('%A')
        date = datetime.datetime.now().strftime('%-d')

        draw.text((24, 8), day, font = getFont(32, 'Regular'), fill = 0)
        draw.text((24, 8), date, font = getFont(148, 'Regular'), fill = 0)

    def drawEvents():
        print('drawEvents')
        line_height = 16

        # Render "Today"
        draw.text((260, 16), 'TODAY', font = getFont(15, 'Regular'), fill = 0)   # Day
        draw.text((325, 16), 'Not much going on!', font = getFont(15, 'Italic'), fill = 0)  # Details

        events_format = formatEvents(events)

        # Sort formatted events by date
        dates_sort = [ datetime.datetime.strptime(event_key, '%Y-%m-%d') for event_key in events_format.keys() ]
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

            for event in events_format[date]:
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

    drawCalendar()
    drawDate()
    drawEvents()
    render()

def render():
    # Render
    epd.display_frame(epd.get_frame_buffer(image))

if __name__ == '__main__':
    main()
