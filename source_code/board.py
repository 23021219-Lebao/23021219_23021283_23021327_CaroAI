class CaroBoard:
    def __init__(self, size=9):
        self.size = size
        self.board = [[0 for _ in range(size)] for _ in range(size)]
        
    def get_valid_moves(self):
        moves = []
        has_piece = False
        for r in range(self.size):
            for c in range(self.size):
                if self.board[r][c] != 0:
                    has_piece = True
                    break
            if has_piece: break
            
        if not has_piece:
            return [(self.size // 2, self.size // 2)]
            
        for r in range(self.size):
            for c in range(self.size):
                if self.board[r][c] == 0:
                    adjacent = False
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dr == 0 and dc == 0: continue
                            nr, nc = r + dr, c + dc
                            if 0 <= nr < self.size and 0 <= nc < self.size and self.board[nr][nc] != 0:
                                adjacent = True
                                break
                        if adjacent: break
                    if adjacent:
                        moves.append((r, c))
        return moves

    def make_move(self, r, c, player):
        if self.board[r][c] == 0:
            self.board[r][c] = player
            return True
        return False

    def undo_move(self, r, c):
        self.board[r][c] = 0

    def check_winner(self):
        dirs = [(0, 1), (1, 0), (1, 1), (1, -1)]
        for r in range(self.size):
            for c in range(self.size):
                player = self.board[r][c]
                if player == 0: continue
                for dr, dc in dirs:
                    count = 1
                    for step in range(1, 4):
                        nr, nc = r + dr * step, c + dc * step
                        if 0 <= nr < self.size and 0 <= nc < self.size and self.board[nr][nc] == player:
                            count += 1
                        else: break
                    if count >= 4: return player
        is_full = True
        for row in self.board:
            if 0 in row:
                is_full = False
                break
        if is_full: return -1
        return 0