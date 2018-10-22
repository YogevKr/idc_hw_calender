from config import Config
from bs4 import BeautifulSoup
import re
import ast

from src.piazza_api.piazza import Piazza
from src.telegram import send_message


def piazza():
    p = Piazza()
    p.user_login(email=Config.PIAZZA_EMAIL, password=Config.PIAZZA_PASSWORD)

    # p.get_user_classes()

    courses = {
        'Advanced Algorithms': {'url': 'https://piazza.com/idc.ac.il/fall2018/3501/resources', 'id': 'jn8vp29d21f2mt'},
        'Automata': {'url': 'https://piazza.com/idc_-_hertzelia/fall2018/1910643/resources', 'id': 'jn8u1w3q1ji2io'}}

    for name, course_data in courses.iteritems():
        r = p.session.get(course_data['url'])
        soup = BeautifulSoup(r.text, 'html.parser')
        data = soup.find_all("script")
        index = [i for i in range(len(data)) if 'this.resource_data' in str(data[i])][0]

        regex = r"this.resource_data *= (\[.*);"
        matches = re.search(regex, str(data[index]))
        match = matches.group(1)

        hw_list = ast.literal_eval(match)
        items = [item for item in hw_list if item['config']['section'] == 'homework']

        details = [[name, item['subject'], item['config']['date'], item['id']] for item in items]

        for item in details:
            file_url = 'https://piazza.com/class_profile/get_resource/{}/{}'.format(course_data['id'], item[3])
            text = '{} uploaded to Piazza - {}.\n Due date {}\n {}'.format(item[1], item[0], item[2], file_url)
            send_message(text)


if __name__ == '__main__':
    piazza()
