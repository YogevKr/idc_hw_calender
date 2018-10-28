import urllib
from datetime import datetime
import pytz
import config
from urllib.request import urlopen
from urllib.parse import quote_plus

tz = pytz.timezone('Asia/Jerusalem')


def send_message_for_new_hw(event):
    ex_time = datetime.fromtimestamp(int(event.end_time), tz).strftime('%d.%m.%Y %H:%M')

    text = 'New Homework!\n\n{0} - {1}\n\nDue by {2}\n\n{3}'\
        .format(event.ex_number, event.course, ex_time, event.link)

    url = 'https://api.telegram.org/{0}/sendMessage' \
          '?chat_id={1}&text={2}'.format(config.Config.TELEGRAM_TOKEN,
                                         config.Config.TELEGRAM_CHAT_ID, quote_plus(text))

    urlopen(url).read()


def send_messages_for_new_hws(events):
    for key, value in events.items():
        send_message_for_new_hw(value)


def send_message_for_update_hw(event):
    ex_time = datetime.fromtimestamp(int(event.end_time), tz).strftime('%d.%m.%Y %H:%M')

    text = 'Extension of the due date!\n\nHw {0} - {1}\n\nDue by {2}\n\n{3}' \
        .format(event.ex_number, event.course, ex_time, event.link)

    url = 'https://api.telegram.org/{0}/sendMessage' \
          '?chat_id={1}&text={2}'.format(config.Config.TELEGRAM_TOKEN,
                                         config.Config.TELEGRAM_CHAT_ID, quote_plus(text))

    urlopen(url).read()


def send_messages_for_update_hws(events):
    for key, value in events.items():
        send_message_for_update_hw(value)


def send_message(text):
    url = 'https://api.telegram.org/{0}/sendMessage' \
          '?chat_id={1}&text={2}'.format(config.Config.TELEGRAM_TOKEN,
                                         config.Config.TELEGRAM_CHAT_ID, quote_plus(text))

    urlopen(url).read()


