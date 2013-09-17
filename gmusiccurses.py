#!/usr/bin/env python

import curses
import subprocess
import sys
import os

from gmusicapi import Webclient

screen = curses.initscr()
api = Webclient()
mainsonglist = []
player = None
lastcurrstart = 0
lastpos = 1


def mainmenu():
    curses.initscr()
    curses.start_color()
    curses.init_pair(1,curses.COLOR_RED, curses.COLOR_WHITE)
    screen.keypad(1)
    pos = 1
    x = None
    h = curses.color_pair(1)
    n = curses.A_NORMAL
    while x != ord('\n'):
        screen.clear()
        screen.border(0)
        screen.addstr(2,2,"pTunes Music Player",curses.A_STANDOUT)
        screen.addstr(4,2,"Select an option...",curses.A_BOLD)
        if pos == 1:
            screen.addstr(5,4,"1 - Log In",h)
        else:
            screen.addstr(5,4,"1 - Log In",n)
        if pos == 2:
            screen.addstr(6,4,"2 - List Songs",h)
        else:
            screen.addstr(6,4,"2 - List Songs",n)
        if pos == 3:
            screen.addstr(7,4,"3 - Exit",h)
        else:
            screen.addstr(7,4,"3 - Exit",n)
        screen.refresh()
        x = screen.getch()
        if x == ord('1'):
            pos = 1
        elif x == ord('2'):
            pos = 2
        elif x == ord('3'):
            pos = 3
        elif x == 258:
            if pos < 3:
                pos += 1
            else:
                pos = 1
        elif x == 259:
            if pos > 1:
                pos += -1
            else:
                pos = 1
        elif x != ord('\n'):
            curses.flash()
        
    return str(pos)

def songselect():
    global lastcurrstart
    global lastpos
    screen.clear()
    screen.border(0)
    
    menuitems = []
    songdata = []
    mainsonglist = api.get_all_songs()
    mainsonglist = sorted(mainsonglist,key=lambda k: k["title"])
    for s in range(0,len(mainsonglist)-1):
        menuitems.append(mainsonglist[s]["title"])
    
    pos = lastpos
    currstart = lastcurrstart
    x = None
    h = curses.color_pair(1)
    n = curses.A_NORMAL
    while x != ord('\n'):
        screen.clear()
        screen.border(0)
        for item in range(currstart,15):
            screen.clear()
            screen.border(0)
            screen.addstr(item+2,2,menuitems[item])
        if pos == 1:
            screen.addstr(2,2,menuitems[currstart],h)
        else:
            screen.addstr(2,2,menuitems[currstart],n)
        if pos == 2:
            screen.addstr(3,2,menuitems[currstart+1],h)
        else:
            screen.addstr(3,2,menuitems[currstart+1],n)
        if pos == 3:
            screen.addstr(4,2,menuitems[currstart+2],h)
        else:
            screen.addstr(4,2,menuitems[currstart+2],n)
        if pos == 4:
            screen.addstr(5,2,menuitems[currstart+3],h)
        else:
            screen.addstr(5,2,menuitems[currstart+3],n)
        if pos == 5:
            screen.addstr(6,2,menuitems[currstart+4],h)
        else:
            screen.addstr(6,2,menuitems[currstart+4],n)
        if pos == 6:
            screen.addstr(7,2,menuitems[currstart+5],h)
        else:
            screen.addstr(7,2,menuitems[currstart+5],n)
        if pos == 7:
            screen.addstr(8,2,menuitems[currstart+6],h)
        else:
            screen.addstr(8,2,menuitems[currstart+6],n)
        if pos == 8:
            screen.addstr(9,2,menuitems[currstart+7],h)
        else:
            screen.addstr(9,2,menuitems[currstart+7],n)
        if pos == 9:
            screen.addstr(10,2,menuitems[currstart+8],h)
        else:
            screen.addstr(10,2,menuitems[currstart+8],n)
        if pos == 10:
            screen.addstr(11,2,menuitems[currstart+9],h)
        else:
            screen.addstr(11,2,menuitems[currstart+9],n)
        if pos == 11:
            screen.addstr(12,2,menuitems[currstart+10],h)
        else:
            screen.addstr(12,2,menuitems[currstart+10],n)
        if pos == 12:
            screen.addstr(13,2,menuitems[currstart+11],h)
        else:
            screen.addstr(13,2,menuitems[currstart+11],n)
        if pos == 13:
            screen.addstr(14,2,menuitems[currstart+12],h)
        else:
            screen.addstr(14,2,menuitems[currstart+12],n)
        if pos == 14:
            screen.addstr(15,2,menuitems[currstart+13],h)
        else:
            screen.addstr(15,2,menuitems[currstart+13],n)
        if pos == 15:
            try:
                screen.addstr(16,2,menuitems[currstart+14],h)
            except UnicodeEncodeError:
                menuuitems[currstart+14] = "Encoding Error"
                screen.addstr(16,2,menuitems[currstart+14],n)
        else:
            try:
                screen.addstr(16,2,menuitems[currstart+14],n)
            except UnicodeEncodeError:
                menuitems[currstart+14] = "Encoding Error"
                screen.addstr(16,2,menuitems[currstart+14],n)
        screen.refresh()
        x = screen.getch()
        if x == ord('1'):
            pos = 1
        elif x == 258:
            if pos < 15:
                pos += 1
            else:
                pos = 1
        elif x == 259:
            if pos > 1:
                pos += -1
            else:
                pos = 1
        elif x == int(curses.KEY_NPAGE):
            tracker = currstart + 10
            screen.clear()
            screen.border(0)
            try:
                tracker = menuitems[currstart+15]
                currstart += 1
            except IndexError:
                currstart = 0
        elif x == int(curses.KEY_PPAGE):
            if currstart > 0:
                tracker = currstart + 10
                screen.clear()
                screen.border(0)
                try:
                    tracker = menuitems[currstart-1]
                    currstart -= 1
                except IndexError:
                    currstart = 0
    lastcurrstart = currstart
    lastpos = pos                
    return mainsonglist[currstart+pos-1]

