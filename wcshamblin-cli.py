from os import system, name
menu = [
"""\u001b[0m\u001b[7mWebsite\u001b[0m

Stuff

More stuff

Other stuff

Source Code
                    🠕 🠗 to navigate, q or e to exit
                           enter to execute
""",
"""Website

\u001b[0m\u001b[7mStuff\u001b[0m

More stuff

Other stuff

Source Code
                    🠕 🠗 to navigate, q or e to exit
                           enter to execute
""",
]
posix = True
def clear():
    system('clear')
if name == 'nt':
    posix = False
    def clear():
        system('cls')


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
                    clear()
                    print(menu[pos])
                if ch == "B" and pos<len(menu)-1: # Down arrow
                    pos+=1
                    clear()
                    print(menu[pos])
        if ch == "\r":
            print("Selected")
        if ch == "q":
            exit()
        return pos
else:
    def menuhandle():
        ch = getch()
        if ch == b"\xe0": # ANSI escape
            ch = getch()
            if ch == b"P" and i>0: # Up arrow
                pos-=1
                clear()
                print(menu[pos])
            if ch == b"Q" and pos<len(menu)-1: # Down arrow
                pos+=1
                clear()
                print(menu[pos])
        if ch == b"\r":
            print("Selected")
        if ch == b"q":
            exit()
        return pos


clear()
i=0
print(menu[i])

while 1:
    i = menuhandle(i)