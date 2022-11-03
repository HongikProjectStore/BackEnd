from datetime import date
import schedule
import time

def crawling():
    if date.today().day != 1:
        return

    # actual job body



schedule.every().day.at("02:00").do(crawling)

while True:
    schedule.run_pending()
    time.sleep(1)
