import os
import sys


def clear_terminal():
    """
    Xóa màn hình terminal trước khi chạy chương trình.
    """
    if sys.platform == "win32":  # Windows
        os.system("cls")
    else:
        os.system("clear")
