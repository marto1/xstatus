#include <X11/Xlib.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>
#include <limits.h>

/*
  
*/

int
main(int argc, char *argv[])
{
   Display *d;
   Window w;
   Window winToEmbedInto = None;
   XEvent e;
   int s;
   char *endPtr;
   char buffer[10];
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
       XStoreName(d, w, "⚫⚪⚪ ⚡ 20:29 11/03 Ⅲ");
       XReparentWindow(d, w, winToEmbedInto, 0, 0);
       XMapWindow(d, w);

 
       while (1) {	   
       	   XNextEvent(d, &e);
       }
 
       XCloseDisplay(d);
   }
   return 0;
}
