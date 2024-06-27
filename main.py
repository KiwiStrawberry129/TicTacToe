# main.py

import numpy as np
import random
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout

# Constants
ROW_COUNT = 3
COLUMN_COUNT = 3
PLAYER = 0
AI = 1
EMPTY = 0
PLAYER_PIECE = 1
AI_PIECE = 2
WINDOW_LENGTH = 3

# Colors
RED = [1, 0, 0, 1]
YELLOW = [1, 1, 0, 1]

# Tic Tac Toe Game Logic
class TicTacToeGame:
    def __init__(self):
        self.board = np.zeros((ROW_COUNT, COLUMN_COUNT))  # 3x3 board, 0 represents empty, 1 for X, 2 for O
        self.current_player = PLAYER_PIECE  # Player 1 starts with X

    def reset(self):
        self.board = np.zeros((ROW_COUNT, COLUMN_COUNT))
        self.current_player = PLAYER_PIECE

    def make_move(self, row, col):
        if self.board[row][col] == EMPTY:  # If the position is empty
            self.board[row][col] = self.current_player
            return True
        return False

    def check_winner(self):
        # Check rows and columns
        for i in range(ROW_COUNT):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] != EMPTY:  # Check rows
                return self.board[i][0]
            if self.board[0][i] == self.board[1][i] == self.board[2][i] != EMPTY:  # Check columns
                return self.board[0][i]

        # Check diagonals
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != EMPTY:  # Top-left to bottom-right diagonal
            return self.board[0][0]
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != EMPTY:  # Top-right to bottom-left diagonal
            return self.board[0][2]

        # Check for tie
        if np.all(self.board != EMPTY):
            return -1  # Tie

        return 0  # No winner yet

    def switch_player(self):
        self.current_player = AI_PIECE if self.current_player == PLAYER_PIECE else PLAYER_PIECE


# Kivy GUI Implementation
class TicTacToeApp(App):
    def build(self):
        self.game = TicTacToeGame()
        self.board_buttons = [[None for _ in range(COLUMN_COUNT)] for _ in range(ROW_COUNT)]

        layout = GridLayout(cols=3)

        for row in range(ROW_COUNT):
            for col in range(COLUMN_COUNT):
                button = Button(font_size=40, size_hint=(0.33, 0.33))
                button.bind(on_press=self.on_button_click)
                layout.add_widget(button)
                self.board_buttons[row][col] = button

        reset_button = Button(text='Reset Game', size_hint=(1, 0.1))
        reset_button.bind(on_press=self.reset_game)
        layout.add_widget(reset_button)

        self.status_label = Label(text="Player X's turn", size_hint=(1, 0.1))
        layout.add_widget(self.status_label)

        return layout

    def on_button_click(self, instance):
        row, col = self.get_button_position(instance)
        if self.game.make_move(row, col):
            instance.text = 'X' if self.game.current_player == PLAYER_PIECE else 'O'
            instance.disabled = True
            winner = self.game.check_winner()
            if winner == PLAYER_PIECE:
                self.show_popup("Player X wins!")
            elif winner == AI_PIECE:
                self.show_popup("Player O wins!")
            elif winner == -1:
                self.show_popup("It's a tie!")
            else:
                self.game.switch_player()
                self.status_label.text = f"Player {'X' if self.game.current_player == PLAYER_PIECE else 'O'}'s turn"

    def reset_game(self, instance):
        self.game.reset()
        for row in range(ROW_COUNT):
            for col in range(COLUMN_COUNT):
                self.board_buttons[row][col].text = ''
                self.board_buttons[row][col].disabled = False
        self.status_label.text = "Player X's turn"

    def show_popup(self, message):
        popup = Popup(title='Game Over', content=Label(text=message), size_hint=(0.5, 0.5))
        popup.open()

    def get_button_position(self, button):
        for row in range(ROW_COUNT):
            for col in range(COLUMN_COUNT):
                if self.board_buttons[row][col] == button:
                    return row, col
        return -1, -1

if __name__ == '__main__':
    TicTacToeApp().run()
