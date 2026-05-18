import math

class CaroAI:
    def __init__(self, evaluator):
        """
        Khởi tạo AI cho bàn cờ Caro.
        :param evaluator: Đối tượng chịu trách nhiệm đánh giá điểm số của một trạng thái bàn cờ (Heuristic Function)
        """
        self.evaluator = evaluator
        self.states_evaluated = 0  # Biến đếm tổng số trạng thái bàn cờ mà AI đã duyệt qua và đánh giá
        
    def minimax(self, board_obj, depth, is_maximizing):
        """
        Thuật toán Minimax cơ bản (Tìm kiếm vét cạn cây quyết định)
        :param board_obj: Đối tượng bàn cờ hiện tại
        :param depth: Độ sâu tìm kiếm còn lại
        :param is_maximizing: True nếu là lượt của AI (tìm nước đi có điểm tối đa), False nếu là lượt của Người chơi
        :return: (best_score, best_move) - Điểm số tốt nhất và tọa độ nước đi tối ưu (row, col)
        """
        # 1. KIỂM TRA TRẠNG THÁI KẾT THÚC (Điều kiện dừng của đệ quy)
        winner = board_obj.check_winner()
        if winner == 2: return 100000, None   # AI thắng -> Trả về điểm cực lớn
        if winner == 1: return -100000, None  # Người chơi thắng -> Trả về điểm cực nhỏ
        if winner == -1: return 0, None       # Hòa cờ -> Trả về điểm 0
        
        # Nếu đạt đến giới hạn độ sâu tìm kiếm, sử dụng hàm Heuristic để ước lượng điểm số
        if depth == 0:
            self.states_evaluated += 1  # Tăng số lượng trạng thái đã đánh giá
            return self.evaluator.evaluate(board_obj.board), None
            
        best_move = None
        valid_moves = board_obj.get_valid_moves() # Lấy danh sách các ô trống có thể đi
        
        # 2. NHÁNH MAXIMIZING (Lượt của AI)
        if is_maximizing:
            max_eval = -math.inf # Khởi tạo điểm tối đa ban đầu là âm vô cùng
            for r, c in valid_moves:
                board_obj.make_move(r, c, 2)  # Giả định AI đánh vào ô (r, c)
                
                # Gọi đệ quy cho lượt tiếp theo 
                eval_val, _ = self.minimax(board_obj, depth - 1, False)
                
                board_obj.undo_move(r, c)     # Thu hồi nước đi thử nghiệm để trả lại trạng thái bàn cờ
                
                # Cập nhật nước đi tốt nhất nếu tìm thấy nước có điểm cao hơn
                if eval_val > max_eval:
                    max_eval = eval_val
                    best_move = (r, c)
            return max_eval, best_move
            
        # 3. NHÁNH MINIMIZING 
        else:
            min_eval = math.inf # Khởi tạo điểm tối thiểu ban đầu là dương vô cùng
            for r, c in valid_moves:
                board_obj.make_move(r, c, 1)  # Giả định đối thủ đánh vào ô (r, c)
                
                # Gọi đệ quy cho lượt tiếp theo (chuyển sang lượt Maximizing của AI)
                eval_val, _ = self.minimax(board_obj, depth - 1, True)
                
                board_obj.undo_move(r, c)     # Thu hồi nước đi thử nghiệm
                
                # Cập nhật nước đi tốt nhất cho đối thủ (nước đi gây bất lợi nhất cho AI)
                if eval_val < min_eval:
                    min_eval = eval_val
                    best_move = (r, c)
            return min_eval, best_move

    def alphabeta(self, board_obj, depth, alpha, beta, is_maximizing):
        """
        Thuật toán Minimax kết hợp cắt tỉa Alpha-Beta (Alpha-Beta Pruning)
        Giúp loại bỏ các nhánh không cần thiết để tăng tốc độ tìm kiếm một cách đáng kể
        :param alpha: Điểm số tối thiểu mà người chơi Maximizing (AI) chắc chắn đạt được
        :param beta: Điểm số tối đa mà người chơi Minimizing (Người chơi) chắc chắn giữ được
        """
        # 1. KIỂM TRA TRẠNG THÁI KẾT THÚC
        winner = board_obj.check_winner()
        if winner == 2: return 100000, None
        if winner == 1: return -100000, None
        if winner == -1: return 0, None
        
        if depth == 0:
            self.states_evaluated += 1
            return self.evaluator.evaluate(board_obj.board), None
            
        best_move = None
        valid_moves = board_obj.get_valid_moves()
        
        # 2. NHÁNH MAXIMIZING (AI) CÓ CẮT TỈA
        if is_maximizing:
            max_eval = -math.inf
            for r, c in valid_moves:
                board_obj.make_move(r, c, 2)
                eval_val, _ = self.alphabeta(board_obj, depth - 1, alpha, beta, False)
                board_obj.undo_move(r, c)
                
                if eval_val > max_eval:
                    max_eval = eval_val
                    best_move = (r, c)
                    
                # Cập nhật giá trị alpha (giá trị tốt nhất mà AI có thể chọn cho đến nay)
                alpha = max(alpha, eval_val)
                
                # CẮT TỈA: Nếu điểm này lớn hơn hoặc bằng beta (điểm tối đa Người chơi chấp nhận ở nhánh trên),
                # thì Người chơi ở nhánh trên sẽ không bao giờ cho phép AI đi vào nhánh này -> Dừng duyệt các ô tiếp theo.
                if beta <= alpha: 
                    break 
            return max_eval, best_move
            
        # 3. NHÁNH MINIMIZING (NGƯỜI CHƠI) CÓ CẮT TỈA
        else:
            min_eval = math.inf
            for r, c in valid_moves:
                board_obj.make_move(r, c, 1)
                eval_val, _ = self.alphabeta(board_obj, depth - 1, alpha, beta, True)
                board_obj.undo_move(r, c)
                
                if eval_val < min_eval:
                    min_eval = eval_val
                    best_move = (r, c)
                    
                # Cập nhật giá trị beta (giá trị thấp nhất mà đối thủ có thể ép AI phải nhận)
                beta = min(beta, eval_val)
                
                # CẮT TỈA: Nếu beta nhỏ hơn hoặc bằng alpha (điểm tối thiểu AI chắc chắn có được ở nhánh khác),
                # thì AI ở nhánh trên sẽ không bao giờ chọn nhánh này -> Dừng duyệt các ô tiếp theo.
                if beta <= alpha: 
                    break 
            return min_eval, best_move