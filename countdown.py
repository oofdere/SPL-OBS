#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import sys
import time
import datetime

from watchdog.events import PatternMatchingEventHandler
from watchdog.observers import Observer

#logging.basicConfig(level=logging.DEBUG)

from obswebsocket import obsws, requests

#! (C)2020 Tibet Tornaci/oofdere. All rights reserved.

#* OBS Websocket Settings
obshost = "localhost"
obsport = 4444
obspass = "obs-spl"
kvcmobs = obsws(obshost, obsport, obspass)
kvcmobs.connect()

class MyEventHandler(PatternMatchingEventHandler):
    def on_modified(self, event):

        # open and read duration
        fileduration = open("duration.txt", 'r', encoding="utf-8")
        global t
        t = int(float(fileduration.read())) # - 3

        print(f"Update!")
       
if __name__ == '__main__':
    path = "."
    event_handler = MyEventHandler(patterns=['*duration.txt'])

    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()

    t = 0 # initial countdown value used until song update
    print("This window shows no output. It might look like nothing is happening but it is running.")
    print("init")

    try:
        starttime = time.time()
        while True:
            if t > 0:
                kvcmobs.call(requests.SetTextGDIPlusProperties("countdown", text=str(datetime.timedelta(seconds=int(t)))))
                t -= 1
            else:
                kvcmobs.call(requests.SetTextGDIPlusProperties("countdown", text="0:00:00"))
            time.sleep(1.0 - ((time.time() - starttime) % 1.0)) # sync to system clock
            
    except KeyboardInterrupt:
        observer.stop()
        kvcmobs.call(requests.SetTextGDIPlusProperties("countdown", text=""))
    observer.join()