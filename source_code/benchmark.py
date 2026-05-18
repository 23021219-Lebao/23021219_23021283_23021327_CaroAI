import tkinter as tk
from tkinter import messagebox
import time
import math
import copy

from board import CaroBoard
from evaluator import HeuristicEvaluator
from ai import CaroAI

# --- Định nghĩa các thế cờ mẫu để kiểm thử thuật toán 
STATES = {
    "1. Đầu ván": [
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0, 0],# Trạng thái khởi đầu ván cờ
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0]
    ],
    "2. Máy có thể thắng ngay": [
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0, 0],# Trạng thái máy có thể thắng ngay
        [0, 0, 2, 2, 2, 0, 0, 0, 0], 
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0]
    ],
    "3. Máy cần chặn.": [
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 2, 1, 1, 1, 0, 0, 0], 
        [0, 0, 0, 0, 0, 0, 0, 0, 0],# Trạng thái người chơi sắp thắng, máy buộc phải chặn
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0]
    ],
    "4. Hai bên tấn công": [
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],# Trạng thái hai bên đều có cơ hội tấn công
        [0, 0, 0, 0, 2, 2, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0]
    ],
    "5. Bẫy tầm nhìn": [
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 2, 2, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 1, 0, 0, 0],# Bẫy tầm nhìn
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]
}

