import requests
import time
import datetime
from plyer import notification

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

def notify_user(message):
    print(message)
    try:
        notification.notify(
            title="XKCD Update",
            message=message,
            timeout=10
        )
    except Exception as e:
        print(f"Notification error: {e}")

def is_expected_upload_day():
    return datetime.datetime.today().weekday() in [0, 2, 4]  # Monday, Wednesday, Friday

def wait_until_next_check(interval_seconds):
    print(f"Waiting {interval_seconds} seconds...")
    time.sleep(interval_seconds)

def main():
    checked_comics = set()

    while True:
        if not is_expected_upload_day():
            print("Not an XKCD update day. Sleeping for 6 hours.")
            time.sleep(6 * 60 * 60)
            continue

        latest = get_latest_comic_number()
        if latest is None:
            wait_until_next_check(60)
            continue

        next_comic = latest + 1

        if next_comic in checked_comics:
            wait_until_next_check(30)
            continue

        print(f"Checking for XKCD comic #{next_comic}...")
        if check_comic_exists(next_comic):
            message = f"XKCD Comic {next_comic} uploaded!"
            notify_user(message)
            checked_comics.add(next_comic)
            print("Comic found. Sleeping until next expected upload day.")
            time.sleep(24 * 60 * 60)  # Sleep a full day
        else:
            wait_until_next_check(30)

if __name__ == "__main__":
    main()
