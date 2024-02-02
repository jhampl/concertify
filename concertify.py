import time
import os
import winotify
from multiprocessing import Process
from server import start_webserver
from scraper import update_all
from storage import get_new_relevant_events

LAST_UPDATE = os.path.abspath("./LAST_UPDATE.txt")
PORT = 8080

def main():
    print("Starting web UI...") 
    server_process = Process(daemon=True, target=start_webserver, args=(PORT,))
    server_process.start()
    
    print("Scheduling scraper...")
    scraper_process = Process(daemon=True, target=update_all)
    scraper_process.start()
    
    # Check for new events 12 hours
    while True:
        if is_time_to_update():
            write_last_update_time()
            try:
                update_all()
            except:
                print("Error updating events and artists")
        new_events = get_new_relevant_events() 
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
        return elapsed_time >= 43200 # 12 hours in seconds

def write_last_update_time():
    current_time = time.time()
    with open(LAST_UPDATE, "w") as file:
        file.write(str(current_time))

def notify(event_count):
    notification = winotify.Notification("Concertify", "New Events")
    notification.add_actions(label=f"You have {event_count} new events!", launch="http://localhost:8080/")
    notification.show()

if __name__ == "__main__":
    main()