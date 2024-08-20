import random
from tkinter import *
from gre_words import gre_words

from place_word_on_board import place_word_on_board
from dictionary import is_word
from points import get_total_points

class BoggleGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Sharon's Game")
        self.points = 0
        self.used_words = set()
        self.king_word = 'Sharon'
        self.studied_words = set()

        # Initialize board
        self.board_size = 5

        # Canvas setup
        self.board_dimension = 250

        # definition canvas
        self.current_letter_index = 0
        self.letters = []
        self.definition_canvas = Canvas(self.root, width=self.board_dimension, height=175, bg='white')
        self.definition_canvas.pack()

        # word board canvas
        self.lines = []
        self.cell_size = self.board_dimension // self.board_size
        self.word_board_canvas = Canvas(self.root, width=self.board_dimension, height=self.board_dimension,
                                        bg='white')
        self.word_board_canvas.pack()

        self.board = [[None for _ in range(self.board_size)] for _ in range(self.board_size)]

        # points and notes canvas
        self.points_canvas = Canvas(self.root, width=self.board_dimension, height=70,
                                        bg='yellow')
        self.points_canvas.pack()
        self.points_text = self.points_canvas.create_text(125, 50, text="", font=("Helvetica", 16), fill="blue")
        self.note_text = None
        self.points_text = None


        self.new_board()

        # gameplay buttons

        # Bind mouse events
        self.word_board_canvas.bind("<Button-1>", self.on_click)
        self.word_board_canvas.bind("<B1-Motion>", self.on_drag)
        self.word_board_canvas.bind("<ButtonRelease-1>", self.on_release)


        # control buttons
        reveal_word_button = Button(root,
                                    text="Reveal Word",
                                    command=self.reveal_word,
                                    activebackground="blue",
                                    activeforeground="white")
        reveal_word_button.pack(side=RIGHT, padx=10, pady=10)

        new_board_button = Button(root,
           text="New Board",
           command=self.new_board,
           activebackground="blue",
           activeforeground="white")
        new_board_button.pack(side=RIGHT, padx=10, pady=10)

        self.win_text = None


    def clear_board(self):
        for i in range(self.board_size):
            for j in range(self.board_size):
                self.board[i][j] = ''


    def split_definition_into_lines(self, long_string):
        words = long_string.split()  # Split the text into words
        lines = []
        current_line = []

        for word in words:
            # Check if adding this word would exceed the line length
            if sum(len(w) for w in current_line) + len(word) + len(current_line) > 30:
                # Join the current line into a string and append it to lines
                lines.append(' '.join(current_line))
                # Start a new line with the current word
                current_line = [word]
            else:
                # Add the word to the current line
                current_line.append(word)

        # Don't forget to add the last line if there are remaining words
        if current_line:
            lines.append(' '.join(current_line))

        return lines


    def draw_key_word(self, word):
        num_lines = len(word)

        # Calculate spacing between lines and vertical offset
        line_spacing = 5  # Space between lines
        line_length = 12

        # Calculate the starting y position to center lines vertically
        y = 165
        x_start = 20

        for i in range(num_lines):
            # Center each line horizontally
            word_start = x_start + 10
            x_end = x_start + line_length
            self.definition_canvas.create_line(x_start, y, x_end, y, fill='black', width=2)

            letter = self.definition_canvas.create_text(word_start, y - 20, text=word[i], font=("Arial", 12), fill='black')
            self.definition_canvas.itemconfig(letter, state='hidden')
            self.letters.append(letter)

            x_start = x_end + line_spacing


    def new_letter_board(self, word):
        self.word_board_canvas.delete('all')
        self.draw_grid()
        self.clear_board()
        self.draw_letter_board(word.upper())


    def new_definition_board(self, word, definition):
        self.definition_canvas.delete('all')
        self.current_letter_index = 0
        self.letters = []

        definition_lines = self.split_definition_into_lines(definition)
        self.definition_canvas.create_rectangle(10, 10, 240, 125, fill='white', width=3)
        start_y = 40
        for line in definition_lines:
            self.definition_canvas.create_text(125, start_y, text=line, fill="black", font=('Helvetica', 10))
            start_y += 15

        self.draw_key_word(word)


    def new_points_board(self, l):
        self.points = 0
        self.points_canvas.delete(self.note_text)
        self.note_text = self.points_canvas.create_text(self.board_dimension // 2, 20,
                                                        text='New board generated, GRE word is ' + str(l) + " long",
                                                        font=("Arial", 10), fill='black')
        if self.points_text:
            self.points_canvas.delete(self.points_text)

        # Display initial points
        self.points_text = self.points_canvas.create_text(125, 50, text="", font=("Helvetica", 24), fill="blue")
        self.update_points(0)


    def new_board(self):
        self.win_text = None
        self.used_words = set()
        random_word = 'Sharon'
        while random_word == 'Sharon' or random_word in self.studied_words:
            random_word = random.choice(list(gre_words.keys()))
        self.studied_words.add(random_word)

        self.king_word = random_word.upper()
        definition = gre_words[random_word]

        self.new_points_board(len(random_word))
        self.new_definition_board(random_word, definition)

        error = True
        while error:
            try:
                self.new_letter_board(random_word)
                error = False
            except ValueError as e:
                error = True


    def reveal_word(self):
        for i in self.letters:
            self.definition_canvas.itemconfig(i, state='normal')


    def draw_grid(self):
        for i in range(self.board_size + 1):
            # Draw horizontal lines
            self.word_board_canvas.create_line(0, i * self.cell_size, self.board_dimension, i * self.cell_size,
                                               fill='black')
            # Draw vertical lines
            self.word_board_canvas.create_line(i * self.cell_size, 0, i * self.cell_size, self.board_dimension,
                                               fill='black')

    def draw_letter_board(self, word):
        self.clear_board()

        place_word_on_board(self.board, word)
        letters = "BCDFGHJKLMNPQRSTVWXYZ"
        vowels = "AEIOU"


        for i in range(self.board_size):
            for j in range(self.board_size):
                random_number = random.randint(0, 10)
                if random_number < 3:
                    letter = random.choice(vowels)
                else:
                    letter = random.choice(letters)

                if self.board[i][j] == '':
                    self.board[i][j] = letter

                x = j * self.cell_size + self.cell_size // 2
                y = i * self.cell_size + self.cell_size // 2
                self.word_board_canvas.create_text(x, y, text=self.board[i][j], font=("Arial", 24), fill='black')


    def on_click(self, event):
        self.points_canvas.delete(self.note_text)
        self.selected_letters = []
        self.word_string = ""
        self.add_letter(event.x, event.y)


    def on_drag(self, event):
        self.add_letter(event.x, event.y)


    def clear_lines(self):
        for line in self.lines:
            self.word_board_canvas.delete(line)


    def add_letter(self, x, y):
        col = x // self.cell_size
        row = y // self.cell_size

        # Ensure we stay within grid bounds
        if 0 <= row < self.board_size and 0 <= col < self.board_size:
            # Calculate the middle third boundaries
            left_bound = col * self.cell_size + self.cell_size // 3
            right_bound = col * self.cell_size + 2 * self.cell_size // 3
            top_bound = row * self.cell_size + self.cell_size // 3
            bottom_bound = row * self.cell_size + 2 * self.cell_size // 3

            # Check if the cursor is within the middle third
            if left_bound <= x <= right_bound and top_bound <= y <= bottom_bound:
                position = (row, col)
                if not self.selected_letters:
                    # Start forming the word
                    self.selected_letters.append(position)
                    self.word_string += self.board[row][col]
                elif self.is_adjacent(position):
                    # Only add letter if adjacent
                    if position not in self.selected_letters:
                        # Draw a line from the last letter to the current letter
                        last_position = self.selected_letters[-1]
                        last_x = last_position[1] * self.cell_size + self.cell_size // 2
                        last_y = last_position[0] * self.cell_size + self.cell_size // 2
                        current_x = col * self.cell_size + self.cell_size // 2
                        current_y = row * self.cell_size + self.cell_size // 2

                        if current_x > last_x:
                            new_x_1 = last_x + 20
                            new_x_2 = current_x - 20
                        elif current_x < last_x:
                            new_x_1 = last_x - 20
                            new_x_2 = current_x + 20
                        else:
                            new_x_1 = last_x
                            new_x_2 = current_x

                        if current_y > last_y:
                            new_y_1 = last_y + 20
                            new_y_2 = current_y - 20
                        elif current_y < last_y:
                            new_y_1 = last_y - 20
                            new_y_2 = current_y + 20
                        else:
                            new_y_1 = last_y
                            new_y_2 = current_y


                        line = self.word_board_canvas.create_line(new_x_1, new_y_1, new_x_2, new_y_2, fill='blue', width=5)
                        self.lines.append(line)

                        # Add the current letter to the word
                        self.selected_letters.append(position)
                        self.word_string += self.board[row][col]


    def is_adjacent(self, position):
        last_position = self.selected_letters[-1]
        row_diff = abs(last_position[0] - position[0])
        col_diff = abs(last_position[1] - position[1])
        # Check adjacency (including diagonals)
        return row_diff <= 1 and col_diff <= 1


    def update_points(self, new_points):
        # Animate points increase
        for i in range(20, 36):
            self.points_canvas.itemconfig(self.points_text, text=str(new_points), font=("Helvetica", i), fill="green")
            self.points_canvas.update()
            self.root.after(30)  # Pause for 30ms between frames

        # Reset to normal size with a different color
        self.points_canvas.itemconfig(self.points_text, font=("Helvetica", 24), fill="blue")

        # Reveal words based on canvas
        self.current_letter_index = int(self.points / 20)
        self.reveal_letters(self.current_letter_index)


    def reveal_letters(self, max_index):
        for i in range(0, max_index):
            letter = self.letters[i]
            self.definition_canvas.itemconfig(letter, state='normal')


    def add_points(self):
        points = get_total_points(self.word_string)
        self.points += points
        self.note_text = self.points_canvas.create_text(self.board_dimension // 2, 20,
                                                        text=self.word_string + ' is a word worth: ' + str(
                                                            points) + ' points!',
                                                        font=("Arial", 12), fill='green')
        self.update_points(self.points)


    def on_release(self, event):
        self.clear_lines()
        if self.word_string.upper().__eq__(self.king_word):
            self.reveal_word()
            self.win_screen()

        # Display the formed word
        if self.word_string:
            if self.word_string in self.used_words:
                self.note_text = self.points_canvas.create_text(self.board_dimension // 2, 20, text='You already tried ' + self.word_string,
                                                                font=("Arial", 12), fill='red')
            else:
                if is_word(self.word_string.lower(), self.king_word):
                    self.add_points()
                    self.used_words.add(self.word_string)
                else:
                    self.note_text = self.points_canvas.create_text(self.board_dimension // 2, 20,
                                                                    text=self.word_string + ' is not a word',
                                                                    font=("Arial", 12), fill='red')

    def shake_text(self):
        # Randomly adjust the position to simulate shaking
        if self.win_text:
            x_offset = random.randint(-5, 5)
            y_offset = random.randint(-5, 5)
            start_x, start_y = 125, 125

            colors = ['red', 'green', 'blue', 'yellow', 'purple', 'orange']

            # Update the text's position
            self.word_board_canvas.coords(self.win_text, start_x + x_offset, start_y + y_offset)

            # Change the text color randomly
            new_color = random.choice(colors)
            self.word_board_canvas.itemconfig(self.win_text, fill=new_color)

            # Continue the animation
            self.root.after(50, self.shake_text)  # Adjust the delay for faster or slower shaking


    def win_screen(self):
        start_x, start_y = 125, 125
        self.win_text = self.word_board_canvas.create_text(start_x, start_y, text="YOU WIN!", font=('Helvetica', 32, 'bold'), fill='red')
        self.shake_text()
