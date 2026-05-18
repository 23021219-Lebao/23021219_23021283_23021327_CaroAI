# Đồ án: Trí tuệ nhân tạo cho trò chơi Caro (Caro AI)

Dự án phát triển ứng dụng trò chơi Cờ Caro đối kháng trực tiếp (Người vs Máy), tích hợp Trí tuệ nhân tạo dựa trên thuật toán tìm kiếm quyết định Minimax và cơ chế cắt tỉa Alpha-Beta Pruning. 

## 1. Thành viên nhóm thực hiện
    [Lê Quốc Bảo] - [23021219]
    [Phạm Việt Hưng] - [23021283]
    [Trần Duy Phúc] - [23021327]

## 2. Thông số kỹ thuật & Quy tắc trò chơi
- **Kích thước bàn cờ:** Hệ thống vận hành trên không gian ma trận $9 \times 9$.
- **Luật chiến thắng:** Áp dụng luật cờ Caro 4 quân tiêu chuẩn. Người chơi (X) hoặc Máy (O) giành chiến thắng ngay khi thiết lập được chuỗi **tối thiểu 4 quân liên tiếp** (ngang, dọc, chéo). Không xét điều kiện chặn hai đầu.
- **Môi trường & Công nghệ:** - Ngôn ngữ lập trình: **Python 3.8+**.
  - Không yêu cầu cài đặt thư viện bên ngoài. Hệ thống sử dụng hoàn toàn các thư viện chuẩn (Standard Libraries) của Python bao gồm: `tkinter` (xây dựng GUI), `time`, `math`, `copy`.

## 3. Cấu trúc mã nguồn (Repository Structure)
Mã nguồn được tổ chức theo mô hình phân lớp tại thư mục `source_code/`, trong đó `main.py` là chương trình lõi:

```text
mssv1_mssv2_mssv3_CaroAI/
├── source_code/
│   ├── main.py          # [CHƯƠNG TRÌNH CHÍNH] Giao diện trò chơi Caro tương tác trực tiếp
│   ├── benchmark.py     # [CÔNG CỤ PHỤ TRỢ] Bộ công cụ đo lường và kiểm thử trạng thái tĩnh
│   ├── board.py         # Quản lý cấu trúc bàn cờ và luật chơi
│   ├── ai.py            # Cài đặt lõi thuật toán Minimax và Alpha-Beta
│   └── evaluator.py     # Hàm đánh giá (Heuristic) trạng thái bàn cờ
├── requirements.txt     # Khai báo môi trường
└── README.md            # Tài liệu hướng dẫn sử dụng
