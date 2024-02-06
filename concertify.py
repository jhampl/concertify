import time
import os
import winotify
import traceback
from multiprocessing import Process
from server.server import start_webserver
from scraper import update_all
from storage import get_new_relevant_events
from configparser import ConfigParser


config = ConfigParser()
config.read('config.ini')
PORT = int(config.get('server', 'PORT'))

LAST_UPDATE = os.path.abspath("./LAST_UPDATE")


def main():
    print("Starting web UI...")
    server_process = Process(daemon=True, target=start_webserver, args=(PORT,))
    server_process.start()
    

    # Check for new events 12 hours
    while True:
        if is_time_to_update():
            try:
                print("Updating events and artists...")
                update_all()
            except Exception as e:
                print(e)
                print(traceback.format_exc())
                print("Error updating events and artists")
        new_events = get_new_relevant_events()
        write_last_update_time()
        if new_events:
            notify(new_events)
        time.sleep(3600)  # Sleep for 1 hour before checking again


def is_time_to_update():
    if not os.path.exists(LAST_UPDATE):
        return True

    with open(LAST_UPDATE, "r") as file:
        last_update_time = float(file.read())
        current_time = time.time()
        elapsed_time = current_time - last_update_time
        return elapsed_time >= 43200  # 12 hours in seconds


def write_last_update_time():
    current_time = time.time()
    with open(LAST_UPDATE, "w") as file:
        file.write(str(current_time))


def notify(events):
    notification = winotify.Notification("Concertify", "New Events")
    notification.add_actions(
        label=f"You have {len(events)} new events!", launch=f"http://localhost:{PORT}/")
    notification.show()


if __name__ == "__main__":
    print("Starting Concertify...")
    main()
