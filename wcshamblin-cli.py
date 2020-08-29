from os import system, name, environ
from shutil import get_terminal_size
import sys
menu = [
"""\u001b[0m\u001b[7mWebsite\u001b[0m

Stuff

More stuff

Other stuff

Source Code
                    arrows to navigate, q to exit
                          enter to execute
""",
"""Website

\u001b[0m\u001b[7mStuff\u001b[0m

More stuff

Other stuff

Source Code
                    arrows to navigate, q to exit
                          enter to execute
""",
]

posix = True
if name == 'nt':
    posix = False

# def supports_color():
#     plat = sys.platform
#     supported_platform = plat != 'Pocket PC' and (plat != 'win32' or
#                                                   'ANSICON' in environ)
#     # isatty is not always implemented, #6223.
#     is_a_tty = hasattr(sys.stdout, 'isatty') and sys.stdout.isatty()
#     return supported_platform and is_a_tty

termsize = get_terminal_size() # Returns tuple (x, y)
# if not termsize:
#     if not posix:
#         def push_buffer():
#             system('cls')
#     else:
#         def push_buffer():
#             system('clear')
# else:
pushlen = termsize[1] - len(menu[0].split("\n"))-2 # ?
def push_buffer():
    print("\n" * pushlen)

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
                    print(menu[pos])
                    push_buffer()
                if ch == "B" and pos<len(menu)-1: # Down arrow
                    pos+=1
                    print(menu[pos])
                    push_buffer()
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
                push_buffer()
                print(menu[pos])
            if ch == b"P" and pos<len(menu)-1: # Down arrow
                pos+=1
                push_buffer()
                print(menu[pos])
        if ch == b"\r":
            print("Selected")
        if ch == b"q":
            exit()
        return pos


i=0
print(menu[i])
push_buffer()
while 1:
    i = menuhandle(i)