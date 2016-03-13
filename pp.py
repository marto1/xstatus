#!/usr/bin/env python
# -*- coding: utf-8 -*-
from twisted.internet import inotify
from twisted.python import filepath
from twisted.internet import reactor, task, defer
from txdbus import error, client
from time import sleep, strftime
from functools import partial
import sys, random
from twisted.internet import abstract
from txdbus.interface import DBusInterface, Signal, Property

TIME_TICK=20 #seconds
CONNECTION_STATES = ["NOP", "ETH", "⚫⚪⚪", "⚫⚫⚪", "⚫⚫⚫"]
POWER_STATES = ["⚡", "⚙"]
LANG_STATES = ["Ⅰ", "Ⅱ", "Ⅲ"] #, "Ⅳ"
BARTEXT = ["conn-status", "⚡", "time", "lang"]
SEP = " "


def update_title(bar):
    print SEP.join(bar),
    sys.stdout.flush()

def update_power_state(*args):
    BARTEXT[1] = POWER_STATES[0] if BARTEXT[1] == POWER_STATES[0] else POWER_STATES[1]
    update_title(BARTEXT)

upower_iface = DBusInterface('org.freedesktop.UPower.Device',
                             Signal('Changed', ''),
                             Property('Online', 'b'))

@defer.inlineCallbacks
def activate_power_notification():
    try:
        cli   = yield client.connect(reactor, 'system')
        robj  = yield cli.getRemoteObject('org.freedesktop.UPower', '/org/freedesktop/UPower/devices/line_power_AC', upower_iface)

        robj.notifyOnSignal('Changed', update_power_state)

    except error.DBusException, e:
        print 'DBus Error:', 

@defer.inlineCallbacks
def update_power_state():
    try:
        cli   = yield client.connect(reactor, 'system')
        robj  = yield cli.getRemoteObject('org.freedesktop.UPower', '/org/freedesktop/UPower/devices/line_power_AC') #, upower_iface)

        r = yield robj.callRemote('Get', '', 'Online')
        BARTEXT[1] = POWER_STATES[0] if r else POWER_STATES[1]
        update_title(BARTEXT)

    except error.DBusException, e:
        print 'DBus Error:', 


def change_date(bar):
    bar[-2] = strftime("%R %d/%m")
    update_title(bar)

def notify_power(ignored, filepath, mask):
    print "CHANGE!!!"
    change_power(BARTEXT)
    
update_bartext = partial(update_title, BARTEXT)

if __name__ == '__main__':

    alives = task.LoopingCall(change_date, BARTEXT)
    alives.start(TIME_TICK)
    
    reactor.callWhenRunning(update_power_state)
    reactor.callWhenRunning(activate_power_notification)
    reactor.run()
