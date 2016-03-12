#!/usr/bin/python
# -*- coding: utf-8 -*-
from time import sleep, strftime
import sys

"⚫⚫⚫ ⚡ 11:29 11/03 Ⅲ"
while True:
    print("⚫⚫⚫ ⚡ " + strftime("%R %d/%m"), end="")
    sys.stdout.flush()
    sleep(30)
