#!/usr/bin/env python
# -*- coding: utf-8 -*-
from twisted.internet import inotify
from twisted.python import filepath
from twisted.internet import reactor, task, defer
from txdbus import error, client
from time import sleep, strftime
from functools import partial
import sys, random
from txdbus.interface import DBusInterface, Signal, Property, Method
import pretty_dbus as pd

#TODO optimize for minimal writes to stdout

TIME_TICK=20 #seconds
CONNECTION_STATES = ["⚪⚪⚪", "⚫⚪⚪", "⚫⚫⚪", "⚫⚫⚫"]
POWER_STATES = ["⚡", "⚙"]
LANG_STATES = ["Ⅰ", "Ⅱ", "Ⅲ"] #, "Ⅳ"
BARTEXT = ["conn-status", "⚡", "time", "lang"]
SEP = " "

CONNECTION_MAP = {
    10: CONNECTION_STATES[0],
    20: CONNECTION_STATES[0],
    30: CONNECTION_STATES[1],
    40: CONNECTION_STATES[2],
    70: CONNECTION_STATES[3]}                  

def update_title(bar):
    print SEP.join(bar),
    sys.stdout.flush()

def toggle_power_title(*args):
    r = BARTEXT[1] == POWER_STATES[0]
    BARTEXT[1] = POWER_STATES[1] if r else POWER_STATES[0]
    update_title(BARTEXT)

upower_iface = DBusInterface(
    'org.freedesktop.UPower.Device',
    Signal('Changed', ''),
    Property('Online', 'b'))

nmnger_iface = DBusInterface(
    'org.freedesktop.NetworkManager',
    Method('state', '', 'u'),
    Signal('StateChanged', 'u'))

def change_date(bar):
    bar[-2] = strftime("%R %d/%m")
    update_title(bar)

def notify_power(ignored, filepath, mask):
    change_power(BARTEXT)

def set_power_state(bar, states, r):
    bar[1] = states[0] if r else states[1]
    update_title(bar)

def set_bartext_network_state(r):
    BARTEXT[0] = CONNECTION_MAP[r]
    update_title(BARTEXT)

set_bartext_power_state = partial(
    set_power_state,
    BARTEXT,
    POWER_STATES)

update_bartext = partial(update_title, BARTEXT)


if __name__ == '__main__':
    alives = task.LoopingCall(change_date, BARTEXT)
    alives.start(TIME_TICK)

    activate = pd.activate_notification
    update = pd.update_state
    call = pd.call_method
    rcall = reactor.callWhenRunning
    powernotif = (
        activate,
        "system",
        upower_iface,
        "/org/freedesktop/UPower/devices/line_power_AC",
        "Changed",
        toggle_power_title)
    getpower = (
        update,
        "system",
        "org.freedesktop.UPower",
        "/org/freedesktop/UPower/devices/line_power_AC",
        "Online",
        set_bartext_power_state)
    nnotif = (
        activate,
        "system",
        nmnger_iface,
        "/org/freedesktop/NetworkManager",
        "StateChanged",
        set_bartext_network_state)
    getnstate = (
        call,
        "system",
        nmnger_iface,
        "/org/freedesktop/NetworkManager",
        "state",
        set_bartext_network_state)
    rcall(*powernotif)
    rcall(*nnotif)
    rcall(*getpower)
    rcall(*getnstate)
    reactor.run()
