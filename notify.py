import winotify

def notify(title, message, webpage_url, event_count):
    notification = winotify.Notification(title, message)
    notification.add_actions(label="You have {event_count} new events!", launch=webpage_url)
    notification.show()