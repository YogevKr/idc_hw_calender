from src import export_htm_robobrowser, manage_db, google_calender
from src.filter_events import get_filtered_events, get_non_update_events
from src.google_calender import add_events_to_calender
from src.manage_db import load_events_from_db, dump_events_to_db, update_events
from src.parse_htm import parse_event_page
from src.telegram import send_messages_for_new_hws, send_messages_for_update_hws


def main():

    # Get the html of the moodle page
    html_page = export_htm_robobrowser.export_html()

    # Dictionary of the events in moodle right now
    event_from_moodle_dic = parse_event_page(html_page)

    # Load events from db
    db_dic = load_events_from_db()

    # Filter to new and exist events
    [new_events, exist_events] = get_filtered_events(db_dic, event_from_moodle_dic)

    # Filter update needed events
    non_update_events = get_non_update_events(db_dic, exist_events)

    # Add new events to google calender
    add_events_to_calender(new_events)

    # Update relevant events and send message on telegram chanel
    google_calender.update_events(non_update_events)
    send_messages_for_update_hws(non_update_events)

    # Send message about new hws to telegram chanel
    send_messages_for_new_hws(new_events)

    # Write all events to database
    manage_db.update_events(non_update_events)
    dump_events_to_db(new_events)


if __name__ == '__main__':
        main()
