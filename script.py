#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import sys
import time
import datetime

from watchdog.events import PatternMatchingEventHandler
from watchdog.observers import Observer

import yaml

#from threading import Thread
from multiprocessing import Process

from obswebsocket import obsws, requests

from rich.logging import RichHandler
from rich.console import Console
from rich import print
from rich.panel import Panel
console = Console()

FORMAT = "%(message)s"
logging.basicConfig(
    level="INFO", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
)

log = logging.getLogger("rich")

#! (C)2020 Tibet Tornaci/oofdere. All rights reserved.

#* OBS Websocket Settings
obshost = "localhost"
obsport = 4444
obspass = "obs-spl"
kvcmobs = obsws(obshost, obsport, obspass)
kvcmobs.connect()


def openfile():
    tempfile = []
    fileref = open("input.yml", 'r', encoding="utf-8")
    for data in yaml.safe_load_all(fileref):
        #print(data)
        tempfile.append(data)

    log.info(tempfile)
    log.info("Parsed YAML")
    return tempfile

def switchscene(scenename):
    # switches scene in obs  
    
    pass

def nowplayingupdate(title):
    # updates the now playing text
    # title points to a dict
    songname = "🎶" + title.get("title")
    artist = ""
    album = ""

    if title.get("artist"):
        artist = "    👤" + title.get("artist")
        pass

    if title.get("album"):
        album = "    💽" + title.get("album")
        pass
    
    nowplayingstring = songname + artist + album + "             "

    kvcmobs.call(requests.SetTextGDIPlusProperties("nowplaying", text=nowplayingstring))

    return console.log(Panel.fit(nowplayingstring, title="Now Playing"))

    pass

def titletotime(title):
    time = int(title.get("duration"))
    return time

def upcomingupdate(schedulelist):
    # updates the schedule text
    #? This might be slightly faster as a while loop seeing as all the math is already being done on 'i.'
    i = 1
    playlist = """"""
    for title in schedulelist:
        titlestring = ""
        if title["title"]:
            titlestring = str(i) + ". 🎶" + title.get("title", "Nothing scheduled") + " 👤" + title.get("artist", "") + '\n'
            playlist += titlestring
        else:
            pass

        i += 1

        if i > 9:
            kvcmobs.call(requests.SetTextGDIPlusProperties("upnext", text=playlist))
            return console.log(Panel.fit(playlist, title="Up Next"))

        #console.log("Updated Up Next item " + str(i))
    pass

def updatetwitchtitle(title):
    # updates stream title on Twitch via nightbot
    NotImplementedError
    pass

class MyEventHandler(PatternMatchingEventHandler):
    def on_modified(self, event):
        logging.info(event)
        
        schedule = openfile()
        nowplaying = next((sub for sub in schedule if sub['index'] == 0), None)
        log.info(nowplaying)

        nowplayingupdate(nowplaying)
        upcomingupdate(schedule)
       
if __name__ == '__main__':
    path = "."
    event_handler = MyEventHandler(patterns=['*input.yml'])

    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    log.info("Started Watchdog")

    schedule = openfile()
    nowplaying = next((sub for sub in schedule if sub['index'] == 0), None)
    console.log(schedule)

    nowplayingupdate(nowplaying)
    upcomingupdate(schedule)

    log.info("End of list")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()