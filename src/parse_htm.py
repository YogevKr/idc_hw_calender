import urlparse
import re
import itertools
import export_htm_robobrowser


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
    eventList = []
    for id, course, num, exTime, link in itertools.izip(exIdlist, exCourseList, exNumList, exTimeList, exLinklist):
        eventList.append([id, course, num, exTime, link])

    return eventList

def get_new_event_list():
    soup = export_htm_robobrowser.export_html()
    return parse_event_page(soup)


def filter_events(eventList):
    ids = open('./id.history', 'rb').read().split('\n')
    filteredEvents = []
    exist = 0
    for event in eventList:
        for oldId in ids:
            if event[0] == oldId:
                exist = 1
                break
        if exist == 0:
            filteredEvents.append(event)
        exist = 0

    return filteredEvents

def backup_events(filteredEvents):
    for event in filteredEvents:
        with open("id.history", "a") as myfile:
            myfile.write(event[0]+'\n')


def filter_backup(eventList):
    filteredList = filter_events(get_new_event_list())
    backup_events(filter_events(filteredList))
    return filteredList


def main():
    eventList = get_new_event_list()
    print eventList

if __name__ == '__main__':
    main()
