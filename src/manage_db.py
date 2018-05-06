import json
import event


def load_events_from_db():
    with open('/data/db.json', 'r') as f:
        db = json.load(f)

    events_list_json = db["events"]

    event_dic = {}
    for key, value in events_list_json.iteritems():
        course = value["course"]
        ex_number = value["ex_number"]
        end_time = value["end_time"]
        link = value["link"]

        ev = event.Event(key, course, ex_number, end_time, link)

        event_dic[key] = ev

    return event_dic


def dump_events_to_db(events_dic):
    data = {"events": {}}

    for key, value in events_dic.iteritems():
        data["events"][key] = {"course": value.course, "ex_number": value.ex_number,
                               "end_time": value.end_time, "link": value.link}

    with open('/data/db.json', 'w') as db:
        json.dump(data, db)
