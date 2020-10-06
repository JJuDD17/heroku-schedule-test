from apscheduler.schedulers.blocking import BlockingScheduler
from requests import get
import os
import datetime as dt
import time
import random

print('heroku_schedule_test.py is running')

TELEGRAM_API_TOKEN = os.environ.get('TELEGRAM_API_TOKEN')
TELEGRAM_CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')
TELEGRAM_MESSAGE = os.environ.get('TELEGRAM_MESSAGE')

def send_notification(token, chat_id, text):
    url = f'https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={text}'
    print(get(url).text)

sched = BlockingScheduler()

#@sched.scheduled_job('interval', minutes=3)
def notify_job():
    now = dt.datetime.now().strftime('%d.%m.%Y %H:%M:%S')
    text = f'[{now}] {TELEGRAM_MESSAGE}'
    send_notification(TELEGRAM_API_TOKEN, TELEGRAM_CHAT_ID, text)

def sleep_job():
    now = dt.datetime.now().strftime('%d.%m.%Y %H:%M:%S')
    print(f'[{now}] sleeping 60 seconds...')
    time.sleep(60)
    now = dt.datetime.now().strftime('%d.%m.%Y %H:%M:%S')
    print(f'[{now}] sleeped 60 seconds')

def imitate_work_job(seconds):
    def wrapper():
        now = dt.datetime.now().strftime('%d.%m.%Y %H:%M:%S')
        print(f'[{now}] imitating work for {seconds} seconds...')
        start = time.time()
        arr = []
        while time.time() - start < seconds:
            arr.append(random.randint(-2**31, 2**31-1))
            if random.randint(1, 200000) == 1 or len(arr) == 2000000:
                del arr
                arr = []
        now = dt.datetime.now().strftime('%d.%m.%Y %H:%M:%S')
        print(f'[{now}] done imitating work')
    return wrapper

#@sched.scheduled_job('cron', day_of_week='mon-fri', hour=17)
#def scheduled_job():
#    print('This job is run every weekday at 5pm.')

#notify_job()
#sched.add_job(notify_job, 'interval', minutes=3)
#sched.add_job(notify_job, 'cron', hour=17, minute=53)
sched.add_job(imitate_work_job(3*60), 'interval', minutes=4)
imitate_work_job(3*60)()
sched.start()
#send_notification(TELEGRAM_API_TOKEN, TELEGRAM_CHAT_ID, TELEGRAM_MESSAGE)
print('heroku_schedule_test.py is stopping')
