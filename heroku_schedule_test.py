from apscheduler.schedulers.blocking import BlockingScheduler
from requests import get
import os
import datetime as dt

print('heroku_schedule_test.py is running')

TELEGRAM_API_TOKEN = os.environ.get('TELEGRAM_API_TOKEN')
TELEGRAM_CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')
TELEGRAM_MESSAGE = os.environ.get('TELEGRAM_MESSAGE')

def send_notification(token, chat_id, text):
    url = f'https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={text}'
    print(get(url).text)

sched = BlockingScheduler()

#@sched.scheduled_job('interval', minutes=3)
def job():
    now = dt.datetime.now().strftime('%d.%m.%Y %H:%M:%S')
    text = f'[{now}] {TELEGRAM_MESSAGE}'
    send_notification(TELEGRAM_API_TOKEN, TELEGRAM_CHAT_ID, text)

#@sched.scheduled_job('cron', day_of_week='mon-fri', hour=17)
#def scheduled_job():
#    print('This job is run every weekday at 5pm.')

job()
sched.add_job(job, 'interval', minutes=3)
sched.add_job(job, 'cron', hour=20, minute=40)
sched.start()
#send_notification(TELEGRAM_API_TOKEN, TELEGRAM_CHAT_ID, TELEGRAM_MESSAGE)
print('heroku_schedule_test.py is stopping')
