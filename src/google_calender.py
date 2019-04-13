from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
import pytz
from datetime import datetime
from config import Config


tz = pytz.timezone('Asia/Jerusalem')

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/calendar-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/calendar'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Calendar API Python Quickstart'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'calendar-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials


def get_service():
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    return service


def add_event(summary, description, start, end, event_id):

    service = get_service()

    event = {
        'summary': summary,
        'description': description,
        'start': {
            'dateTime': start,
            'timeZone': 'Asia/Jerusalem',
                },
        'end': {
            'dateTime': end,
            'timeZone': 'Asia/Jerusalem',
                },
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'popup', 'minutes': 30},
            ],
        },
    }

    event = service.events().insert(calendarId='{0}@group.calendar.google.com'.format(Config.GOOGLE_CALENDER_ID), body=event).execute()

    return event.get('id')

def update_event(event_obj):

    service = get_service()

    # try:
    event = service.events().get(calendarId='{0}@group.calendar.google.com'
                                 .format(Config.GOOGLE_CALENDER_ID), eventId=event_obj.google_id.encode("utf-8")).execute()

    ex_time_iso_format = datetime.fromtimestamp(int(event_obj.end_time), tz).isoformat()

    event['start'] = {
        'dateTime': ex_time_iso_format,
        'timeZone': 'Asia/Jerusalem',
    }

    event['end'] = {
        'dateTime': ex_time_iso_format,
        'timeZone': 'Asia/Jerusalem',
    }

    updated_event = service.events().update(calendarId='{0}@group.calendar.google.com'.format(Config.GOOGLE_CALENDER_ID), eventId=event['id'],
                                            body=event).execute()
    # except:
    #     return


def add_event_from_event_object(event):

    title = '{0} - {1}'.format(event.ex_number, event.course)
    ex_time_iso_format = datetime.fromtimestamp(int(event.end_time), tz).isoformat()

    google_id = add_event(title, event.link, ex_time_iso_format, ex_time_iso_format, event.id)

    event.google_id = google_id
    print(title)


def add_events_to_calender(events):
    for key, value in events.iteritems():
        add_event_from_event_object(value)


def update_events(events):
    for key, value in events.iteritems():
        update_event(value)
