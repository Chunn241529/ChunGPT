import os
import sqlite3
from datetime import datetime

# Kiểm tra nếu file database tồn tại và xóa nó
db_file = "chatbot.db"
if os.path.exists(db_file):
    os.remove(db_file)
    print(f"File '{db_file}' đã được xóa.")

# Kết nối đến cơ sở dữ liệu SQLite (hoặc tạo mới nếu chưa có)
conn = sqlite3.connect(db_file)
cursor = conn.cursor()

# Tạo bảng emotions với cột emoji
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS emotions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        emotion_name TEXT NOT NULL UNIQUE,
        emoji TEXT
    )
    """
)

# Tạo bảng datasets
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS datasets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        datasets_name TEXT NOT NULL UNIQUE,
        description TEXT
    )
    """
)

# Tạo bảng settings cho việc thay đổi ảnh nền, cỡ chữ và liên kết với user
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS settings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        background_image TEXT,         -- Đường dẫn tới ảnh nền
        font_size INTEGER,             -- Cỡ chữ
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- Thời gian cập nhật
        FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
    )
    """
)

# Tạo hoặc sửa bảng users với các cột bổ sung như ảnh đại diện và các trường profile
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,                 -- Tên đầy đủ của người dùng
        username TEXT NOT NULL UNIQUE,       -- Tên đăng nhập
        email TEXT NOT NULL UNIQUE,          -- Email của người dùng
        password TEXT NOT NULL,              -- Mật khẩu (khuyến khích mã hóa trước khi lưu)
        phone TEXT,                          -- Số điện thoại
        country_code TEXT,                   -- Mã quốc gia của số điện thoại
        profile_picture TEXT,                -- Ảnh đại diện
        bio TEXT,                            -- Tiểu sử người dùng
        date_of_birth DATE,                  -- Ngày sinh
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- Thời điểm đăng ký
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP  -- Thời gian cập nhật
    )
    """
)

# Thêm cột flag vào bảng users
cursor.execute(
    """
    ALTER TABLE users
    ADD COLUMN flag BOOLEAN DEFAULT FALSE;
    """
)

# Tạo bảng group_history
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS group_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        group_name TEXT,
        user_id INTEGER,
        dataset_id INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
        FOREIGN KEY (dataset_id) REFERENCES datasets (id) ON DELETE SET NULL
    )
    """
)

# Sửa bảng conversation_history để chỉ còn khóa phụ với group_id và emotion_id
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS conversation_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        group_id INTEGER,
        emotion_id INTEGER,
        input_text TEXT NOT NULL,
        img_base64 TEXT,
        ai_response TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (group_id) REFERENCES group_history (id) ON DELETE CASCADE,
        FOREIGN KEY (emotion_id) REFERENCES emotions (id) ON DELETE SET NULL
    )
    """
)

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS topics (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        topic_name TEXT UNIQUE
    );
    """
)

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS vocabulary (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        topic_id INTEGER,
        term TEXT,
        definition TEXT,
        FOREIGN KEY (topic_id) REFERENCES topics(id) ON DELETE CASCADE
    );
    """
)

# Tạo bảng verification_codes
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS verification_codes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,                          -- Khóa phụ đến bảng users
        verification_code TEXT NOT NULL,          -- Mã xác thực
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Thời gian tạo mã xác thực
        expires_at TIMESTAMP,                     -- Thời gian hết hạn mã xác thực
        used BOOLEAN DEFAULT FALSE,               -- Trạng thái sử dụng của mã
        FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
    );
    """
)

# Lưu thay đổi và đóng kết nối
conn.commit()
conn.close()

print("Đã tạo lại db thành công!!!")
