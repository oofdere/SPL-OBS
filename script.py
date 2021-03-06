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

import twitch

#! (C)2020 Tibet Tornaci/oofdere. All rights reserved.

#* OBS Websocket Settings
obshost = config['obs-websockets']['host']
obsport = config['obs-websockets']['port']
obspass = str(config['obs-websockets']['password'])
obsinstance = obsws(obshost, obsport, obspass)
obsinstance.connect()
log.info("Connected to OBS!")

#* Twitch Chat Settings
if config['twitch']['enabled'] == "yes":
    twchannel = '#' + config['twitch']['channel']
    twnickname = config['twitch']['nickname']
    twoauth = config['twitch']['oauth']
    twclientid = config['twitch']['clientid']
    chat = twitch.Chat(channel=twchannel, nickname=twnickname, oauth=twoauth, helix=twitch.Helix(client_id=twclientid, use_cache=True))
    log.info("Connected to Twitch Chat!")

def openfile():
    tempfile = []
    fileref = open("input.yml", 'r', encoding="utf-8")
    for data in yaml.safe_load_all(fileref):
        #print(data)
        tempfile.append(data)

    log.info(tempfile)
    log.info("Parsed YAML")
    return tempfile

def quotefree(input_variable):
    """
    this function removes quotes after type conversion to string
    """
    return str(input_variable).strip('"')

def updatercore(service_name: str, title):
    serviceconfig = service_name
    titleconfig = service_name + '-title'
    artistconfig = service_name + '-artist'
    albumconfig = service_name + '-album'

    songname = quotefree(config[titleconfig]['prefix']) + title.get("title")
    artist = ""
    album = ""

    prefix = seperator = quotefree(config[serviceconfig]['prefix'])
    suffix = seperator = quotefree(config[serviceconfig]['suffix'])
    seperator = quotefree(config[serviceconfig]['seperator'])

    if title.get("artist") and quotefree(config[artistconfig]['enabled']) == "yes":
        artist = seperator + quotefree(config[artistconfig]['prefix']) + title.get("artist") + quotefree(config[artistconfig]['suffix'])
        pass

    if title.get("album") and quotefree(config[albumconfig]['enabled']) == "yes":
        album = seperator + quotefree(config[albumconfig]['prefix']).strip('"') + title.get("album") + quotefree(config[albumconfig]['suffix'])
        pass
    
    titlestring = prefix + songname + artist + album + suffix

    return titlestring

def nowplayingupdate(title: dict):
    """
    updates the now playing text
    """

    nowplayingstring = updatercore("nowplaying", title)

    obsinstance.call(requests.SetTextGDIPlusProperties("nowplaying", text=nowplayingstring))

    return console.log(Panel.fit(nowplayingstring, title="Now Playing"))

    pass

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

            titlestring = numstring + updatercore("upcoming", title) + '\n'
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
    titlestring = updatercore("twitch", title)

    #chat.send("!title " + titlestring)

    return console.log(Panel.fit(titlestring, title="Twitch Title"))

class MyEventHandler(PatternMatchingEventHandler):
    def on_modified(self, event):
        logging.info(event)
        
        schedule = openfile()
        nowplaying = next((sub for sub in schedule if sub['index'] == 0), None)
        log.info(nowplaying)

        if config['nowplaying']['enabled'] == "yes":
            nowplayingupdate(nowplaying)

        if config['twitch']['enabled'] == "yes":
            updatetwitchtitle(nowplaying)

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

    if config['twitch']['enabled'] == "yes":
        updatetwitchtitle(nowplaying)

    log.info("End of list")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()