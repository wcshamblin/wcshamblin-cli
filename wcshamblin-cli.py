from os import system, name, environ
from shutil import get_terminal_size
import sys
from webbrowser import open_new_tab
import re

termsize = get_terminal_size() # Returns tuple (x, y)

midx = int(termsize[0]/2)
midy = int(termsize[1]/2)

# MAKE THIS A FOR LOOP FOR GENNING MENUS THIS IS MESSY
# menu={}
# for menuitem in menudex:
#     menu[menuitem] = {"menu": ''.join([])}
menudex = ["Website", "Stuff", "More Stuff", "Other Stuff", "Source Code"]
pushm = "\n"*(termsize[1]-(len(menudex)*2+2))
menu = {"Website": {"menu": """\u001b[0m\u001b[7mWebsite\u001b[0m

Stuff

More Stuff

Other Stuff

Source Code
"""+pushm, "action": None},"Stuff": {"menu": """Website

\u001b[0m\u001b[7mStuff\u001b[0m

More Stuff

Other Stuff

Source Code
"""+pushm, "action": None}, "More Stuff": {"menu": """Website

Stuff

\u001b[0m\u001b[7mMore Stuff\u001b[0m

Other Stuff

Source Code
"""+pushm, "action": None}, "Other Stuff": {"menu": """Website

Stuff

More Stuff

\u001b[0m\u001b[7mOther Stuff\u001b[0m

Source Code
"""+pushm, "action": None}, "Source Code": {"menu": """Website

Stuff

More Stuff

Other Stuff

\u001b[0m\u001b[7mSource Code\u001b[0m
"""+pushm, "action": None}}

helplines = " "*(midx-14)+"arrows to navigate, q to exit\n"+" "*(midx-8)+"enter to execute"

asciiart = {"Website": "       _____       \n"\
"    .-'.  ':'-.    \n"\
"  .''::: .:    '.  \n"\
" /   :::::'      \\ \n"\
";.    ':' `       ;\n"\
"|       '..       |\n"\
"; '      ::::.    ;\n"\
" \\       '::::   / \n"\
"  '.      :::  .'  \n"\
"    '-.___'_.-`     ", "Stuff": " _________ \n"\
"|^|     | |\n"\
"| |_____| |\n"\
"|  _____  |\n"\
"| |     | |\n"\
"| |_____| |\n"\
"|_|_____|_| ", "More Stuff": " _________ \n"\
"|^|     | |\n"\
"| |_____| |\n"\
"|  _____  |\n"\
"| |     | |\n"\
"| |_____| |\n"\
"|_|_____|_| ", "Other Stuff": " _________ \n"\
"|^|     | |\n"\
"| |_____| |\n"\
"|  _____  |\n"\
"| |     | |\n"\
"| |_____| |\n"\
"|_|_____|_| ", "Source Code": " _________ \n"\
"|^|     | |\n"\
"| |_____| |\n"\
"|  _____  |\n"\
"| |     | |\n"\
"| |_____| |\n"\
"|_|_____|_| "}

ascii_enabled = False
if termsize[0] >= max(len(menutitle) for menutitle in menudex)+max(max(len(asciiline) for asciiline in asciiline.split("\n")) for asciiline in asciiart.values())+3:
    ascii_enabled = True

if ascii_enabled:
    ansi_re = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
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
        pushm = "\n"*(termsize[1]-len(concat.split("\n"))-3) # Push
        menu[menuitem]["menu"] = concat+pushm

posix = True
if name == 'nt':
    posix = False

if not posix: # Rewriting is the only way to retain persistence of vision on Windows. Maybe it's because of the buflen?
    def clear():
        system('cls') # ANSI codes don't work without rewriting on CMD + powershell for some fucking reason
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