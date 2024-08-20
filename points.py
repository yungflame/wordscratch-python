# 1 point – A   E   I   O   U   L   N   S   T   R
# 2 points – D   G
# 3 points – B   C   M   P
# 4 points – F   H   V   W   Y
# 5 points – K
# 8 points – J  X
# 10 points – Q  Z

scrabble_points = {
    'a': 1, 'e': 1, 'i': 1, 'o': 1, 'u': 1,
    'l': 1, 'n': 1, 's': 1, 't': 1, 'r': 1,
    'd': 2, 'g': 2,
    'b': 3, 'c': 3, 'm': 3, 'p': 3,
    'f': 4, 'h': 4, 'v': 4, 'w': 4, 'y': 4,
    'k': 5,
    'j': 8, 'x': 8,
    'q': 10, 'z': 10
}

def get_total_points(word):
    lower = word.lower()
    p = 0
    for i in range(0, len(word)):
        p += scrabble_points[lower[i]]

    if len(word) < 5:
        return p
    elif len(word) < 7:
        return int(p * 1.2)
    elif len(word) < 10:
        return int(p * 1.5)
    else:
        return int(p * 2)