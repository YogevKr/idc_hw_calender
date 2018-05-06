import urllib
import urllib2
from datetime import datetime
import pytz
import config

tz = pytz.timezone('Asia/Jerusalem')


def send_message_for_new_hw(event):
    ex_time_iso_format = datetime.fromtimestamp(int(event.end_time), tz).isoformat()

    text = 'New Homework!\n\nHw {0} - {1}\n\nDue by {2}\n\n{3}'\
        .format(event.ex_number, event.course, ex_time_iso_format, event.link)

    url = 'https://api.telegram.org/{0}/sendMessage' \
          '?chat_id={1}&text={2}'.format(config.Config.TELEGRAM_TOKEN,
                                         config.Config.TELEGRAM_CHAT_ID, urllib.quote_plus(text))

    urllib2.urlopen(url).read()


def send_messages_for_new_hws(events):
    for key, value in events.iteritems():
        send_message_for_new_hw(value)


