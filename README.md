Description
===========

A window with dynamic title that can be embedded into another X window.

Build with `make`. Template from tabbed's Makefile. 

Dependencies
============

* xlib

Usage
=====

`xstatus \<id of parent window\>`

Get date in separate window: `(while sleep 1; do date; done) | ./xstatus`

Get date in embedded tab: `(while sleep 1; do date; done) | ./xstatus <0xid of window>`

Usage in tabbed: `python pp.py | ./xstatus <0xid of tabbed>`

Demo
====

![Alt Text](https://raw.githubusercontent.com/marto1/xstatus/master/exmp1.png)




