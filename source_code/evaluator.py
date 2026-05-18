class HeuristicEvaluator:
    def evaluate(self, board_matrix):
        """Duyệt toàn bộ bàn cờ để tính tổng điểm Heuristic cho trạng thái hiện tại"""
        score = 0
        size = len(board_matrix)
        # 4 hướng quét: Ngang, Dọc, Chéo xuôi, Chéo ngược
        dirs = [(0, 1), (1, 0), (1, 1), (1, -1)]
        
        for r in range(size):
            for c in range(size):
                for dr, dc in dirs:
                    window = []
                    # Tạo một "cửa sổ" gồm 4 ô liên tiếp theo hướng quét
                    for step in range(4):
                        nr, nc = r + dr*step, c + dc*step
                        if 0 <= nr < size and 0 <= nc < size:
                            window.append(board_matrix[nr][nc])
                    
                    # Nếu đủ 4 ô hợp lệ, tiến hành chấm điểm cho cửa sổ này
                    if len(window) == 4:
                        score += self._score_window(window)
        return score
        
    def _score_window(self, window):
        """Trọng số điểm cho từng kịch bản của chuỗi 4 ô (Cửa sổ luận cờ)"""
        ai = window.count(2)      # Số quân của AI trong cửa sổ
        player = window.count(1)  # Số quân của Đối thủ trong cửa sổ
        empty = window.count(0)   # Số ô trống còn lại
        
        # Nếu cửa sổ chứa quân của cả hai bên -> Bị chặn nhau, không có giá trị tạo chuỗi
        if ai > 0 and player > 0: return 0 
        
        # Đánh giá các trạng thái dựa trên mức độ nguy hiểm/lợi thế
        if ai == 4: return 100000        # AI đạt 4 quân -> Thắng tuyệt đối
        elif player == 4: return -100000  # Đối thủ đạt 4 quân -> AI thua tuyệt đối
        
        elif ai == 3 and empty == 1: return 1000   # AI có 3 quân thoáng -> Cơ hội thắng cao
        elif player == 3 and empty == 1: return -5000 # Đối thủ có 3 quân thoáng -> Cực kỳ nguy hiểm (Ưu tiên chặn)
        
        elif ai == 2 and empty == 2: return 10    # AI có 2 quân -> Tích lũy thế trận nông
        elif player == 2 and empty == 2: return -10   # Đối thủ có 2 quân -> Đề phòng nhẹ
        
        return 0