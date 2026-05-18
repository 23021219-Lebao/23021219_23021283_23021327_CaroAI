import math

class CaroAI:
    def __init__(self, evaluator):
        self.evaluator = evaluator
        self.states_evaluated = 0 
        
    def minimax(self, board_obj, depth, is_maximizing):
        winner = board_obj.check_winner()
        if winner == 2: return 100000, None
        if winner == 1: return -100000, None
        if winner == -1: return 0, None
        
        if depth == 0:
            self.states_evaluated += 1
            return self.evaluator.evaluate(board_obj.board), None
            
        best_move = None
        valid_moves = board_obj.get_valid_moves()
        
        if is_maximizing:
            max_eval = -math.inf
            for r, c in valid_moves:
                board_obj.make_move(r, c, 2)
                eval_val, _ = self.minimax(board_obj, depth - 1, False)
                board_obj.undo_move(r, c)
                if eval_val > max_eval:
                    max_eval = eval_val
                    best_move = (r, c)
            return max_eval, best_move
        else:
            min_eval = math.inf
            for r, c in valid_moves:
                board_obj.make_move(r, c, 1)
                eval_val, _ = self.minimax(board_obj, depth - 1, True)
                board_obj.undo_move(r, c)
                if eval_val < min_eval:
                    min_eval = eval_val
                    best_move = (r, c)
            return min_eval, best_move

    def alphabeta(self, board_obj, depth, alpha, beta, is_maximizing):
        winner = board_obj.check_winner()
        if winner == 2: return 100000, None
        if winner == 1: return -100000, None
        if winner == -1: return 0, None
        
        if depth == 0:
            self.states_evaluated += 1
            return self.evaluator.evaluate(board_obj.board), None
            
        best_move = None
        valid_moves = board_obj.get_valid_moves()
        
        if is_maximizing:
            max_eval = -math.inf
            for r, c in valid_moves:
                board_obj.make_move(r, c, 2)
                eval_val, _ = self.alphabeta(board_obj, depth - 1, alpha, beta, False)
                board_obj.undo_move(r, c)
                if eval_val > max_eval:
                    max_eval = eval_val
                    best_move = (r, c)
                alpha = max(alpha, eval_val)
                if beta <= alpha: break
            return max_eval, best_move
        else:
            min_eval = math.inf
            for r, c in valid_moves:
                board_obj.make_move(r, c, 1)
                eval_val, _ = self.alphabeta(board_obj, depth - 1, alpha, beta, True)
                board_obj.undo_move(r, c)
                if eval_val < min_eval:
                    min_eval = eval_val
                    best_move = (r, c)
                beta = min(beta, eval_val)
                if beta <= alpha: break
            return min_eval, best_move