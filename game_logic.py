EMPTY = 0
BLACK = 1
WHITE = 2

DIRECTIONS = [
    (-1, -1), (-1, 0), (-1, 1),
    (0, -1),         (0, 1), 
    (1, -1), (1, 0), (1, 1)
]

class OthelloGame:
    def __init__(self):
        self.board = [[EMPTY for _ in range(8)] for _ in range(8)]
        self.current_player = BLACK # Start for BLACK
        self.init_board()

    def init_board(self):
        # initial
        self.board[3][3] = WHITE
        self.board[3][4] = BLACK
        self.board[4][3] = BLACK
        self.board[4][4] = WHITE

    def is_valid_move(self, x, y, player):
        if self.board[y][x] != EMPTY:
            return False

        opponent = BLACK if player == WHITE else WHITE
        for dx, dy in DIRECTIONS:
            nx, ny = x + dx, y + dy
            has_opponent = False
            while 0 <= nx < 8 and 0 <= ny < 8:
                if self.board[ny][nx] == opponent:
                    has_opponent = True
                elif self.board[ny][nx] == player:
                    if has_opponent:
                        return True
                    break
                else:
                    break
                nx += dx
                ny += dy
        return False

    def get_valid_moves(self, player):
        return [(x, y) for y in range(8) for x in range(8) if self.is_valid_move(x, y, player)]

    # def apply_move(self, x, y, player):
    #     if not self.is_valid_move(x, y, player):
    #         return
    #     self.board[y][x] = player
    #     opponent = BLACK if player == WHITE else WHITE
    #     for dx, dy in DIRECTIONS:
    #         nx, ny = x + dx, y + dy
    #         stones_to_flip = []
    #         while 0 <= nx < 8 and 0 <= ny < 8 and self.board[ny][nx] == opponent:
    #             stones_to_flip.append((nx, ny))
    #             nx += dx
    #             ny += dy

    #         if 0 <= nx < 8 and 0 <= ny < 8 and self.board[ny][nx] == player:
    #             for fx, fy in stones_to_flip:
    #                 self.board[fy][fx] = player # turn over

    def apply_move_with_tracking(self, x, y, player):
        if not self.is_valid_move(x, y, player):
            return []

        self.board[y][x] = player
        opponent = BLACK if player == WHITE else WHITE
        flipped = []

        for dx, dy in DIRECTIONS:
            nx, ny = x + dx, y + dy
            stones_to_flip = []
            while 0 <= nx < 8 and 0 <= ny < 8 and self.board[ny][nx] == opponent:
                stones_to_flip.append((nx, ny))
                nx += dx
                ny += dy

            if 0 <= nx < 8 and 0 <= ny < 8 and self.board[ny][nx] == player:
                for fx, fy in stones_to_flip:
                    self.board[fy][fx] = player # turn over
                    flipped.append((fx, fy))
        return flipped

    def count_pieces(self):
        black_count = sum(row.count(BLACK) for row in self.board)
        white_count = sum(row.count(WHITE) for row in self.board)
        return black_count, white_count

    def is_game_over(self):
        return not self.get_valid_moves(BLACK) and not self.get_valid_moves(WHITE)
