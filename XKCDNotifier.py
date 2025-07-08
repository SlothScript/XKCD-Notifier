import requests
import time
import datetime
from notifypy import Notify
import sys

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
    return datetime.datetime.now().weekday() in {0, 2, 4}

def countdown_timer(seconds):
    start_time = time.time()
    while seconds > 0:
        elapsed = time.time() - start_time
        remaining = max(seconds - int(elapsed), 0)
        
        hours, remainder = divmod(remaining, 3600)
        minutes, secs = divmod(remainder, 60)
        time_str = f"{hours:02d}:{minutes:02d}:{secs:02d}"
        sys.stdout.write(f"\rNext check in {time_str}")
        sys.stdout.flush()
        
        if remaining == 0:
            break
        
        time.sleep(1)
    sys.stdout.write("\r" + " " * 40 + "\r")  # Clear the line

def main():
    latest_known_comic = get_latest_comic_number() or 0  # Initialize with the latest known comic

    while True:
        # Only check for comics on expected upload days
        if not is_expected_upload_day():
            print("Not a release day. Calculating next upload time...")
            
            # Find next expected upload day
            today = datetime.datetime.now()
            days_ahead = (0 - today.weekday() + 7) % 7  # Next Monday
            if today.weekday() > 0:
                days_ahead = (2 - today.weekday() + 7) % 7  # Next Wednesday
                if today.weekday() > 2:
                    days_ahead = (4 - today.weekday() + 7) % 7  # Next Friday

            next_upload_day = today + datetime.timedelta(days=days_ahead)
            next_upload_day = next_upload_day.replace(hour=8, minute=0, second=0, microsecond=0)
            
            # Sleep until 8am on next upload day
            sleep_seconds = int((next_upload_day - today).total_seconds())
            countdown_timer(sleep_seconds)
            continue

        latest = get_latest_comic_number()
        if latest is None:
            countdown_timer(300)
            continue

        if latest > latest_known_comic:
            # New comic found!
            message = f"New XKCD Comic {latest} uploaded!"
            notify_user(message, latest)
            latest_known_comic = latest
        else:
            print("No new comic found. Checking again soon...")

        countdown_timer(300)

if __name__ == "__main__":
    main()
