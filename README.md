A window with dynamic title that can be embedded into another X window.

Build with make. Template from tabbed's Makefile. 

Depends on: xlib

Usage: xstatus \<id of parent window\>

Example to get date in separate window: (while sleep 1; do date; done) | ./xstatus

Example to get date in embedded tab: (while sleep 1; do date; done) | ./xstatus <0xid of window> 

Example usage in tabbed: python pp.py | ./xstatus <0xid of tabbed> 

![Alt Text](https://raw.githubusercontent.com/marto1/xstatus/master/exmp1.png)


