from os import system, name, environ
from shutil import get_terminal_size
import sys
from webbrowser import open_new_tab
import re

def website():
    print("Open website")

def sourcecode():
    print("Open GH")

def contact():
    print("mailto://wcshamblin@gmail.com")

termsize = get_terminal_size() # Returns tuple (x, y)

midx = int(termsize[0]/2)
midy = int(termsize[1]/2)

menudex = ["Website", "Stuff", "More Stuff", "Source Code", "Contact"]
actions = {"Website": website, "Stuff": website, "More Stuff": website, "Source Code": sourcecode, "Contact": contact}

pushm = "\n"*(termsize[1]-(len(menudex)*2+2))
menu = {}
for menuitem in menudex:
    menu[menuitem] = {"menu": '\n\n'.join([("\u001b[0m\u001b[7m"+menutext+"\u001b[0m" if menutext is menuitem else menutext) for menutext in menudex])+pushm}

helplines = " "*(midx-14)+"arrows to navigate, q to exit\n"+" "*(midx-8)+"enter to execute"

# Min linenum and linelen have to be uniform, or something
asciiart = {"Website":
"       _____       \n"\
"    .-'.  ':'-.    \n"\
"  .''::: .:    '.  \n"\
" /   :::::'      \\ \n"\
";.    ':' `       ;\n"\
"|       '..       |\n"\
"; '      ::::.    ;\n"\
" \\       '::::   / \n"\
"  '.      :::  .'  \n"\
"    '-.___'_.-`     ",

"Stuff":
" _________ \n"\
"|^|     | |\n"\
"| |_____| |\n"\
"|  _____  |\n"\
"| |     | |\n"\
"| |_____| |\n"\
"|_|_____|_| ",

"More Stuff":
" _________ \n"\
"|^|     | |\n"\
"| |_____| |\n"\
"|  _____  |\n"\
"| |     | |\n"\
"| |_____| |\n"\
"|_|_____|_| ",

"Source Code":
" _________ \n"\
"|^|     | |\n"\
"| |_____| |\n"\
"|  _____  |\n"\
"| |     | |\n"\
"| |_____| |\n"\
"|_|_____|_| ",

"Contact":
" ____________________ \n"\
"|\\                  /|\n"\
"| \\                / |\n"\
"|  \\              /  |\n"\
"|  /\\____________/\\  |\n"\
"| /                \\ |\n"\
"|/__________________\\| "}

ascii_enabled = False
if termsize[0] >= max(len(menutitle) for menutitle in menudex)+max(max(len(asciiline) for asciiline in asciiline.split("\n")) for asciiline in asciiart.values())+3:
    ascii_enabled = True

if ascii_enabled:
    ansi_re = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])') # Regex for ANSI
    # Concat menu and asciiart
    for menuitem, menutext in menu.items():
        concat = ""
        menusplit = menutext["menu"].splitlines(True)
        asciisplit = asciiart[menuitem].splitlines(True)

        if len(menusplit) > len(asciisplit):
            asciisplit = asciisplit+['\n' for i in range((len(menusplit)-len(asciisplit)))]

        if len(asciisplit) > len(menusplit):
            menusplit = menusplit+['\n' for i in range((len(asciisplit)-len(menusplit)))]

        for ml, al in zip(menusplit, asciisplit):
            ml = ml.replace("\n", "")
            alignto = " "*(termsize[0]-len(ansi_re.sub('', ml))-len(al)-2) # Right align art + 2 cols
            concat+=ml+alignto+al
        pushm = "\n"*(termsize[1]-len(concat.split("\n"))-3) # Pushlen
        menu[menuitem]["menu"] = concat+pushm

posix = True
if name == 'nt':
    posix = False

if not posix: # Rewriting is the only way to retain persistence of vision on Windows. Maybe it's because of the buflen?
    def clear():
        system('cls') # ANSI codes don't work without rewriting on CMD + powershell for some fucking reason
    clear()

def get_getch():
    try:
        import termios
    except ImportError as error:
        # Not POSIX
        import msvcrt
        return msvcrt.getch
    # POSIX
    import sys, tty
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
                    print(menu[menudex[pos]]["menu"]+helplines)
                if ch == "B" and pos<len(menu)-1: # Down arrow
                    pos+=1
                    print(menu[menudex[pos]]["menu"]+helplines)
        if ch == "\r":
            actions[menudex[pos]]()
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
                clear()
                print(menu[menudex[pos]]["menu"]+helplines)
            if ch == b"P" and pos<len(menu)-1: # Down arrow
                pos+=1
                clear()
                print(menu[menudex[pos]]["menu"]+helplines)
        if ch == b"\r":
            print("Selected")
        if ch == b"q":
            exit()
        return pos
i=0
print(menu[menudex[0]]["menu"]+helplines)
while 1:
    i = menuhandle(i)