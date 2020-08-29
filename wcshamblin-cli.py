from os import system, name, environ
from shutil import get_terminal_size
import sys
menu = [
"""\u001b[0m\u001b[7mWebsite\u001b[0m

Stuff

More Stuff

Other Stuff

Source Code
""",
"""Website

\u001b[0m\u001b[7mStuff\u001b[0m

More Stuff

Other Stuff

Source Code
""",
"""Website

Stuff

\u001b[0m\u001b[7mMore Stuff\u001b[0m

Other Stuff

Source Code
""",
"""Website

Stuff

More Stuff

\u001b[0m\u001b[7mOther Stuff\u001b[0m

Source Code
""",
"""Website
                                         ___  
Stuff                                   |__ \\ 
                                           ) |
More Stuff                                / / 
                                         |_|  
Other Stuff                               _
                                         (_)  
\u001b[0m\u001b[7mSource Code\u001b[0m
""",
]

termsize = get_terminal_size() # Returns tuple (x, y)
midlim = int(termsize[0]/2)
helplines = "\n"*(termsize[1]-(len(menu[0].split("\n"))+2))+" "*(midlim-16)+"arrows to navigate, q to exit\n"+" "*(midlim-8)+"enter to execute"

posix = True
if name == 'nt':
    posix = False

if not posix: # rewriting is faster than pushing out of buffer on Windows
    def clear():
        system('cls') # ANSI codes don't work without rewriting on CMD + powershell
    clear()

# def ansi_active(): # Taken from https://github.com/django/django/blob/master/django/core/management/color.py
#     supported_platform = sys.platform != 'win32' or 'ANSICON' in os.environ
#     is_a_tty = hasattr(sys.stdout, 'isatty') and sys.stdout.isatty()
#     return supported_platform and is_a_tty

def get_getch():
    try:
        import termios
    except ImportError as error:
        # Not POSIX
        import msvcrt
        return msvcrt.getch
    import sys, tty
    # POSIX
    def getch():
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch
    return getch

getch = get_getch()

if posix:
    def menuhandle(pos):
        ch = getch()
        if ch == "\x1b": # ANSI escape
            ch = getch()
            if ch == "[": # Func call
                ch = getch()
                if ch == "A" and pos>0: # Up arrow
                    pos-=1
                    print(menu[pos], helplines)
                if ch == "B" and pos<len(menu)-1: # Down arrow
                    pos+=1
                    print(menu[pos], helplines)
        if ch == "\r":
            print("Selected")
        if ch == "q":
            exit()
        return pos
else:
    def menuhandle(pos):
        ch = getch()
        if ch == b"\xe0": # ANSI escape
            ch = getch()
            if ch == b"H" and i>0: # Up arrow
                pos-=1
                print(menu[pos],helplines)
                clear()
            if ch == b"P" and pos<len(menu)-1: # Down arrow
                pos+=1
                print(menu[pos], helplines)
                clear()
        if ch == b"\r":
            print("Selected")
        if ch == b"q":
            exit()
        return pos
i=0
print(menu[0], helplines)
while 1:
    i = menuhandle(i)