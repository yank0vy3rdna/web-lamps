import time
from threading import Thread

import requests
from apscheduler.schedulers.background import BackgroundScheduler

from lamps.lampsRepository import lampsRepository


class Sun:
    sunrise = None
    sunset = None
    scheduler = None
    allOn = None
    allOff = None

    def __init__(self, allOn, allOff):
        self.scheduler = BackgroundScheduler()
        self.scheduler.start()
        self.allOn = allOn
        self.allOff = allOff

    def getting_suntime(self):
        sunrise_job = None
        sunset_job = None
        while True:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'}
            r = requests.get('https://time.is/Dubna#time_zone', headers=headers).text
            sunrise = r[r.index("<li>Восход: ") + 12:r.index("<li>Восход: ") + 12 + 5]
            sunset = r[r.index("<li>Закат: ") + 11:r.index("<li>Закат: ") + 11 + 5]
            if sunrise_job is None or sunset_job is None:
                sunrise_job = self.scheduler.add_job(self.allOff, 'cron', kwargs={"sun": True},
                                                     hour=sunrise.split(':')[0],
                                                     minute=sunrise.split(':')[1])
                sunset_job = self.scheduler.add_job(self.allOn, 'cron', kwargs={"sun": True}, hour=sunset.split(':')[0],
                                                    minute=sunset.split(':')[1])
            else:
                try:
                    sunrise_job.reschedule(trigger='cron', hour=sunrise.split(':')[0], minute=sunrise.split(':')[1])
                    sunset_job.reschedule(trigger='cron', hour=sunset.split(':')[0], minute=sunset.split(':')[1])
                except Exception as e:
                    print(e)
            time.sleep(3600 * 24)


def setup():
    sun = Sun(lampsRepository.allOn, lampsRepository.allOff)
    suntimeThread = Thread(target=sun.getting_suntime)
    suntimeThread.start()
