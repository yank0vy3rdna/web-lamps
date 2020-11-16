import logging
import time
from threading import Thread

from lamps.lampsRepository import lampsRepository


def getDataAsync(lampid):
    while True:
        try:
            lampsRepository.getLampById(lampid).update()
        except Exception:
            pass
        time.sleep(3)


def setup():
    for lamp in lampsRepository.lamps.keys():
        lampThread = Thread(target=getDataAsync, args=(str(lamp),))
        lampThread.start()
