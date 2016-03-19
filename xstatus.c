/*
  See LICENSE file for copyright and license details. 
  xstatus <parent> <- will embed the window to the specified parent,
  stdin is read on data arrival(!) and received data becomes
  the new title.
*/
#include <X11/Xlib.h>
#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>
#include <limits.h>
#include <poll.h>
#include "config.h"

int
main(int argc, char *argv[])
{
  Display *d;
  Window w;
  Window winToEmbedInto = None;
  XEvent e;
  int s,xfd;
  int rv;
  char *endPtr;
  char buffer[STDIN_BUFFER_SIZE];
  struct pollfd fds[2];
  if (argc > 1) {
    winToEmbedInto = (Window) strtol(argv[1], &endPtr, 0);
    if ((errno == ERANGE && (winToEmbedInto == LONG_MAX || winToEmbedInto == LONG_MIN))
	|| (errno != 0 && winToEmbedInto == 0)) {
      perror("strtol");
      exit(EXIT_FAILURE);
    }
    d = XOpenDisplay(NULL);
    if (d == NULL) {
      fprintf(stderr, "Cannot open display\n");
      exit(1);
    }

    s = DefaultScreen(d);
    w = XCreateSimpleWindow(d, RootWindow(d, s), 0, 0, 500, 500, 1,
			    BlackPixel(d, s), BlackPixel(d, s));
    XSelectInput(d, w, ExposureMask | KeyPressMask);
    XReparentWindow(d, w, winToEmbedInto, 0, 0);
    XMapWindow(d, w);
    xfd = ConnectionNumber(d);
    fds[0].fd = xfd;
    fds[0].events = POLLIN;
    fds[1].fd = STDIN_FILENO;
    fds[1].events = POLLIN;

    while (1) {
      rv = poll(fds, 2, -1);
      if (rv == -1) {
	perror("poll");
      }
      if (fds[1].revents & POLLIN) {
	memset(buffer, 0, STDIN_BUFFER_SIZE);
	read(STDIN_FILENO, buffer, STDIN_BUFFER_SIZE);
	XStoreName(d, w, buffer);
      }
      while(XPending(d) != 0)
	XNextEvent(d, &e);
    }

    XCloseDisplay(d);
  }
  return 0;
}
