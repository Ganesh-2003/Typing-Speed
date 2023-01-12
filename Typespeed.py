import curses
from curses import wrapper
import time
import random


def start_screen(stdscr):
    stdscr.clear()
    stdscr.addstr("Hello, Buddy, Welcome to Typing Test!")
    stdscr.addstr("\nPress any key to continue")
    stdscr.refresh()
    stdscr.getkey()


def display_text(stdscr, target, current, wpm):
    stdscr.addstr(target)
    if (wpm >= 60):
        stdscr.addstr(1, 0, f"WPM: {wpm}")
        stdscr.addstr(
            3, 0, "*** WOW LOOK AT YOUR SPEED ! YOU ARE AT TOP 10% TYPISTS OUT THERE ***")

    elif (wpm >= 30):
        stdscr.addstr(1, 0, f"WPM: {wpm}")
        stdscr.addstr(
            3, 0, "*** THIS SPEED IS REQUIRED FOR REGULAR JOBS U CAN BE A PROFESSIONAL TYPIST ***")

    elif (wpm >= 20):
        stdscr.addstr(1, 0, f"WPM: {wpm}")
        stdscr.addstr(
            3, 0, "*** YOU ARE AN AVERAGE TYPIST LOL! ***")
    elif (wpm == 0):
        stdscr.addstr(1, 0, f"WPM: {wpm}")
        stdscr.addstr(
            3, 0, "*** BRO ! START TYPING ***")

    else:
        stdscr.addstr(1, 0, f"WPM: {wpm}")
        stdscr.addstr(
            2, 0, "*** LEARN THE PROPER WAY TO TYPE AND IMPROVE BRO ***")

    for i, char in enumerate(current):
        correct_char = target[i]
        color = curses.color_pair(1)
        if char != correct_char:
            color = curses.color_pair(2)

        stdscr.addstr(0, i, char, color)


def load_text():
    with open("text.txt", "r") as f:
        lines = f.readlines()
        return random.choice(lines).strip()


def wpm_test(stdscr):
    target_text = load_text()
    current_text = []
    start_time = time.time()
    wpm = 0
    stdscr.nodelay(True)

    while True:
        time_elapsed = max(time.time() - start_time, 1)
        wpm = round((len(current_text) / (time_elapsed/60))/5)

        stdscr.clear()
        display_text(stdscr, target_text, current_text, wpm)
        stdscr.refresh()

        if "".join(current_text) == target_text:
            stdscr.nodelay(False)
            break

        try:
            key = stdscr.getkey()
        except:
            continue

        if ord(key) == 27:
            break

        if key in ("KEY_BACKSPACE", '\b', '\x7f'):
            if len(current_text) > 0:
                current_text.pop()
        elif (len(current_text) < len(target_text)):
            current_text.append(key)


def main(stdscr):
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)

    start_screen(stdscr)
    while True:
        wpm_test(stdscr)

        stdscr.addstr(
            5, 0, "Hey! You Completed the test.Do you want to play again?")
        stdscr.addstr(
            7, 0, "Press Any key to continue and press (ESC to exit)")
        key = stdscr.getkey()

        if ord(key) == 27:
            break


wrapper(main)
print("Welcome")
