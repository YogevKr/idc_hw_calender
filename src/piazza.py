import ast
import re

from bs4 import BeautifulSoup
from piazza_api import Piazza

from jsondb.db import Database

from config import Config
from event import Event
from src.telegram import send_message


def get_new_piazza_events():
    db = Database("piazza.db")

    p = Piazza()
    p.user_login(email=Config.PIAZZA_EMAIL, password=Config.PIAZZA_PASSWORD)

    # p.get_user_classes()

    courses = {
        'Advanced Algorithms': {'url': 'https://piazza.com/idc.ac.il/fall2018/3501/resources', 'id': 'jn8vp29d21f2mt'},
        'Automata': {'url': 'https://piazza.com/idc_-_hertzelia/fall2018/1910643/resources', 'id': 'jn8u1w3q1ji2io'}}

    new_resources_ids = []
    new_resources_events = {}
    piazza_hw_key = "piazza_resources_hw_{}"

    for name, course_data in courses.items():
        r = p.session.get(course_data['url'])
        soup = BeautifulSoup(r.text, 'html.parser')
        data = soup.find_all("script")
        index = [i for i in range(len(data)) if 'this.resource_data' in str(data[i])][0]

        regex = r"this.resource_data *= (\[.*);"
        matches = re.search(regex, str(data[index]))
        match = matches.group(1)

        hw_list = ast.literal_eval(match)
        items = [item for item in hw_list if item['config']['section'] == 'homework']

        resources_details = {item['id']: {'name': name, 'subject': item['subject'], 'date': item['config']['date']} for
                             item in
                             items}

        for r_id in resources_details:
            key = piazza_hw_key.format(r_id)

            if key not in db:
                file_url = 'https://piazza.com/class_profile/get_resource/{}/{}'.format(course_data['id'], r_id)
                new_resources_ids.append(r_id)
                new_resources_events[r_id] = Event(r_id, name, resources_details[r_id]['subject'],
                                                   resources_details[r_id]['date'], file_url)

                text = '{} uploaded to Piazza - {}.\n Due date {}\n {}'.format(resources_details[r_id]['subject'], name,
                                                                               resources_details[r_id]['date'],
                                                                               file_url)
                send_message(text)

                db[key] = resources_details[r_id]

    return new_resources_events, new_resources_ids

    # for item in resources_details:
    #     file_url = 'https://piazza.com/class_profile/get_resource/{}/{}'.format(course_data['id'], item[3])
    #     text = '{} uploaded to Piazza - {}.\n Due date {}\n {}'.format(item[1], item[0], item[2], file_url)
    #     send_message(text)


if __name__ == '__main__':
    get_new_piazza_events()
