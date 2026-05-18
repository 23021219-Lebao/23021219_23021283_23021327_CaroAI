class HeuristicEvaluator:
    def evaluate(self, board_matrix):
        score = 0
        size = len(board_matrix)
        dirs = [(0, 1), (1, 0), (1, 1), (1, -1)]
        for r in range(size):
            for c in range(size):
                for dr, dc in dirs:
                    window = []
                    for step in range(4):
                        nr, nc = r + dr*step, c + dc*step
                        if 0 <= nr < size and 0 <= nc < size:
                            window.append(board_matrix[nr][nc])
                    if len(window) == 4:
                        score += self._score_window(window)
        return score
        
    def _score_window(self, window):
        ai = window.count(2)
        player = window.count(1)
        empty = window.count(0)
        
        if ai > 0 and player > 0: return 0 
        
        if ai == 4: return 100000
        elif player == 4: return -100000
        elif ai == 3 and empty == 1: return 1000
        elif player == 3 and empty == 1: return -5000
        elif ai == 2 and empty == 2: return 10
        elif player == 2 and empty == 2: return -10
        
        return 0