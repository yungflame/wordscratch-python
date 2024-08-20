import random


def place_word_on_board(board, word):
    size = len(board)
    word_length = len(word)

    # Randomly choose a starting position on the board
    start_row = random.randint(0, size - 1)
    start_col = random.randint(0, size - 1)

    board[start_row][start_col] = word[0]
    current_row, current_col = start_row, start_col

    for i in range(1, word_length):
        # Get all possible adjacent positions within bounds (no wrapping)
        possible_positions = []
        for r in range(-1, 2):
            for c in range(-1, 2):
                if r == 0 and c == 0:
                    continue  # Skip the current position
                new_row = current_row + r
                new_col = current_col + c
                if 0 <= new_row < size and 0 <= new_col < size and board[new_row][new_col] == '':
                    possible_positions.append((new_row, new_col))

        # If no valid positions are found, break out of the loop
        if not possible_positions:
            raise ValueError("Something went wrong!")

        # Choose a random valid adjacent position
        new_row, new_col = random.choice(possible_positions)
        board[new_row][new_col] = word[i]
        current_row, current_col = new_row, new_col