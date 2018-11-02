# import epd7in5
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import datetime
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'

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
    for event in events:
        print(event['summary'])

if __name__ == '__main__':
    main()