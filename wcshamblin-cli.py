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

def clear():
    system('cls' if name == 'nt' else 'clear')

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

clear()
i=0
print(menu[i])

while 1:
    ch = getch()
    if ch == "\x1b" or ch == b"\xe0": # ANSI escape
        ch = getch()
        if ch == "[": # Func call
            ch = getch()
            if ch == "A" or ch == b"H" and i>0: # Up arrow
                i-=1
                clear()
                print(menu[i])
            if ch == "B" or ch == b"P" and i<len(menu)-1: # Down arrow
                i+=1
                clear()
                print(menu[i])

    if ch == "\r":
        print("Selected")
    if ch == "q" or ch == "e":
        exit()