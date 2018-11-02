# main

import epd7in5
import datetime
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
EPD_WIDTH = 640
EPD_HEIGHT = 384

def main():
    fetchEvents()
    drawEvents()

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
    
    # print(events[0])

    # for event in events:
    #     start = event['start'].get('dateTime', event['start'].get('date'))
    #     print(start, event['summary'])

def drawEvents():
    epd = epd7in5.EPD()
    epd.init()

    # For simplicity, the arguments are explicit numerical coordinates
    image = Image.new('1', (EPD_WIDTH, EPD_HEIGHT), 1)    # 1: clear the frame
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', 24)
    draw.rectangle((0, 6, 640, 30), fill = 0)
    draw.text((200, 10), 'e-Paper demo', font = font, fill = 255)
    draw.rectangle((200, 80, 600, 280), fill = 0)
    draw.arc((240, 120, 580, 220), 0, 360, fill = 255)
    draw.rectangle((0, 80, 160, 280), fill = 255)
    draw.arc((40, 80, 180, 220), 0, 360, fill = 0)
    epd.display_frame(epd.get_frame_buffer(image))

    image = Image.open('monocolor.bmp')
    epd.display_frame(epd.get_frame_buffer(image))

    # You can get frame buffer from an image or import the buffer directly:
    #epd.display_frame(imagedata.MONOCOLOR_BITMAP)

if __name__ == '__main__':
    main()