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
config.read('updater.ini', encoding="utf-8")

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
    level=config['debug']['loglevel'], format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
)

log = logging.getLogger("rich")

#! (C)2020 Tibet Tornaci/oofdere. All rights reserved.

#* OBS Websocket Settings
obshost = config['obs-websockets']['host']
obsport = config['obs-websockets']['port']
obspass = str(config['obs-websockets']['password'])
obsinstance = obsws(obshost, obsport, obspass)
obsinstance.connect()
log.info("Connected to OBS!")

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
    songname = str(config['nowplaying-title']['preceding']).strip('"') + title.get("title")
    artist = ""
    album = ""

    if title.get("artist"):
        artist = str(config['nowplaying-artist']['preceding']).strip('"') + title.get("artist")
        pass

    if title.get("album"):
        album = str(config['nowplaying-album']['preceding']).strip('"') + title.get("album")
        pass
    
    nowplayingstring = songname + artist + album + str(config['nowplaying']['seperator']).strip('"')

    obsinstance.call(requests.SetTextGDIPlusProperties("nowplaying", text=nowplayingstring))

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
        namestring = ""
        numstring = ""
        artiststring = ""

        if title["title"]:
            if config['upcoming']['number'] == "yes":
                numstring = str(i) + config['upcoming']['afternumber'].strip('"')
            
            if config['upcoming-title']['enabled'] == "yes":
                namestring = config['upcoming-title']['preceding'].strip('"') + title.get("title", "Nothing scheduled")

            if config['upcoming-artist']['enabled'] == "yes":
                artiststring = config['upcoming-artist']['preceding'].strip('"') + title.get("artist")

            titlestring = numstring + namestring + artiststring + '\n'
            playlist += titlestring
        else:
            pass

        i += 1

        if i > int(config['upcoming']['count']):
            obsinstance.call(requests.SetTextGDIPlusProperties("upnext", text=playlist))
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

        if config['nowplaying']['enabled'] == "yes":
            nowplayingupdate(nowplaying)

        if config['upcoming']['enabled'] == "yes":
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

    if config['nowplaying']['enabled'] == "yes":
        nowplayingupdate(nowplaying)

    if config['upcoming']['enabled'] == "yes":
        upcomingupdate(schedule)

    log.info("End of list")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()