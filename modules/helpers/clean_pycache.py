import os
import shutil
from rich.progress import track


def clear_python_cache():
    files_to_delete = []  # Danh sách lưu trữ các mục cần xóa

    # Tìm tất cả các thư mục __pycache__ và file .pyc
    for root, dirs, files in os.walk(".", topdown=False):
        for name in dirs:
            if name == "__pycache__":
                files_to_delete.append(
                    os.path.join(root, name)
                )  # Thêm thư mục __pycache__ vào danh sách
        for name in files:
            if name.endswith(".pyc"):
                files_to_delete.append(
                    os.path.join(root, name)
                )  # Thêm file .pyc vào danh sách

    # Dùng track để theo dõi tiến độ xóa các mục trong danh sách
    for item in track(files_to_delete, description="Clearing Python Cache..."):
        if os.path.isdir(item):
            shutil.rmtree(item)  # Xóa thư mục
        elif os.path.isfile(item):
            os.remove(item)  # Xóa file
