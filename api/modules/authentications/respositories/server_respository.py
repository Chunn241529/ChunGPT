import os
import sqlite3
from datetime import datetime


class Repository_server:
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

    ### USERS TABLE METHODS ###
    def get_user_by_id(self, user_id):
        """Lấy thông tin người dùng theo user_id."""
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
            result = cursor.fetchone()
            return result  # Trả về thông báo nếu không có người dùng nào

    def get_user_by_username(self, username):
        """Lấy thông tin người dùng theo user_id."""
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
            result = cursor.fetchone()
            return result  # Trả về thông báo nếu không có người dùng nào

    ### USERS TABLE METHODS ###
    def get_client_by_id(self, user_id):
        """Lấy thông tin người dùng theo user_id."""
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT database_client FROM users WHERE id = ?", (user_id,))
            result = cursor.fetchone()
            if result:
                return result[
                    0
                ]  # Trả về giá trị đầu tiên trong tuple  # Hoặc bạn có thể tùy chỉnh theo cách bạn muốn

            return "User not found in (get_client_by_id)"  # Trả về thông báo nếu không có người dùng nào

    def insert_user(
        self,
        name,
        username,
        email,
        password,
        phone=None,
        country_code=None,
        profile_picture=None,
        bio=None,
        date_of_birth=None,
        database_client=None,
    ):
        """Thêm người dùng mới với kiểm tra trùng lặp."""
        if not database_client:
            database_client = "__" + username + "__" + ".sqlite3"

        with self._connect() as conn:
            cursor = conn.cursor()

            # Kiểm tra xem email hoặc username đã tồn tại chưa
            cursor.execute(
                "SELECT 1 FROM users WHERE email = ? OR username = ?", (email, username)
            )
            if cursor.fetchone():
                raise ValueError("Email hoặc tên đăng nhập đã tồn tại.")

            try:
                # Thêm người dùng mới
                cursor.execute(
                    """
                    INSERT INTO users (name, username, email, password, phone, country_code, profile_picture, bio, date_of_birth, database_client, created_at, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        name,
                        username,
                        email,
                        password,
                        phone,
                        country_code,
                        profile_picture,
                        bio,
                        date_of_birth,
                        database_client,
                        datetime.now(),
                        datetime.now(),
                    ),
                )
                conn.commit()
                return cursor.lastrowid
            except sqlite3.IntegrityError as e:
                raise ValueError(f"Lỗi ràng buộc UNIQUE: {e}")

    def update_user(
        self,
        user_id,
        name=None,
        username=None,
        email=None,
        password=None,
        phone=None,
        country_code=None,
        profile_picture=None,
        bio=None,
        date_of_birth=None,
    ):
        """Cập nhật thông tin người dùng."""
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE users
                SET name = ?, username = ?, email = ?, password = ?, phone = ?, country_code = ?, profile_picture = ?, bio = ?, date_of_birth = ?, updated_at = ?
                WHERE id = ?
            """,
                (
                    name,
                    username,
                    email,
                    password,
                    phone,
                    country_code,
                    profile_picture,
                    bio,
                    date_of_birth,
                    datetime.now(),
                    user_id,
                ),
            )
            conn.commit()
            return cursor.rowcount

    def delete_user(self, user_id):
        """Xóa người dùng theo user_id."""
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
            conn.commit()
            return cursor.rowcount

    ### SETTINGS TABLE METHODS ###
    def get_settings_by_user(self, user_id):
        """Lấy cài đặt của người dùng theo user_id."""
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM settings WHERE user_id = ?", (user_id,))
            result = cursor.fetchone()
            if result:
                return result[
                    0
                ]  # Trả về giá trị đầu tiên trong tuple  # Hoặc bạn có thể tùy chỉnh theo cách bạn muốn

            return "error in get_settings_by_user"  # Trả về thông báo nếu không có người dùng nào

    def insert_settings(self, user_id, background_image, font_size):
        """Thêm cài đặt cho người dùng."""
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO settings (user_id, background_image, font_size, updated_at)
                VALUES (?, ?, ?, ?)
            """,
                (user_id, background_image, font_size, datetime.now()),
            )
            conn.commit()
            return cursor.lastrowid

    def update_settings(self, user_id, background_image=None, font_size=None):
        """Cập nhật cài đặt của người dùng."""
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE settings
                SET background_image = ?, font_size = ?, updated_at = ?
                WHERE user_id = ?
            """,
                (background_image, font_size, datetime.now(), user_id),
            )
            conn.commit()
            return cursor.rowcount

    ### VERIFICATION CODES METHODS ###
    def get_verification_code(self, user_id):
        """Lấy mã xác thực của người dùng theo user_id."""
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM verification_codes WHERE user_id = ?", (user_id,)
            )
            result = cursor.fetchone()
            if result:
                return result[
                    0
                ]  # Trả về giá trị đầu tiên trong tuple  # Hoặc bạn có thể tùy chỉnh theo cách bạn muốn

            return "error in (get_verification_code)"  # Trả về thông báo nếu không có người dùng nào

    def insert_verification_code(self, user_id, verification_code, expires_at):
        """Thêm mã xác thực cho người dùng."""
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO verification_codes (user_id, verification_code, expires_at, created_at)
                VALUES (?, ?, ?, ?)
            """,
                (user_id, verification_code, expires_at, datetime.now()),
            )
            conn.commit()
            return cursor.lastrowid

    def update_verification_code(self, user_id, verification_code, expires_at):
        """Cập nhật mã xác thực cho người dùng."""
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE verification_codes
                SET verification_code = ?, expires_at = ?, created_at = ?
                WHERE user_id = ?
            """,
                (verification_code, expires_at, datetime.now(), user_id),
            )
            conn.commit()
            return cursor.rowcount

    def delete_verification_code(self, user_id):
        """Xóa mã xác thực của người dùng."""
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM verification_codes WHERE user_id = ?", (user_id,)
            )
            conn.commit()
            return cursor.rowcount
