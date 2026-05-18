class CaroBoard:
    def __init__(self, size=9):
        """Khởi tạo bàn cờ vuông kích thước 9x9)"""
        self.size = size
        # 0: Ô trống, 1: Người chơi 1 (X), 2: Người chơi 2 (AI)
        self.board = [[0 for _ in range(size)] for _ in range(size)]
        
    def get_valid_moves(self):
        """Tìm danh sách các nước đi hợp lệ nhằm tối ưu hóa không gian tìm kiếm cho AI"""
        moves = []
        has_piece = False
        
        # Kiểm tra xem bàn cờ đã có quân nào được hạ xuống chưa
        for r in range(self.size):
            for c in range(self.size):
                if self.board[r][c] != 0:
                    has_piece = True
                    break
            if has_piece: break
            
        # Nếu bàn cờ trống hoàn toàn, gợi ý đi ngay ô chính giữa để chiếm lợi thế
        if not has_piece:
            return [(self.size // 2, self.size // 2)]
            
        # Chỉ lấy các ô trống có ít nhất 1 quân cờ khác nằm xung quanh (bán kính 1 ô)
        for r in range(self.size):
            for c in range(self.size):
                if self.board[r][c] == 0:
                    adjacent = False
                    # Duyệt 8 ô xung quanh ô (r, c)
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dr == 0 and dc == 0: continue
                            nr, nc = r + dr, c + dc
                            # Nếu phát hiện ô lân cận có quân, đánh dấu hợp lệ
                            if 0 <= nr < self.size and 0 <= nc < self.size and self.board[nr][nc] != 0:
                                adjacent = True
                                break
                        if adjacent: break
                    if adjacent:
                        moves.append((r, c))
        return moves

    def make_move(self, r, c, player):
        """Đặt quân của người chơi vào ô (r, c) nếu ô đó còn trống"""
        if self.board[r][c] == 0:
            self.board[r][c] = player
            return True
        return False

    def undo_move(self, r, c):
        """Hủy nước đi tại ô (r, c) phục vụ cho thuật toán quay lui (Backtracking)"""
        self.board[r][c] = 0

    def check_winner(self):
        """Kiểm tra điều kiện thắng/thua/hòa trên bàn cờ"""
        # 4 hướng cần kiểm tra: Ngang, Dọc, Chéo xuôi, Chéo ngược
        dirs = [(0, 1), (1, 0), (1, 1), (1, -1)]
        
        for r in range(self.size):
            for c in range(self.size):
                player = self.board[r][c]
                if player == 0: continue
                
                # Quét theo các hướng để tìm chuỗi liên tiếp
                for dr, dc in dirs:
                    count = 1
                    # Kiểm tra 3 ô tiếp theo theo hướng đang quét
                    for step in range(1, 4):
                        nr, nc = r + dr * step, c + dc * step
                        if 0 <= nr < self.size and 0 <= nc < self.size and self.board[nr][nc] == player:
                            count += 1
                        else: break
                    # Đạt đủ 4 quân liên tiếp theo logic hiện tại -> Trả về người thắng
                    if count >= 4: return player
                    
        # Kiểm tra trạng thái hòa (Bàn cờ đã đầy nhưng không ai thắng)
        is_full = True
        for row in self.board:
            if 0 in row:
                is_full = False
                break
        if is_full: return -1 # -1 nghĩa là Hòa
        
        return 0 # 0 nghĩa là Trận đấu vẫn đang tiếp tục