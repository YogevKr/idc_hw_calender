def get_filtered_events(db, events):
    new_events = {}
    exists_events = {}

    for key, value in events.iteritems():

        if key not in db:
            new_events[key] = value

        else:
            exists_events[key] = value

    return [new_events, exists_events]


def get_non_update_events(db, events):
    non_update_events = {}

    for key, value in events.iteritems():

        if key in db:
            if db[key] == value:
                non_update_events[key] = value

    return non_update_events
