import tkinter as tk

from game_logic import BLACK, EMPTY, WHITE, OthelloGame


CELL_SIZE = 60
BOARD_SIZE = CELL_SIZE * 8

class OthelloGUI:
    def __init__(self, root):
        self.root = root
        self.root.title('オセロゲーム')
        self.game = OthelloGame()

        self.canvas = tk.Canvas(root, width=BOARD_SIZE, height=BOARD_SIZE, bg='darkgreen')
        self.canvas.pack()
        self.canvas.bind('<Button-1>', self.handle_click)

        self.status_label = tk.Label(self.root, text="黒の番です", font=("Arial", 14))
        self.status_label.pack()

        self.count_label = tk.Label(self.root, text="黒: 2 白: 2", font=("Arial", 12))
        self.count_label.pack()

        self.restart_button = tk.Button(self.root, text="もう一度遊ぶ", font=("Arial", 12),command=self.restart_game, state="disabled")
        self.restart_button.pack(pady=5)

        self.animating = False
        self.draw_board()

    def restart_game(self):
        self.game = OthelloGame()
        self.restart_button.config(state="disabled")
        self.canvas.bind("<Button-1>", self.handle_click)
        self.status_label.config(text="黒の番です")
        self.count_label.config(text="黒: 2 白: 2")
        self.draw_board()

    def draw_board(self):
        self.canvas.delete('all')

        for y in range(8):
            for x in range(8):
                self.canvas.create_rectangle(
                    x * CELL_SIZE, y * CELL_SIZE, 
                    (x + 1) * CELL_SIZE, (y + 1) * CELL_SIZE, 
                    outline='black', width=2
                )

                stone = self.game.board[y][x]
                if stone != EMPTY:
                    self.draw_stone(x, y, stone)
        
        for x, y in self.game.get_valid_moves(self.game.current_player):
            cx = x * CELL_SIZE + CELL_SIZE // 2
            cy = y * CELL_SIZE + CELL_SIZE // 2
            r = 6
            self.canvas.create_oval(cx - r, cy - r, cx + r, cy + r, fill='yellow', outline='')

        self.status_label.config(
            text=('黒' if self.game.current_player == BLACK else '白') + 'の番です'
        )
        black, white = self.game.count_pieces()
        self.count_label.config(text=f"黒: {black} 白: {white}")

    def draw_stone(self, x, y, color, scale=1.0):
        cx = x * CELL_SIZE + CELL_SIZE // 2
        cy = y * CELL_SIZE + CELL_SIZE // 2
        r = int((CELL_SIZE // 2 - 4) * scale)
        fill_color = 'black' if color == BLACK else 'white'
        self.canvas.create_oval(cx - r, cy - r, cx + r, cy + r, fill=fill_color, outline='gray')

    def animate_flip(self, x, y, from_color, to_color, step=0):
        total_steps = 12
        if step < 6:
            scale = 1.0 - step * 0.15
            self.draw_board()
            self.draw_stone(x, y, from_color, scale)
            self.root.after(30, lambda: self.animate_flip(x, y, from_color, to_color, step + 1))
        elif step == 6:
            self.draw_board()
            self.draw_stone(x, y, to_color, 0.1)
            self.root.after(30, lambda: self.animate_flip(x, y, from_color, to_color, step + 1))
        elif step <= total_steps:
            scale = (step - 6) * 0.15 + 0.1
            self.draw_board()
            self.draw_stone(x, y, to_color, scale)
            self.root.after(30, lambda: self.animate_flip(x, y, from_color, to_color, step + 1))
        else:
            self.animating = False
            self.draw_board()
            self.check_pass_or_end()

    def animate_flips(self, positions, player):
        if not positions:
            self.animating = False
            self.draw_board()
            self.check_pass_or_end()
            return

        fx, fy = positions[0]
        opponent = WHITE if player == BLACK else BLACK
        self.animate_flip(fx, fy, opponent, player)
        self.root.after(250, lambda: self.animate_flips(positions[1:], player))

    def handle_click(self, event):
        if self.animating:
            return
        x = event.x // CELL_SIZE
        y = event.y // CELL_SIZE
        player = self.game.current_player

        if (x, y) not in self.game.get_valid_moves(player):
            return

        flip_positions = self.game.apply_move_with_tracking(x, y, player)
        self.game.current_player = WHITE if player == BLACK else BLACK

        if flip_positions:
            self.animating = True
            self.animate_flips(flip_positions, player)
        else:
            self.check_pass_or_end()

    #----------------------------------------
    # 勝敗・パス処理
    #----------------------------------------
    def check_pass_or_end(self):
        current = self.game.current_player
        valid = self.game.get_valid_moves(current)
        other = BLACK if current == WHITE else WHITE
        other_valid = self.game.get_valid_moves(other)

        if not valid and not other_valid:
            self.show_result()
            return

        if not valid and other_valid:
            self.status_label.config(
                text=('黒' if self.game.current_player == BLACK else '白') + 'はパスです！'
            )
            self.game.current_player = other
            self.root.after(1000, self.draw_board)
            return

        self.draw_board()

    #----------------------------------------
    # 勝敗結果表示
    #----------------------------------------
    def show_result(self):
        black, white = self.game.count_pieces()
        if black > white:
            result = "黒の勝ち！"
        elif white > black:
            result = "白の勝ち！"
        else:
            result = "引き分け"

        self.status_label.config(text=f"{result}　黒: {black}　白: {white}")
        self.canvas.unbind("<Button-1>")

        # ✅ リスタートボタンを有効化
        self.restart_button.config(state="normal")

if __name__ == '__main__':
    root = tk.Tk()
    app = OthelloGUI(root)
    root.mainloop()
