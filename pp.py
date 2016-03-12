#!/usr/bin/env python
# -*- coding: utf-8 -*-
from twisted.internet import reactor, task
from time import sleep, strftime
from functools import partial
import sys, random

TIME_TICK=20 #seconds
CONNECTION_STATES = ["NOP", "ETH", "⚫⚪⚪", "⚫⚫⚪", "⚫⚫⚫"]
POWER_STATES = ["⚡", "⚙"]
LANG_STATES = ["Ⅰ", "Ⅱ", "Ⅲ"] #, "Ⅳ"
BARTEXT = ["conn-status", "power", "time", "lang"]
SEP = " "

def update_title(bar):
    print SEP.join(bar),
    sys.stdout.flush()

def change_date(bar):
    bar[-2] = strftime("%R %d/%m")
    update_title(bar)

update_bartext = partial(update_title, BARTEXT)

if __name__ == '__main__':

    alives = task.LoopingCall(change_date, BARTEXT)
    alives.start(TIME_TICK)

    reactor.run()