class CaroGUI:
    def __init__(self, root):
        """Khởi tạo giao diện game tích hợp bảng chọn thế cờ thử nghiệm"""
        self.root = root
        self.root.title("Cờ Caro - Benchmark Tool")
        self.size = 9
        
        self.board = CaroBoard(self.size)
        self.evaluator = HeuristicEvaluator()
        self.ai = CaroAI(self.evaluator)
        self.game_over = False

        # --- Cấu hình thuật toán & độ sâu ---
        control_frame = tk.Frame(root)
        control_frame.pack(pady=5)
        
        self.algo_var = tk.StringVar(value="alphabeta")
        tk.Radiobutton(control_frame, text="Minimax", variable=self.algo_var, value="minimax").grid(row=0, column=0, padx=5)
        tk.Radiobutton(control_frame, text="Alpha-Beta", variable=self.algo_var, value="alphabeta").grid(row=0, column=1, padx=5)
        
        tk.Label(control_frame, text="Độ sâu:").grid(row=0, column=2)
        self.depth_var = tk.IntVar(value=3)
        tk.Spinbox(control_frame, from_=1, to=5, textvariable=self.depth_var, width=3).grid(row=0, column=3, padx=5)
        
        tk.Button(control_frame, text="Làm mới bàn cờ", command=self.reset_game).grid(row=0, column=4, padx=10)

        # --- Khung chức năng Benchmark ---
        benchmark_frame = tk.Frame(root, bd=1, relief="solid")
        benchmark_frame.pack(pady=5, ipadx=5, ipady=5)
        
        tk.Label(benchmark_frame, text="Thực nghiệm:").grid(row=0, column=0, padx=5)
        self.state_var = tk.StringVar(value=list(STATES.keys())[0])
        tk.OptionMenu(benchmark_frame, self.state_var, *STATES.keys()).grid(row=0, column=1, padx=5)
        
        tk.Button(benchmark_frame, text="Tải Thế Cờ", command=self.load_benchmark, bg="lightblue").grid(row=0, column=2, padx=5)
        tk.Button(benchmark_frame, text="AI Đánh Ngay", command=self.force_ai_turn, bg="lightgreen", font=('Arial', 9, 'bold')).grid(row=0, column=3, padx=5)

        # --- Khởi tạo lưới nút bấm bàn cờ ---
        self.grid_frame = tk.Frame(root)
        self.grid_frame.pack(pady=5)
        self.buttons = [[None for _ in range(self.size)] for _ in range(self.size)]
        
        for r in range(self.size):
            for c in range(self.size):
                btn = tk.Button(self.grid_frame, text="", font=('Helvetica', 16, 'bold'), width=3, height=1,
                                command=lambda row=r, col=c: self.player_click(row, col))
                btn.grid(row=r, column=c, padx=1, pady=1)
                self.buttons[r][c] = btn
                
        self.stats_label = tk.Label(root, text="Sẵn sàng! Mời bạn (X) đi trước hoặc Tải Benchmark.", font=('Arial', 11), fg="blue")
        self.stats_label.pack(pady=10)

    def load_benchmark(self):
        """Sao chép sâu (deep copy) thế cờ mẫu được chọn vào ma trận bàn cờ hiện tại"""
        state_name = self.state_var.get()
        self.board.board = copy.deepcopy(STATES[state_name])
        self.game_over = False
        self.update_ui()
        self.stats_label.config(text=f"Đã tải {state_name}. Hãy chọn AI và bấm 'AI Đánh Ngay'.", fg="blue")

    def update_ui(self):
        """Đồng bộ trạng thái từ ma trận board.board lên giao diện nút bấm"""
        for r in range(self.size):
            for c in range(self.size):
                val = self.board.board[r][c]
                if val == 1:
                    self.buttons[r][c].config(text="X", fg="blue", state="disabled")
                elif val == 2:
                    self.buttons[r][c].config(text="O", fg="red", state="disabled")
                else:
                    self.buttons[r][c].config(text="", state="normal")

    def player_click(self, r, c):
        """Xử lý nước đi của người chơi khi bấm trực tiếp lên bàn cờ"""
        if self.game_over or self.board.board[r][c] != 0:
            return
            
        self.board.make_move(r, c, 1)
        self.update_ui()
        
        winner = self.board.check_winner()
        if winner != 0:
            self.handle_game_over(winner)
            return

        self.force_ai_turn()

    def force_ai_turn(self):
        """Ép AI tính toán nước đi ngay lập tức (phục vụ nút bấm ép lượt hoặc sau khi người chơi đi)"""
        if self.game_over:
            return
            
        self.stats_label.config(text="Máy (O) đang suy nghĩ...", fg="orange")
        self.root.update()
        self.root.after(100, self.ai_turn)

    def ai_turn(self):
        """Chạy thuật toán tìm kiếm (Minimax/Alpha-Beta) và đo lường thông số hiệu năng"""
        depth = self.depth_var.get()
        use_ab = (self.algo_var.get() == "alphabeta")
        
        self.ai.states_evaluated = 0
        start_time = time.time()
        
        if use_ab:
            eval_score, best_move = self.ai.alphabeta(self.board, depth, -math.inf, math.inf, True)
        else:
            eval_score, best_move = self.ai.minimax(self.board, depth, True)
            
        elapsed_time = time.time() - start_time
        
        if best_move:
            self.board.make_move(best_move[0], best_move[1], 2)
            self.update_ui()
            
            # Xuất kết quả đo lường: số trạng thái đã duyệt và thời gian thực thi
            stats_text = (f"AI đánh: {best_move} | Đánh giá: {eval_score} \n"
                          f"Trạng thái đã xét: {self.ai.states_evaluated} | Thời gian: {elapsed_time:.4f}s")
            self.stats_label.config(text=stats_text, fg="black")
            
            winner = self.board.check_winner()
            if winner != 0:
                self.handle_game_over(winner)
        else:
            self.stats_label.config(text="Lỗi: AI không tìm được nước đi (Hòa hoặc kín bàn)!")

    def handle_game_over(self, winner):
        """Dừng trò chơi và thông báo kết quả chung cuộc"""
        self.game_over = True
        if winner == 1:
            msg = "Chúc mừng! Bạn (X) đã thắng!"
        elif winner == 2:
            msg = "Máy (O) đã thắng!"
        else:
            msg = "Bàn cờ đầy! Hòa!"
            
        self.stats_label.config(text=msg, fg="green" if winner == 1 else "red")
        messagebox.showinfo("Kết thúc", msg)

    def reset_game(self):
        """Khởi tạo lại ma trận bàn cờ mới trống hoàn toàn"""
        self.board = CaroBoard(self.size)
        self.game_over = False
        self.stats_label.config(text="Đã làm mới! Mời bạn (X) đi trước.", fg="blue")
        self.update_ui()

if __name__ == "__main__":
    root = tk.Tk()
    app = CaroGUI(root)
    root.mainloop()