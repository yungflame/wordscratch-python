import sys
import os

dictionary = set()


def get_file_path(filename):
    if getattr(sys, 'frozen', False):
        # If running as a frozen executable
        return os.path.join(sys._MEIPASS, filename)
    else:
        # If running as a script
        return os.path.join(os.path.dirname(__file__), filename)


unix_dictionary = get_file_path('scrabble.txt')
with open(unix_dictionary, 'r') as file:
    for line in file:
        dictionary.add(line.strip().lower())


def is_word(word, king_word):
    lower = word.lower()
    if lower == king_word.lower():
        return True
    return lower in dictionary
