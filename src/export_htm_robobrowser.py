from robobrowser import RoboBrowser
import time
import datetime
from config import Config


def export_html(url=None):

    date = str(int(time.time()))
    browser = RoboBrowser()
    current_year = datetime.datetime.now().year

    browser = RoboBrowser(
    	history=True,
        user_agent='Mozilla/5.0 ... Safari/537.36'
    )
    login_url = 'http://moodle.idc.ac.il/{0}/calendar/view.php?lang=en'.format(current_year)
    browser.open(login_url)
    form = browser.get_form(id='auth_form')
    form['username'].value = Config.MOODLE_USER_NAME
    form['password'].value = Config.MOODLE_PASSWORD
    browser.submit_form(form)

    if url is None:
        browser.open('http://moodle.idc.ac.il/2019/calendar/view.php?time={1}&lang=en'.format(current_year, date))
        browser.open('http://moodle.idc.ac.il/2019/calendar/view.php?time={1}&lang=en'.format(current_year, date))
    else:
        browser.open(url)
        browser.open(url)

    return browser.parsed

