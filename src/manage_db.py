import json
import event


def load_events_from_db():
    with open('data/db.json', 'r') as f:
        db = json.load(f)

    events_list_json = db["events"]

    event_dic = {}
    for key, value in events_list_json.items():
        course = value["course"]
        ex_number = value["ex_number"]
        end_time = value["end_time"]
        link = value["link"]
        google_id = value["google_id"]

        ev = event.Event(key, course, ex_number, end_time, link, google_id)

        event_dic[key] = ev

    return event_dic


def parse_events_obj_to_json_format(events):
    data = {"events": {}}

    for key, value in events.items():
        data["events"][key] = {"course": value.course, "ex_number": value.ex_number,
                               "end_time": value.end_time, "link": value.link, "google_id": value.google_id}
    return data


def dump_events_to_db(new_events_dic):

    current_db_events = load_events_from_db()

    # Add the new event obj
    for key, value in new_events_dic.items():
        current_db_events[key] = value

    data = parse_events_obj_to_json_format(current_db_events)

    with open('data/db.json', 'w') as db:
        json.dump(data, db)


def update_event(i_event):
    current_db_events = load_events_from_db()

    current_db_events[i_event.id] = i_event

    data = parse_events_obj_to_json_format(current_db_events)

    with open('data/db.json', 'w') as db:
        json.dump(data, db)


def update_events(events):
    for key, value in events.items():
        update_event(value)
