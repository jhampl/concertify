from plyer import notification

def notify(link, timeout=5):
    notification.notify(
        title="Concertify",
        message="There are new concerts!",
        timeout=timeout,
        actions=[link]
    )
