#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import sys
import time
import datetime

# File watching
from watchdog.events import PatternMatchingEventHandler
from watchdog.observers import Observer

# Configuration parsing
import configparser
config = configparser.ConfigParser()
config.read('countdown.ini', encoding="utf-8")

from rich.logging import RichHandler
from rich.console import Console
from rich import print
from rich.panel import Panel
console = Console()

FORMAT = "%(message)s"
logging.basicConfig(
    level=config['debug']['loglevel'], format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
)

log = logging.getLogger("rich")

from obswebsocket import obsws, requests

#! (C)2020 Tibet Tornaci/oofdere. All rights reserved.

#* OBS Websocket Settings
obshost = config['obs-websockets']['host']
obsport = config['obs-websockets']['port']
obspass = str(config['obs-websockets']['password'])
obsinstance = obsws(obshost, obsport, obspass)
obsinstance.connect()
log.info("Connected to OBS!")

class MyEventHandler(PatternMatchingEventHandler):
    def on_modified(self, event):

        # open and read duration
        fileduration = open("duration.txt", 'r', encoding="utf-8")
        global t
        t = int(float(fileduration.read()))

        log.info(f"Update!")
       
if __name__ == '__main__':
    path = "."
    event_handler = MyEventHandler(patterns=['*duration.txt'])

    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    log.info("Started Watchdog")

    t = int(config['debug']['launchtime']) # initial countdown value used until song update
    log.info("t initialized as " + str(t))

    try:
        starttime = time.time()
        while True:
            if t > 0:
                obsinstance.call(requests.SetTextGDIPlusProperties("countdown", text=str(datetime.timedelta(seconds=int(t)))))
                log.info(str(datetime.timedelta(seconds=int(t))))
                t -= 1
            else:
                obsinstance.call(requests.SetTextGDIPlusProperties("countdown", text="0:00:00"))
                log.error("DEAD AIR!")
            time.sleep(1.0 - ((time.time() - starttime) % 1.0)) # sync to system clock
            
    except KeyboardInterrupt:
        observer.stop()
        console.log(obsinstance.call(requests.SetTextGDIPlusProperties("countdown", text="")), log_locals=True)
    observer.join()