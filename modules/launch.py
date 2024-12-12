import re
import time
from helpers.formatted import *
from helpers.clean_pycache import *
from func.models import *
from func.clear_terminal import *
from func.scan_file import *

from respositories.client_respository import Repository_client

repo = Repository_client("client_db_1.sqlite3")


def check():
    scan = repo.get_brain_history_scan()

    if not scan:  # Kiểm tra nếu bảng trống
        clear_terminal()
        clear_python_cache()
        scan_project()
        clear_terminal()
    else:
        clear_terminal()
        clear_python_cache()
        clear_terminal()


def start():
    """
    Vòng lặp chính cho tương tác với AI.
    """
    check()
    global function_list
    selected_model = default_model
    print(f"Bạn đang sử dụng modal: {selected_model}\n")

    while True:
        user_input = input("\033[1;36m>>>   \033[0m")
        if user_input.lower() == "thoát":
            print("Đã thoát chương trình.")
            break

        if user_input.lower() == ".ls":
            selected_model = select_model()
            continue

        # Kiểm tra nếu user_input chứa @<tên_hàm>
        match = re.search(r".func<(\w+)>", user_input)
        if match:
            function_name = match.group(1)  # Lấy tên hàm trong <>
            prompt = user_input.replace(f".func<{function_name}>", "").strip()
            display_function_code(function_name, prompt)
            continue

        match = re.search(
            r".file<([\w\.\-]+)>", user_input
        )  # Cập nhật regex để bắt cả phần mở rộng file
        if match:
            file_name = match.group(1)  # Lấy tên file bao gồm phần mở rộng
            prompt = user_input.replace(f".file<{file_name}>", "").strip()
            display_file(file_name, prompt)
            continue

        send_to_ai(None, None, user_input, selected_model)


start()
