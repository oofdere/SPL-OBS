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

logging.basicConfig(level=logging.DEBUG)

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

    #print(tempfile)
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

    print(f"Updated Now Playing")

    pass

def titletotime(title):
    time = int(title.get("duration"))
    return time

def upcomingupdate(schedulelist):
    # updates the schedule text
    schedulefile = open("schedule.txt", 'w', encoding='utf8') 

    #? This might be slightly faster as a while loop seeing as all the math is already being done on 'i.'
    i = 1
    playlist = """"""
    for title in schedulelist:
        titlestring = ""
        if title["title"]:
            titlestring = str(i) + ". 🎶" + title.get("title", "Nothing scheduled") + " 👤" + title.get("artist", "") + '\n'
            playlist += titlestring
        else:
            #print("Nothing programmed.")
            pass

        i += 1
        
        #schedulefile.write(titlestring)
        #schedulefile.write('\n')

        if i > 9:
            kvcmobs.call(requests.SetTextGDIPlusProperties("upnext", text=playlist))
            return 0

        print(f"Updated Up Next item " + str(i))
    pass

def updatetwitchtitle(title):
    # updates stream title on Twitch via nightbot
    NotImplementedError
    pass

class MyEventHandler(PatternMatchingEventHandler):
    def on_modified(self, event):
        logging.debug(event)
        
        #print(f"Updating...")
        schedule = openfile()
        nowplaying = next((sub for sub in schedule if sub['index'] == 0), None)
        print(nowplaying)

        nowplayingupdate(nowplaying)
        upcomingupdate(schedule)
       
if __name__ == '__main__':
    path = "."
    event_handler = MyEventHandler(patterns=['*input.yml'])

    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()

    schedule = openfile()
    nowplaying = next((sub for sub in schedule if sub['index'] == 0), None)
    print(schedule)
    print("init")

    nowplayingupdate(nowplaying)
    upcomingupdate(schedule)

    print("End of list")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()