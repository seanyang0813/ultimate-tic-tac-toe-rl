import tkinter as tk
import random
from game import Game, Player
from agent_play import RandomAgent
from tianshou_play import RLAgent

rl_agent = RLAgent()
random_agent = RandomAgent()

class UltimateTicTacToeApp:
    def __init__(self, master):
        self.master = master
        master.title("Ultimate Tic-Tac-Toe")
        self.player_choice = tk.IntVar()  # 0 for Black, 1 for White, 2 for Random
        self.human_player = Player.X
        self.opponent_choice = tk.StringVar(value="RL")
        self.init_agent_selection_ui()
        self.agent = random_agent

    def init_agent_selection_ui(self):
        self.cleanup_ui()
        self.label = tk.Label(self.master, text="Choose your side:", font=("Arial", 16))
        self.label.pack(pady=20)

        # Radio buttons for player choice
        tk.Radiobutton(self.master, text="X", variable=self.player_choice, value=0, font=("Arial", 12)).pack(anchor=tk.W)
        tk.Radiobutton(self.master, text="O", variable=self.player_choice, value=1, font=("Arial", 12)).pack(anchor=tk.W)
        tk.Radiobutton(self.master, text="Random", variable=self.player_choice, value=2, font=("Arial", 12)).pack(anchor=tk.W)

        self.label_opponent = tk.Label(self.master, text="Choose your opponent:", font=("Arial", 16))
        self.label_opponent.pack(pady=20)

        # Radio buttons for opponent choice
        tk.Radiobutton(self.master, text="RL Agent", variable=self.opponent_choice, value="RL", font=("Arial", 12)).pack(anchor=tk.W)
        tk.Radiobutton(self.master, text="Random Agent", variable=self.opponent_choice, value="Random", font=("Arial", 12)).pack(anchor=tk.W)

        # Button to confirm selection and start the game
        self.start_button = tk.Button(self.master, text="Start Game", command=self.setup_game)
        self.start_button.pack(pady=20)


    def setup_game(self):
        self.cleanup_ui()
        self.game = Game()
        player_selection = self.player_choice.get()
        self.human_player = Player.X if player_selection == 0 else Player.O
        if (player_selection == 2):
            self.human_player = random.choice([Player.X, Player.O])
        opponent_selection = self.opponent_choice.get()
        if (opponent_selection == "Random"):
            self.agent = random_agent
        else:
            self.agent = rl_agent
        self.is_gamerover = False
        self.winner = None
        
        # Display who starts the game and the opponent type
        starting_player_label = tk.Label(self.master, text="You are playing " + ("X" if self.human_player==Player.X else "O"), font=("Arial", 16))
        starting_player_label.pack(pady=10)
        opponent_type_label = tk.Label(self.master, text=f"Opponent: {opponent_selection} Agent", font=("Arial", 16))
        opponent_type_label.pack(pady=10)
        if (self.human_player != self.game.to_move):
            self.agent.play_move(self.game)
        
        self.init_game_ui()
        self.render_board()

    def init_game_ui(self):
        cell_size = 50
        normal_line_width = 1
        bold_line_width = 3
        grid_size = 9

        # Adjusted canvas size considering bold lines
        canvas_size = cell_size * grid_size + bold_line_width * 4 + normal_line_width * (grid_size - 1 - 4)
        self.canvas = tk.Canvas(self.master, width=canvas_size, height=canvas_size)
        self.canvas.pack()

        # Draw the grid lines with bold lines for subgrids
        for i in range(1, grid_size):
            line_width = bold_line_width if i % 3 == 0 else normal_line_width
            position = i * cell_size + (i - 1) * normal_line_width + (bold_line_width if i > 3 else 0) + (bold_line_width if i > 6 else 0)
            self.canvas.create_line(position, 0, position, canvas_size, width=line_width)
            self.canvas.create_line(0, position, canvas_size, position, width=line_width)

        self.buttons = [[None for _ in range(grid_size)] for _ in range(grid_size)]
        for i in range(grid_size):
            for j in range(grid_size):
                x1 = j * cell_size + j * normal_line_width + (bold_line_width if j >= 3 else 0) + (bold_line_width if j >= 6 else 0)
                y1 = i * cell_size + i * normal_line_width + (bold_line_width if i >= 3 else 0) + (bold_line_width if i >= 6 else 0)
                button = tk.Button(self.master, text='', font=("Arial", 20, "bold"), height=1, width=2, bg="white",
                                   command=lambda i=i, j=j: self.on_button_click(i, j))
                # Adjust the button size to fill the cell, considering line widths
                button_width = cell_size - 2  # Adjust button width to fit the cell
                button_height = cell_size - 2  # Adjust button height to fit the cell
                self.canvas.create_window((x1 + button_width / 2), (y1 + button_height / 2), window=button, anchor="center", width=button_width, height=button_height)
                self.buttons[i][j] = button

        self.reset_button = tk.Button(self.master, text="Reset Game", command=self.init_agent_selection_ui)
        self.reset_button.pack(pady=20)

    def on_button_click(self, y, x):
        # opponent probably thinking
        if (self.game.to_move != self.human_player):
            return
        if (self.is_gamerover):
            return
        if self.game.is_move_allowed(x, y):
            self.game.make_move(x, y)
            winner = self.game.is_game_over_and_winner()
            if (winner[0] == True):
                self.is_gamerover = True
                winner_text = "You won the game" if winner[1] == self.human_player else "You lost the game"
                if (winner[1] == Player.EMPTY):
                    winner_text = "You drew the game"
                game_end_label = tk.Label(self.master, text=f"{winner_text}", font=("Arial", 16))
                game_end_label.pack(pady=10)
                self.render_board()
                return
            self.agent.play_move(self.game)
            self.render_board()
            winner = self.game.is_game_over_and_winner()
            if (winner[0] == True):
                self.is_gamerover = True
                winner_text = "You won the game" if winner[1] == self.human_player else "You lost the game"
                if (winner[1] == Player.EMPTY):
                    winner_text = "You drew the game"
                game_end_label = tk.Label(self.master, text=f"{winner_text}", font=("Arial", 16))
                game_end_label.pack(pady=10)
                self.render_board()
                return

    def render_board(self):
        # loop through the board and update the button text
        print(self.human_player)
        for i in range(9):
            for j in range(9):
                # reset button background
                self.buttons[i][j].config(bg="white")
                if self.game.board[i][j] == self.human_player:
                    self.buttons[i][j].config(text=("X" if self.human_player==Player.X else "O"))
                elif self.game.board[i][j] == Player.EMPTY:
                    continue
                else:
                    self.buttons[i][j].config(text="O" if self.human_player==Player.X else "X")
        if (self.is_gamerover):
            print("game is over")
            self.game.print_board()
        

        # look through all valid moves and mark the buttons lightblue
        valid_moves = self.game.get_all_valid_moves()
        for move in valid_moves:
            self.buttons[move[1]][move[0]].config(bg="lightblue")

        # look through won mini grids and draw big X over the 3 x 3 buttons
        for i in range(3):
            for j in range(3):
                if self.game.min_grid_win_info[i][j] != None:
                    # paint the 3x3 grid green for self red for opponent
                    winner_color = "green"
                    if self.game.min_grid_win_info[i][j] == self.human_player:
                        winner_color = "green"
                    elif self.game.min_grid_win_info[i][j] == Player.EMPTY:
                        winner_color = "yellow"
                    else:
                        winner_color = "red"
                    for mini_x in range(3):
                        for mini_y in range(3):
                            self.buttons[i * 3 + mini_x][j * 3 + mini_y].config(bg=winner_color)


                

    def cleanup_ui(self):
        for widget in self.master.winfo_children():
            widget.destroy()

root = tk.Tk()
app = UltimateTicTacToeApp(root)
root.mainloop()
