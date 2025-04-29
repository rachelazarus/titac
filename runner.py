import tkinter as tk
from tictac import *

class TicTacToeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🎉 Tic Tac Toe - You vs AI 🎉")
        self.root.configure(bg="#f0f0f0")  # Light background for minimalism

        self.board = initial_state()

        # Role attributes
        self.human_player = None
        self.ai_player = None

        # Control frame for start options and restart
        self.control_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.control_frame.pack(pady=10)

        # Start option: who begins
        self.start_var = tk.StringVar(value="player")
        tk.Label(self.control_frame, text="Who starts?", font=("Comic Sans MS", 14), bg="#f0f0f0").pack(side="left", padx=5)
        tk.Radiobutton(self.control_frame, text="You", variable=self.start_var, value="player", font=("Comic Sans MS", 12), bg="#f0f0f0").pack(side="left")
        tk.Radiobutton(self.control_frame, text="AI", variable=self.start_var, value="ai", font=("Comic Sans MS", 12), bg="#f0f0f0").pack(side="left")
        self.start_button = tk.Button(self.control_frame, text="Start Game", font=("Comic Sans MS", 14, "bold"), command=self.start_game, bg="#90ee90")
        self.start_button.pack(side="left", padx=10)

        # Restart button
        self.restart_button = tk.Button(
            self.control_frame, text="🔄 Restart", font=("Comic Sans MS", 14, "bold"),
            command=self.restart_game, bg="#ffd700"
        )
        self.restart_button.pack(side="left", padx=10)

        # Game board frame
        self.board_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.board_frame.pack(pady=20)

        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.create_board()

        # Label for "AI is thinking..."
        self.thinking_label = tk.Label(self.root, text="🤖 AI is thinking...", font=("Arial", 18), bg="#f0f0f0")
        self.thinking_label.pack_forget()

        # Game state
        self.game_active = False

    def create_board(self):
        for i in range(3):
            for j in range(3):
                btn = tk.Button(
                    self.board_frame, text="", font=("Comic Sans MS", 24, "bold"),
                    width=6, height=3,
                    bg="#ffffff", fg="#444",
                    relief="flat",
                    command=lambda row=i, col=j: self.human_move(row, col)
                )
                btn.grid(row=i, column=j, padx=5, pady=5)
                # Hover effect
                btn.bind("<Enter>", lambda e, b=btn: b.config(bg="#e0e0e0"))
                btn.bind("<Leave>", lambda e, b=btn: b.config(bg="#ffffff"))
                self.buttons[i][j] = btn

    def start_game(self):
        self.restart_game()
        self.game_active = True
        # Assign roles based on who starts
        if self.start_var.get() == "ai":
            self.human_player = O
            self.ai_player = X
            # AI starts
            self.root.after(500, self.ai_move)
        else:
            self.human_player = X
            self.ai_player = O

    def human_move(self, i, j):
        if not self.game_active or terminal(self.board):
            return

        if self.board[i][j] is None:
            # Human is 'O' or 'X' based on role
            self.board = result(self.board, (i, j))
            self.update_buttons()

            if terminal(self.board):
                self.show_result()
            else:
                self.root.after(500, self.ai_move)

    def ai_move(self):
        if not self.game_active or terminal(self.board):
            return

        # Show "AI is thinking..."
        self.thinking_label.pack(pady=10)
        self.root.update()

        move = minimax(self.board)
        if move is not None:
            self.board = result(self.board, move)
            self.update_buttons()

        self.thinking_label.pack_forget()

        if terminal(self.board):
            self.show_result()

    def update_buttons(self):
        for i in range(3):
            for j in range(3):
                val = self.board[i][j]
                if val is not None:
                    self.buttons[i][j].config(text=val, fg="#222")
                else:
                    self.buttons[i][j].config(text="", fg="#444")

    def show_result(self):
        win = winner(self.board)
        # Determine who is human and who is AI
        human_wins = (win == self.human_player)
        ai_wins = (win == self.ai_player)

        if human_wins:
            result_text = "🎉 You Win! 🎉"
        elif ai_wins:
            result_text = "🤖 AI Wins! 🤖"
        else:
            result_text = "🤝 It's a Tie! 🤝"

        result_label = tk.Label(self.root, text=result_text, font=("Comic Sans MS", 16, "bold"), bg="#f0f0f0")
        result_label.pack(pady=10)
        self.game_active = False

    def restart_game(self):
        self.board = initial_state()
        self.update_buttons()
        # Remove result labels
        for widget in self.root.pack_slaves():
            if isinstance(widget, tk.Label) and widget != self.thinking_label:
                widget.destroy()
        self.game_active = False

if __name__ == "__main__":
    root = tk.Tk()
    app = TicTacToeGUI(root)
    root.mainloop()
