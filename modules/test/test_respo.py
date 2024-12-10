# main.py
import os
import sys
import sqlite3

# Thêm thư mục gốc của dự án vào sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Import lớp Repository từ module chứa nó
from respositories.server_respository import Repository_server
from respositories.client_respository import Repository_client

# Thêm thư mục gốc của dự án vào sys.path

# from helpers.database_client import create_database_client


def test_get_user_by_id():
    """Test phương thức get_user_by_id."""
    # Đường dẫn đến cơ sở dữ liệu của bạn
    db_path = "chatbot_v2.sqlite3"

    # Khởi tạo đối tượng Repository
    repo = Repository_server(db_path)

    # ID người dùng cần tìm
    user_id = 1  # Ví dụ user_id

    # Gọi phương thức get_user_by_id
    database = repo.get_client_by_id(user_id)
    # print(database)
    return database


def test():
    """Test phương thức get_user_by_id."""
    # Đường dẫn đến cơ sở dữ liệu của bạn
    db_path = test_get_user_by_id()
    # Khởi tạo đối tượng Repository
    repo = Repository_client(db_path)

    repo.insert_brain_ai("hello world!")


# Gọi hàm test
test()
