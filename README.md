# Đồ án: Trí tuệ nhân tạo cho trò chơi Caro (Caro AI)

Dự án phát triển ứng dụng trò chơi Cờ Caro đối kháng trực tiếp (Người vs Máy), tích hợp Trí tuệ nhân tạo dựa trên thuật toán tìm kiếm quyết định Minimax và cơ chế cắt tỉa Alpha-Beta Pruning. 

## 1. Thành viên nhóm thực hiện
    Lê Quốc Bảo      - 23021219
    Phạm Việt Hưng   - 23021283
    Trần Duy Phúc    - 23021327

## 2. Thông số kỹ thuật & Quy tắc trò chơi
- **Kích thước bàn cờ:** $9 \times 9$.
- **Luật chơi:** Áp dụng luật cờ Caro 4 quân tiêu chuẩn. Người chơi (X) hoặc Máy (O) giành chiến thắng ngay khi thiết lập được chuỗi tối thiểu 4 quân liên tiếp (ngang, dọc, chéo). Không xét luật chặn hai đầu. Nếu bàn cờ đầy và không có người thắng thì kết quả là hòa.
- **Môi trường & Công nghệ:** - Ngôn ngữ lập trình: **Python 3.8+**.
  - Không yêu cầu cài đặt thư viện bên ngoài. Hệ thống sử dụng hoàn toàn các thư viện chuẩn (Standard Libraries) của Python bao gồm: `tkinter`, `time`, `math`, `copy`.

## 3. Cấu trúc mã nguồn (Repository Structure)
Mã nguồn được tổ chức theo mô hình phân lớp tại thư mục `source_code/`, trong đó `main.py` là chương trình lõi:

```text
mssv1_mssv2_mssv3_CaroAI/
├── source_code/
│   ├── main.py          # [CHƯƠNG TRÌNH CHÍNH] Giao diện trò chơi Caro tương tác trực tiếp
│   ├── benchmark.py     # [CÔNG CỤ PHỤ TRỢ] Bộ công cụ đo lường và kiểm thử trạng thái tĩnh
│   ├── board.py         # Quản lý cấu trúc bàn cờ và luật chơi
│   ├── ai.py            # Cài đặt thuật toán Minimax và Alpha-Beta
│   └── evaluator.py     # Hàm đánh giá trạng thái bàn cờ
├── requirements.txt     # Khai báo môi trường
└── README.md            # Tài liệu hướng dẫn sử dụng
```

## 4. Hướng dẫn vận hành chương trình

Mở ứng dụng dòng lệnh (Terminal/Command Prompt), di chuyển vào thư mục mã nguồn: `cd source_code`. Hệ thống cung cấp 2 tính năng như sau:

### 4.1. Chức năng chính: Chơi cờ tương tác (Khởi chạy `main.py`)
Đây là module chính, cho phép người dùng chơi cờ trực tiếp với AI trên giao diện đồ họa.
- **Lệnh khởi chạy:**
  ```bash
  python main.py
  ```
- **Hướng dẫn sử dụng:**
  - Trên thanh điều khiển, lựa chọn thuật toán AI (`Minimax` nguyên bản hoặc `Alpha-Beta`).
  - Tùy chỉnh độ khó của AI thông qua tham số `Độ sâu (Depth = 1 đến 5)`.
  - Người chơi (X) luôn đi trước. Nhấp chuột vào các ô trống trên lưới để hạ quân. Khối AI (O) sẽ tự động tính toán và phản hồi nước đi kế tiếp.
  - Hệ thống tự động nhận diện chuỗi 4 quân và thông báo kết quả thắng/thua.

### 4.2. Chức năng phụ trợ: Công cụ Benchmark (Khởi chạy `benchmark.py`)
Đây là công cụ kiểm thử được nhóm phát triển thêm nhằm phục vụ việc thu thập số liệu định lượng cho Báo cáo đồ án. Công cụ này nạp cứng các thế cờ tĩnh để đo lường giới hạn của thuật toán.
- **Lệnh khởi chạy:**
  ```bash
  python benchmark.py
  ```
- **Hướng dẫn sử dụng:**
  - Lựa chọn 1 trong 5 trạng thái thế cờ tiêu chuẩn để nạp lên bàn cờ.
  - Thiết lập thuật toán và độ sâu muốn đo lường.
  - Nhấn nút **"AI Đánh Ngay"**. Hệ thống sẽ xuất ra các chỉ số bao gồm: *Tọa độ*, *Tổng số trạng thái đã xét* và *Thời gian thực thi*.

---
*Lưu ý: Trên một số hệ điều hành, lệnh `python` có thể cần thay thế bằng `python3`.*
