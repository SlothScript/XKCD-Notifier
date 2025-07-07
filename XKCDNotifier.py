import requests
import time
import datetime
from notifypy import Notify

def get_latest_comic_number():
    url = "https://xkcd.com/info.0.json"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json().get("num")
    except Exception as e:
        print(f"Error fetching latest comic: {e}")
        return None

def check_comic_exists(comic_number):
    url = f"https://xkcd.com/{comic_number}/info.0.json"
    response = requests.get(url)
    return response.status_code != 404

def notify_user(message, comic_number):
    print(message)
    try:
        notification = Notify()
        notification.title = "XKCD Update"
        notification.message = message
        notification.open = f"https://xkcd.com/{comic_number}"
        notification.send()
    except Exception as e:
        print(f"Notification error: {e}")

def is_expected_upload_day():
    return datetime.datetime.today().weekday() in [0, 2, 4]  # Monday, Wednesday, Friday

def wait_until_next_check(interval_seconds):
    print(f"Waiting {interval_seconds} seconds...")
    time.sleep(interval_seconds)

def main():
    checked_comics = set()
    latest_known_comic = get_latest_comic_number() or 0  # Initialize with the latest known comic

    while True:
        latest = get_latest_comic_number()
        if latest is None:
            wait_until_next_check(30)
            continue

        if latest > latest_known_comic:
            # New comic found!
            message = f"New XKCD Comic {latest} uploaded!"
            notify_user(message, latest)
            latest_known_comic = latest
        else:
            print("No new comic found. Checking again soon...")

        wait_until_next_check(30)

if __name__ == "__main__":
    main()