def songplayer(song):
    global player
    screen.clear()
    screen.border(0)
    
    h = curses.color_pair(1)
    n = curses.A_NORMAL
    x = None
    pos = 1
    playing = False
    stop = False
    while stop == False:
        screen.clear()
        screen.border(0)
        screen.addstr(2,2,"Title: " + song["title"],curses.A_BOLD)
        screen.addstr(3,2,"Album: " + song["album"],curses.A_NORMAL)
        screen.addstr(4,2,"Artist: " + song["artist"],curses.A_NORMAL)
        if "year" in song:
            screen.addstr(5,2,"Year: " + str(song["year"]),curses.A_NORMAL)
        else:
            screen.addstr(5,2,"Year: ",curses.A_NORMAL)
        if pos == 1:
            screen.addstr(7,2,"<Play>",h)
        else:
            screen.addstr(7,2,"<Play>",n)
        if pos == 2:
            screen.addstr(7,9,"<Stop>",h)
        else:
            screen.addstr(7,9,"<Stop>",n)
        if playing == True:
            screen.addstr(6,2,"Playing...",n)
        else:
            screen.addstr(6,2,"Not playing",n)
        screen.refresh()
        x = screen.getch()
        if x == ord('p'):
            pos = 1
        elif x == 258:
            if pos < 2:
                pos += 1
            else:
                pos = 1
        elif x == 259:
            if pos > 1:
                pos += -1
            else:
                pos = 1
        elif x == ord('\n'):
            if pos == 1:
                playing = True
                player = play(api.get_stream_urls(song['id'])[0])
            else:
                if player != None:
                    player.terminate()
                playing = False
                stop = True
                
    selectedsong = songselect()
    screen.clear()
    screen.border(0)
    songplayer(selectedsong)

def play(song):
    with open(os.devnull, 'w') as temp:
        proc =  subprocess.Popen(["mplayer", "-noconfig", "all","%s" % song], stdin=subprocess.PIPE, stdout=temp, stderr=temp)
        return proc

selection = mainmenu()
if selection == '1':
    screen.clear()
    screen.border(0)
    screen.addstr(2,2,"Please enter your account info:",curses.A_BOLD)
    screen.addstr(4,2,"E-Mail: ")
    googlemail = screen.getstr()
    screen.addstr(5,2,"Password: ")
    googlepass = screen.getstr()
    api.login(googlemail,googlepass)
    
    selection = mainmenu()
    if selection == '2':
        selectedsong = songselect()
        screen.clear
        screen.border(0)
        songplayer(selectedsong)
    curses.endwin()

elif selection == '2':
    selectedsong = songselect()
    screen.clear()
    screen.border(0)
    songplayer(selectedsong)

elif selection == '3':
    curses.endwin()
