import tkinter as tk
from tkinter import messagebox
import time
import math

from board import CaroBoard
from evaluator import HeuristicEvaluator
from ai import CaroAI

class CaroGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Cờ Caro")
        self.size = 9
    
        self.board = CaroBoard(self.size)
        self.evaluator = HeuristicEvaluator()
        self.ai = CaroAI(self.evaluator)
        
        self.game_over = False

        control_frame = tk.Frame(root)
        control_frame.pack(pady=10)
        
        self.algo_var = tk.StringVar(value="alphabeta")
        tk.Radiobutton(control_frame, text="Minimax", variable=self.algo_var, value="minimax").grid(row=0, column=0, padx=10)
        tk.Radiobutton(control_frame, text="Alpha-Beta", variable=self.algo_var, value="alphabeta").grid(row=0, column=1, padx=10)
        
        tk.Label(control_frame, text="Độ sâu (Depth):").grid(row=0, column=2)
        self.depth_var = tk.IntVar(value=3)
        tk.Spinbox(control_frame, from_=1, to=5, textvariable=self.depth_var, width=5).grid(row=0, column=3, padx=5)
        
        tk.Button(control_frame, text="Chơi Lại", command=self.reset_game, bg="lightgray").grid(row=0, column=4, padx=10)

        self.grid_frame = tk.Frame(root)
        self.grid_frame.pack()
        self.buttons = [[None for _ in range(self.size)] for _ in range(self.size)]
        
        for r in range(self.size):
            for c in range(self.size):
                btn = tk.Button(self.grid_frame, text="", font=('Helvetica', 16, 'bold'), width=3, height=1,
                                command=lambda row=r, col=c: self.player_click(row, col))
                btn.grid(row=r, column=c, padx=1, pady=1)
                self.buttons[r][c] = btn

        self.stats_label = tk.Label(root, text="Sẵn sàng! Mời bạn (X) đi trước.", font=('Arial', 11), fg="blue")
        self.stats_label.pack(pady=10)

    def update_ui(self):
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
        if self.game_over or self.board.board[r][c] != 0:
            return
            
        self.board.make_move(r, c, 1)
        self.update_ui()
        
        winner = self.board.check_winner()
        if winner != 0:
            self.handle_game_over(winner)
            return

        self.stats_label.config(text="Máy (O) đang suy nghĩ...", fg="orange")
        self.root.update()
        
        self.root.after(100, self.ai_turn)

    def ai_turn(self):
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
            
            stats_text = (f"AI đánh: {best_move} | Đánh giá: {eval_score} \n"
                          f"Trạng thái đã xét: {self.ai.states_evaluated} | Thời gian: {elapsed_time:.4f}s")
            self.stats_label.config(text=stats_text, fg="black")
            
            winner = self.board.check_winner()
            if winner != 0:
                self.handle_game_over(winner)
        else:
            self.stats_label.config(text="Lỗi: AI không tìm được nước đi!")

    def handle_game_over(self, winner):
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
        self.board = CaroBoard(self.size)
        self.game_over = False
        self.stats_label.config(text="Đã làm mới! Mời bạn (X) đi trước.", fg="blue")
        self.update_ui()

if __name__ == "__main__":
    root = tk.Tk()
    app = CaroGUI(root)
    root.mainloop()