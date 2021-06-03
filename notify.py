from notifypy import Notify
from slack_sdk.webhook.client import WebhookClient

def console(near, far, location):
    shortmessage = f"{near} near / {far} far dates"

    print(shortmessage)


def popup(near, far, location):
    shortmessage = f"{near} near / {far} far dates"

    notification = Notify()
    notification.title = "COVID Vaccination Available"
    notification.message = shortmessage
    notification.send()


def slack(near, far, location, url):
    shortmessage = f"{near} dates this week, {far} next week"
    message = f"@all {shortmessage} available: [doctolib.de]({location})"

    client = WebhookClient(url)
    response = client.send(text=message)
