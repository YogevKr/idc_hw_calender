import re
import event

from datetime import datetime
from time import mktime

from export_htm_robobrowser import export_html


def parse_event_page(soup):
    event_dic = {}

    # extract initial details
    assignments_links = [x.find_all('a')[0]['href'] for x in
                         soup.find_all('div', attrs={"class": "description card-block calendar_event_due"})]

    for link in assignments_links:
        html = export_html(link)
        m = re.search("id=([0-9]*)", link)
        ex_id = m.group(1)
        course_name = html.find_all('h1')[0].text
        ex_name = html.find_all('h2')[0].text

        potential_dates_tags = html.find_all('td', attrs={"class": "cell c1 lastcol"})

        due_time = None

        for tag in potential_dates_tags:
            try:
                due_time = datetime.strptime(tag.text, '%A, %d %B %Y, %I:%M %p')
                break
            except ValueError:
                pass

        if not due_time:
            raise Exception

        time_stamp = mktime(datetime.timetuple(due_time))

        event_dic[ex_id] = event.Event(ex_id, course_name, ex_name, time_stamp, link)

    return event_dic
