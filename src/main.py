from google_calender import add_event
from parse_htm import get_new_event_list
from parse_htm import filter_backup
import urllib
import urllib2
import pytz
from datetime import datetime
from config import Config

tz = pytz.timezone('Asia/Jerusalem')


def main():

    print '-----Start-----\n' +  datetime.now().strftime("%d-%m-%Y %H:%M:%S") + '\n'
    eventlist = get_new_event_list()

    filteredlist = filter_backup(eventlist)

    # event = [id, course, num, exTime, link]
    for event in filteredlist:
        print 'Hw ' + event[2] + ' - ' + event[1]+ ' ' + event[4] + ' ' + \
              datetime.fromtimestamp(int(event[3]), tz).isoformat() + ' ' +\
              datetime.fromtimestamp(int(event[3]), tz).isoformat()
        
        add_event('Hw ' + event[2] + ' - ' + event[1], event[4], datetime.fromtimestamp(int(event[3]), tz).isoformat()
                  , datetime.fromtimestamp(int(event[3]), tz).isoformat())

        ######### Send to Telegram Channel ##########

        text = 'New Homework!\n\nHw ' + event[2] + ' - ' + event[1] + '\n\nDue by ' + \
                   datetime.fromtimestamp(int(event[3]), tz).strftime('%d.%m.%Y %H:%M')+ '\n\n' + event[4]

        url = 'https://api.telegram.org/{0}/sendMessage' \
              '?chat_id={1}&text={2}'.format(Config.TELEGRAM_TOKEN, Config.GOOGLE_CALENDER_ID, urllib.quote_plus(text))

        contents = urllib2.urlopen(url).read()

    print '------End------\n'


if __name__ == '__main__':
        main()
