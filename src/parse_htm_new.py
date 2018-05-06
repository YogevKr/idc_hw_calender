import urlparse
import re
import itertools
import export_htm_robobrowser
import event

def parse_event_page(soup):

    # Ex number
    exNumList = []
    exNumList1 = [re.search("[0-9]{1,2}", row.find('a').contents[0]) for row in
                 soup.find_all('div', attrs={"class": "event"})]


    for item in exNumList1:
        if item is not None:
            exNumList.append(item.group())


    #exNumList = [re.search("\d", row.find('a').contents[0]).group() for row in
     #             soup.find_all('div', attrs={"class": "event"})]


    # date + hour in unix time
    exTimeList = [urlparse.parse_qs(urlparse.urlparse(row.find('a')['href']).query)['time'][0] for row in
                  soup.find_all('span', attrs={"class": "date pull-xs-right m-r-1"})]

    # course
    exCourseList = [row.find('a').contents[0] for row in soup.find_all('div', attrs={"class": "course"})]

    # link
    exLinklist = [row.find('a')['href'] for row in soup.find_all('h3', attrs={"class": "referer"})]

    # id
    exIdlist = [urlparse.parse_qs(urlparse.urlparse(row.find('a')['href']).query)['id'][0] for row in
                soup.find_all('h3', attrs={"class": "referer"})]

    # for id, course, num, exTime, link in itertools.izip(exIdlist, exCourseList, exNumList, exTimeList, exLinklist):
    #     print id + ' HW ' + num + ' - ' + course + ' ' + time.ctime(int(exTime)) + ' ' + link
    event_list = []
    for id, course, num, exTime, link in itertools.izip(exIdlist, exCourseList, exNumList, exTimeList, exLinklist):
        evnt = event.Event(id, course, num, exTime, link)
        event_list.append(evnt)

    return event_list