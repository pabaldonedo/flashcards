import string
import termios, sys, os
from random import shuffle

def cls():
    os.system(['clear','cls'][os.name == 'nt'])

def extract_vocabulary(name_list):
    
    vocabulary = []
    for name in name_list:
        try:
            with open(name, 'r') as f:
                for line in f:
                    sep = string.split(line, '->')
                    t = tuple(sep)
                    vocabulary.append(t)
        except IOError:
            print 'File ', name, ' not found'
            sys.exit()
    return vocabulary


def show(words, show_answer):
    cls()
    if not show_answer:
        print words[0]
    else:
        print '%s -> %s' % (words[0], words[1])
    



def getkey():
    TERMIOS = termios
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    new = termios.tcgetattr(fd)
    new[3] = new[3] & ~TERMIOS.ICANON & ~TERMIOS.ECHO
    new[6][TERMIOS.VMIN] = 1
    new[6][TERMIOS.VTIME] = 0
    termios.tcsetattr(fd, TERMIOS.TCSANOW, new)
    c = None
    try:
        c = os.read(fd, 1)
    finally:
        termios.tcsetattr(fd, TERMIOS.TCSAFLUSH, old)
    return c
    
    
def parse_input(key, i, sh, length):
    index = i
    if key == 's':
        index += sh
        if index == length:
            return i, sh
        show_answer = (sh+1)%2
        return index, show_answer
    if key == 'a':
        index += -1 + sh
        show_answer = (sh-1)
        return max(index,0), max(show_answer, 0)
    if key == 'q':
        return -1,0
    return i,sh
def main(name):
    print name
    voc = extract_vocabulary(name)
    shuffle(voc)
    index = 0
    show_answer = 0
    print 'Welcome to flash cards!'
    print "use 's' to see the translation of the current word or move to a new word"
    print "use 'a' to go to the previous word"
    print "use 'q' to quit"
    print "Now press any key to get starting"
    _ = getkey()
    while index is not -1:
        show(voc[index], show_answer)
        #key = raw_input()
        key = getkey()
        index, show_answer = parse_input(key, index, show_answer, len(voc))

if __name__ == "__main__":
    names = sys.argv
    if len(names) == 1:
        print "No vocabulary file set, use 'python flashcards.py textfiles' to run the program"
    else:
        main(names[1:])