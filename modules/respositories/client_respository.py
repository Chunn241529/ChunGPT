import os
import sqlite3
from datetime import datetime


class Repository_client:
    def __init__(self, db_path):
        """Khởi tạo repository với đường dẫn đến cơ sở dữ liệu SQLite."""
        if not os.path.exists(db_path):
            raise FileNotFoundError(
                f"Database file '{db_path}' does not exist."
            )  # Ném lỗi nếu file không tồn tại
        self.db_path = db_path

    def _connect(self):
        """Kết nối đến cơ sở dữ liệu."""
        return sqlite3.connect(self.db_path)

    # =============================== TABLE: brain_ai ===============================

    def insert_brain_ai(self, custom_ai):
        """Thêm một bản ghi vào bảng brain_ai."""
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO brain_ai (custom_ai, updated_at)
                VALUES (?, ?)
                """,
                (custom_ai, datetime.now()),
            )
            conn.commit()

    def get_brain_ai(self):
        """Lấy tất cả bản ghi từ bảng brain_ai."""
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM brain_ai")
            return cursor.fetchall()

    # =============================== TABLE: brain_history_scan_project ===============================

    def insert_brain_history_scan(self, filepath, func):
        """Thêm một bản ghi vào bảng brain_history_scan_project."""
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO brain_history_scan_project (filepath, func, updated_at)
                VALUES (?, ?, ?)
                """,
                (filepath, func, datetime.now()),
            )
            conn.commit()

    def get_brain_history_scan(self):
        """Lấy tất cả bản ghi từ bảng brain_history_scan_project."""
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM brain_history_scan_project")
            return cursor.fetchall()

    def get_brain_history_scan_by_filepath(self, filepath):
        """Lấy tất cả bản ghi từ bảng brain_history_scan_project theo filepath."""
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM brain_history_scan_project WHERE filepath = ?",
                (filepath,),
            )
            return cursor.fetchall()

    # =============================== TABLE: brain_history_chat ===============================

    def insert_brain_history_chat(self, role, content):
        """Thêm một bản ghi vào bảng brain_history_chat."""
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO brain_history_chat (role, content, updated_at)
                VALUES (?, ?, ?)
                """,
                (role, content, datetime.now()),
            )
            conn.commit()

    def get_brain_history_chat(self):
        """Lấy tất cả bản ghi từ bảng brain_history_chat."""
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM brain_history_chat")
            return cursor.fetchall()

    def get_brain_history_chat_by_role(self, role):
        """Lấy tất cả bản ghi từ bảng brain_history_chat theo role."""
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM brain_history_chat WHERE role = ?",
                (role,),
            )
            return cursor.fetchall()

    # =============================== UPDATE AND DELETE ===============================

    def update_brain_history_scan(self, scan_id, filepath, func):
        """Cập nhật thông tin trong bảng brain_history_scan_project."""
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE brain_history_scan_project
                SET filepath = ?, func = ?, updated_at = ?
                WHERE id = ?
                """,
                (filepath, func, datetime.now(), scan_id),
            )
            conn.commit()

    def delete_brain_history_scan(self, scan_id):
        """Xóa bản ghi từ bảng brain_history_scan_project."""
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM brain_history_scan_project WHERE id = ?", (scan_id,)
            )
            conn.commit()

    def delete_brain_history_chat(self, chat_id):
        """Xóa bản ghi từ bảng brain_history_chat."""
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM brain_history_chat WHERE id = ?", (chat_id,))
            conn.commit()
