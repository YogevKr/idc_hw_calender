import re
import event
from datetime import datetime
from time import mktime
import logging

from export_htm_robobrowser import export_html


def parse_event_page(soup):
    event_dic = {}

    # extract initial details

    hw_divs = soup.find_all('div', attrs={"class": "description card-block calendar_event_due"})
    open_quiz_divs = soup.find_all('div', attrs={"class": "description card-block calendar_event_open"})

    assignments_links = [x.find_all('a')[0]['href'] for x in (hw_divs + open_quiz_divs)]

    for link in assignments_links:

        if 'moodle' not in link:
            continue

        html = export_html(link)
        due_time = None

        if 'quiz' in link:

            ps = html.find_all('p')

            for p in ps:
                if 'This quiz will close' in p.text:
                    close_lst = p.text.split(',')
                    close_str = close_lst[1] + close_lst[2]
                    due_time = datetime.strptime(close_str, ' %d %B %Y %I:%M %p')
                    break
        else:
            potential_dates_tags = html.find_all('td', attrs={"class": "cell c1 lastcol"})
            for tag in potential_dates_tags:
                try:
                    due_time = datetime.strptime(tag.text, '%A, %d %B %Y, %I:%M %p')
                    break
                except ValueError:
                    pass

        m = re.search("id=([0-9]*)", link)
        ex_id = m.group(1)
        course_name = html.find_all('h1')[0].text
        ex_name = html.find_all('h2')[0].text

        if due_time is None:
            logging.error("No due time " + link)
            continue

        time_stamp = mktime(datetime.timetuple(due_time))

        event_dic[ex_id] = event.Event(ex_id, course_name, ex_name, time_stamp, link)

    return event_dic
