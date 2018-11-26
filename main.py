# main

# TODO:
# - event['start']['dateTime'] & event['end']['dateTime'] may span a few days
# - On multi-day event, if date is start day, display "Starts @ 7:30AM"
# - On multi-day event, if date is end day, display "Ends @ 10:30PM"

import epd7in5
import datetime
# from googleapiclient.discovery import build
# from httplib2 import Http
# from oauth2client import file, client, tools
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
# import sys
# import os
import json
from pprint import pprint

with open('data.json') as f:
    events = json.load(f)

# print(os.getcwd())
# print(sys.platform)

# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
EPD_WIDTH = 640
EPD_HEIGHT = 384

def main():
    fetchEvents()
    # drawEvents()

def fetchEvents():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('e-ink_home_display-dcb881b9fb01.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('calendar', 'v3', http=creds.authorize(Http()))

    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    
    print('Getting the upcoming 10 events')
    
    events_result = service.events().list(
        calendarId='lkopeh0sr1m9svqcggd0pms2ug@group.calendar.google.com',
        maxResults=10,
        orderBy='startTime',
        singleEvents=True,
        timeMin=now
    ).execute()
    
    global events
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
    
    for event in events: 
        start = event['start'].get('dateTime', event['start'].get('date'))

def draw():
    print('drawEvents')
    # Initialize E-Paper Display inferface
    epd = epd7in5.EPD()
    epd.init()

    # For simplicity, the arguments are explicit numerical coordinates
    image = Image.new('1', (EPD_WIDTH, EPD_HEIGHT), 1)    # 1: clear the frame
    draw = ImageDraw.Draw(image)

    # Fonts
    def font(size, weight):
        return ImageFont.truetype('/home/pi/python_programs/pi-cal/fonts/OpenSans-{}.ttf'.format(weight), size)
    

    def drawCalendar():
        print('drawEvents')
        
        year = datetime.datetime.now().strftime("%Y")
        month = datetime.datetime.now().strftime("%B")

        draw.text((32, 225), month + ' ' + year, font = font(24, 'Regular'), fill = 0)
        draw.text((32, 250), 'Su  M  T  W  Th  F  S', font = font(18, 'Bold'), fill = 0)
        draw.text((32, 270), '30  1  2  3   4  5  6', font = font(15, 'Regular'), fill = 0)
        draw.text((32, 290), ' 7  8  9 10  11 12 13', font = font(15, 'Regular'), fill = 0)
        draw.text((32, 310), '14 15 16 17  18 19 20', font = font(15, 'Regular'), fill = 0)
        draw.text((32, 330), '21 22 23 24  25 26 27', font = font(15, 'Regular'), fill = 0)
        draw.text((32, 350), '28 29 30 31   1  2  3', font = font(15, 'Regular'), fill = 0)
    
    def drawDate():
        print('drawDate')

        day = datetime.datetime.now().strftime('%A')
        date = datetime.datetime.now().strftime('%-d')

        draw.text((32, 24), day, font = font(32, 'Regular'), fill = 0)
        draw.text((32, 24), date, font = font(148, 'Regular'), fill = 0)

    def drawEvents():
        print('drawEvents')
        lineheight = 20

        for event in events:
            event_summary = event['summary']
            print(event['summary'])
            
            # Location
            try:
                event_location = '@ ' + event['location']
            except:
                event_location = ''

            try:
                print('try')
                event_datetime_start = datetime.datetime.strptime(event['start']['dateTime'][0:19], '%Y-%m-%dT%H:%M:%S')
                event_datetime_end = datetime.datetime.strptime(event['end']['dateTime'][0:19], '%Y-%m-%dT%H:%M:%S')

                event_day = event_datetime_start.strftime('%a').upper()
                event_date = str(event_datetime_start.day)
                
                event_time_start = event_datetime_start.strftime('%-I') + ':' + event_datetime_start.strftime('%M') + event_datetime_start.strftime('%p')       # "7:30AM'
                event_time_end = event_datetime_end.strftime('%-I') + ':' + event_datetime_end.strftime('%M') + event_datetime_end.strftime('%p')     # "10:30PM"

                # For multi-day events
                if event['start']['dateTime'][0:10] == event['end']['dateTime'][0:10]:
                    print('Same day')
                    event_time = '{} - {} '.format(event_time_start, event_time_end)     # "7:30AM - 10:45PM"

                else :
                    print('Different days')
                    event_time = ''

            except Exception:
                print('except')
                event_datetime_start = datetime.datetime.strptime(event['start']['date'], '%Y-%m-%d')
                event_datetime_end = datetime.datetime.strptime(event['end']['date'], '%Y-%m-%d')

                event_day = event_datetime_start.strftime('%a').upper()
                event_date = str(event_datetime_start.day)

                event_time = ''
                print(event_datetime_start)

            # Truncate long descriptions
            if(len(event_summary) > 24):
                event_summary = event_summary[0:24] + '...' 
            
            if(len(event_location) > 18):
                event_location = event_location[0:18] + '...' 

            draw.text((255, 0 + lineheight), event_date, font = font(42, 'Regular'), fill = 0)   # Date
            draw.text((260, 50 + lineheight), event_day, font = font(15, 'Regular'), fill = 0)   # Day
            
            draw.text((315, 10 + lineheight), event_summary, font = font(15, 'Bold'), fill = 0)   # Summary
            draw.text((315, 32 + lineheight), event_time + event_location, font = font(15, 'Regular'), fill = 0)  # Details

            lineheight += 80

    drawCalendar()
    drawDate()
    drawEvents()

    # Render
    epd.display_frame(epd.get_frame_buffer(image))

if __name__ == '__main__':
    draw()