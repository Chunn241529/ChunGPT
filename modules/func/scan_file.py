import os
import re
from rich.progress import track

from helpers.formatted import *
from helpers.clean_pycache import *
from func.models import *
from func.clear_terminal import *
from func.chat import *

# respository
from respositories.client_respository import Repository_client

repository_client = Repository_client("client_db_1.sqlite3")

repository_client = Repository_client("client_db_1.sqlite3")
function_list = []  # Đặt function_list là biến toàn cục


def scan_project(directory="."):
    """
    Duyệt qua toàn bộ project để tìm các hàm trong file Python, JavaScript, và CSS.
    """
    global function_list
    function_list = []  # Reset function list

    # Thu thập danh sách các tệp cần quét
    file_paths = []
    for root, _, files in os.walk(directory):
        if ".venv" in root:
            continue  # Bỏ qua thư mục .venv
        for file in files:
            if file.endswith((".py", ".js", ".css")):
                file_paths.append(os.path.join(root, file))

    # Hiển thị tiến trình xử lý danh sách file
    for filepath in track(file_paths, description="Đang quét dự án..."):
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
            functions = extract_functions(content, filepath)

            # Ghi các hàm vào database và cập nhật danh sách function_list
            for func in functions:
                func_str = (
                    ", ".join(map(str, func)) if isinstance(func, tuple) else str(func)
                )
                repository_client.insert_brain_history_scan(filepath, func_str)
            list_db = repository_client.get_brain_history_scan()
            function_list.extend(
                [
                    (filepath_in_db, func_in_db)
                    for _, filepath_in_db, func_in_db, _ in list_db
                ]
            )


def extract_functions(content, file_type):
    """
    Tìm các hàm trong nội dung file dựa trên loại file.
    """
    if file_type.endswith(".py"):
        return [
            (match[0], match[1])
            for match in re.findall(r"(?:(def|class)\s+([a-zA-Z_]\w*))", content)
        ]
    elif file_type.endswith(".js"):
        return [
            (match[0], match[1])
            for match in re.findall(r"(?:(function|class)\s+([a-zA-Z_]\w*))", content)
        ]
    elif file_type.endswith(".css"):
        return [
            ("css", match) for match in re.findall(r"([.#][a-zA-Z_][\w-]*)", content)
        ]
    return []


def display_function_code(function_name, prompt):
    """
    Tìm và hiển thị code của hàm dựa trên tên được cung cấp.
    Sau đó gửi nội dung code và prompt tới AI để phân tích.
    """
    for filepath, func_in_db in function_list:
        type_, name = func_in_db.split(", ")
        if name == function_name:  # Tìm đúng hàm
            try:
                # Đọc file gốc để lấy nội dung đầy đủ của hàm
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()

                # Xác định pattern regex dựa trên loại (def/class/function)
                if type_ == "def":  # Python function
                    pattern = rf"(^\s*def {function_name}\(.*?\):[\s\S]*?(?=^\s*def |\s*class |\Z))"
                elif type_ == "class":  # Python class
                    pattern = (
                        rf"(^\s*class {function_name}\(.*?\):[\s\S]*?(?=^\s*class |\Z))"
                    )
                else:  # JavaScript or CSS case
                    pattern = rf"{function_name}\s*?[{{(][\s\S]*?[}})]"

                # Thực hiện tìm kiếm với re.MULTILINE để hỗ trợ pattern trên nhiều dòng
                match = re.search(pattern, content, re.MULTILINE)
                if match:
                    function_code = match.group(0)
                    # Gửi code và prompt tới AI
                    send_to_ai(function_name, function_code, prompt, default_model_code)
                    return
                else:
                    print(f"Không tìm thấy code chi tiết của hàm {function_name}.\n")
                    return
            except Exception as e:
                print(f"Đã xảy ra lỗi khi đọc file {filepath}: {e}")
                return

    print(f"Không tìm thấy hàm {function_name} trong danh sách đã quét.\n")


def display_file(file_name, prompt):
    """
    Tìm và hiển thị nội dung của file dựa trên tên file và đường dẫn.
    Sau đó gửi nội dung file và prompt tới AI để phân tích.
    """
    # Kiểm tra xem function_list có tồn tại và không rỗng
    if not function_list:
        print("Danh sách function_list rỗng hoặc không tồn tại.\n")
        return

    found_files = [filepath for filepath, _ in function_list if file_name in filepath]

    if not found_files:
        print(f"Không tìm thấy file {file_name} trong danh sách đã quét.\n")
        return

    # Hiển thị nội dung của các file tìm được
    for filepath in found_files:
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()

            if content:
                send_to_ai(filepath, content, prompt, default_model_code)
            else:
                print(f"Nội dung file {filepath} rỗng.\n")
        except Exception as e:
            print(f"Đã xảy ra lỗi khi đọc file {filepath}: {e}\n")
