import os
import re
import sys
import time
from openai import OpenAI
from rich.console import Console
from rich.progress import track
from helpers.formatted import *
from helpers.clean_pycache import *
from func.models import *
from func.clear_terminal import *
from func.scan_file import *


def main():
    """
    Vòng lặp chính cho tương tác với AI.
    """
    clear_terminal()
    clear_python_cache()
    scan_project()

    time.sleep(1)
    clear_terminal()

    global function_list
    selected_model = default_model
    print(f"Bạn đang sử dụng modal: {selected_model}\n")

    while True:
        user_input = input(">>>  ")
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


main()
# if __name__ == "__main__":
#     main()
