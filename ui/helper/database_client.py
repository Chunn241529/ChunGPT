import os
import sqlite3


def create_database_client(db_name):
    # Kiểm tra nếu file database tồn tại và xóa nó
    db_file = db_name
    if os.path.exists(db_file):
        os.remove(db_file)
        print(f"File '{db_file}' đã được xóa.")

    # Kết nối đến cơ sở dữ liệu SQLite (hoặc tạo mới nếu chưa có)
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Tạo bảng brain_ai
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS brain_ai (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            custom_ai TEXT,             
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    # Tạo bảng brain_history_chat
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS brain_history_chat (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role TEXT,         
            content TEXT,      
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    # Tạo bảng brain_history_scan_project
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS brain_history_scan_project (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filepath TEXT,        
            func TEXT,          
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP  
        )
        """
    )

    # Lưu thay đổi và đóng kết nối
    conn.commit()
    conn.close()

    print("Tạo thành công!!!")


create_database_client("client_db_1.sqlite3")
