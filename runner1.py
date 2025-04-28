import tkinter as tk
from tictac import *

class TicTacToeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe - You vs AI")
        self.board = initial_state()
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.create_board()

        # Label for "AI is thinking..."
        self.thinking_label = tk.Label(self.root, text="AI is thinking...", font=("Arial", 18))
        self.thinking_label.grid(row=3, column=0, columnspan=3)
        self.thinking_label.grid_forget()  # Hide initially

        # Make the AI start first
        self.root.after(500, self.ai_move)  # Let AI take the first move after 500ms

    def create_board(self):
        for i in range(3):
            for j in range(3):
                button = tk.Button(self.root, text="", font=("Arial", 24), width=5, height=2,
                                   command=lambda row=i, col=j: self.human_move(row, col))
                button.grid(row=i, column=j)
                self.buttons[i][j] = button

    def human_move(self, i, j):
        if terminal(self.board):
            return

        if self.board[i][j] is None:
            # Human is 'O'
            self.board = result(self.board, (i, j))
            self.update_buttons()

        # After making a move and updating the buttons, THEN check if the game is over
        if terminal(self.board):
            self.show_result()
        else:
            self.root.after(500, self.ai_move)

    def ai_move(self):
        # Show "AI is thinking..." while AI is calculating
        self.thinking_label.grid(row=3, column=0, columnspan=3)

        # Force the GUI to update (to show the "thinking" label)
        self.root.update()

        if not terminal(self.board):
            move = minimax(self.board)
            if move is not None:
                self.board = result(self.board, move)
                self.update_buttons()

        # Hide the "AI is thinking..." label after AI move is made
        self.thinking_label.grid_forget()

        if terminal(self.board):
            self.show_result()

    def update_buttons(self):
        for i in range(3):
            for j in range(3):
                if self.board[i][j] is not None:
                    self.buttons[i][j].config(text=self.board[i][j])

    def show_result(self):
        win = winner(self.board)
        result_text = "It's a tie!"
        if win == X:
            result_text = "AI WINS!"
        elif win == O:
            result_text = "YOU WIN!"

        result_label = tk.Label(self.root, text=result_text, font=("Arial", 18))
        result_label.grid(row=4, column=0, columnspan=3)

if __name__ == "__main__":
    root = tk.Tk()
    app = TicTacToeGUI(root)
    root.mainloop()
