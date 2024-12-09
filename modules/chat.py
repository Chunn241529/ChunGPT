import os
import re
import sys
import time
from openai import OpenAI
from rich.console import Console
from rich.progress import track
import sys


# Add the parent directory of "helpers" to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))
# from ngrok.ngrok import *
from helpers.formatted import *
from helpers.clean_pycache import *

# url = main_ngrok() or "http://localhost:11434/"
# Initialize OpenAI client
client = OpenAI(base_url=f"http://localhost:11434/v1", api_key="ollama")

# List of available models
available_models = [
    "qwen2.5-coder:14b",
    "llama3.2-vision:11b",
    "llama3.1:8b",
]
default_model = "llama3.1:8b"
default_model_code = "qwen2.5-coder:14b"
messages = []
function_list = []

console = Console()


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

    # Thêm `track` để hiển thị tiến trình khi xử lý danh sách file
    for filepath in track(file_paths, description="Loading model... "):
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
            functions = extract_functions(content, filepath)
            function_list.extend(
                [(filepath, func) for func in functions]
            )  # Lưu theo đường dẫn file


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
    for filepath, (type_, name) in function_list:
        if name == function_name:  # Tìm đúng hàm
            try:
                # Đọc file gốc để lấy nội dung đầy đủ của hàm
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()

                # Lấy phần code cụ thể của hàm bằng regex
                if type_ == "def":  # Python function
                    pattern = rf"def {function_name}\(.*?\):[\s\S]*?(?=def|class|$)"
                elif type_ == "class":  # Python class
                    pattern = rf"class {function_name}\(.*?\):[\s\S]*?(?=class|$)"
                else:
                    # JavaScript or CSS case
                    pattern = rf"{function_name}.*?{{[\s\S]*?}}"

                match = re.search(pattern, content)
                if match:
                    function_code = match.group(0)
                    # print(f"\nCode của hàm {function_name} trong file {filepath}:\n")
                    print(function_code)

                    # Gửi đoạn code này và prompt tới AI để phân tích
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

    found_files = []  # Duy trì danh sách các file khớp

    # Duyệt qua danh sách các file đã quét được
    for filepath, (type_, name) in function_list:
        if (
            file_name in filepath
        ):  # Tìm kiếm file dựa trên đường dẫn đầy đủ bao gồm phần mở rộng
            found_files.append(filepath)

    # Nếu không tìm thấy file nào, in thông báo lỗi
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


def send_to_ai(function_name, function_code, prompt, models):
    """
    Gửi đoạn code của hàm cùng prompt tới AI và nhận phản hồi.

    Args:
        function_name (str): Tên hàm.
        function_code (str): Mã nguồn của hàm.
        prompt (str): Lời nhắc gửi đến AI.
        models (str): Tên mô hình AI để sử dụng.
        client (object): Đối tượng client để gọi API AI.
        console (object): Đối tượng console để in ra kết quả với định dạng.
        messages (list): Danh sách các tin nhắn gửi đi và phản hồi.

    Returns:
        None
    """
    # Kiểm tra và xử lý function_code nếu bị None
    if function_code is None:
        function_code = ""

    # Chuẩn bị nội dung tin nhắn
    message = f"{function_code}\n\n{prompt}\n"
    messages.append({"role": "user", "content": message})

    try:
        # Gửi yêu cầu đến API
        response = client.chat.completions.create(
            model=models,
            stream=True,  # Sử dụng stream để nhận từng phần phản hồi
            messages=messages,
        )

        # Ghi đè stdout để tắt bộ đệm (nếu cần)
        sys.stdout = open(sys.stdout.fileno(), "w", buffering=1)

        # Xử lý từng chunk phản hồi
        bot_reply = ""
        for chunk in response:
            # Lấy nội dung từ chunk
            part = getattr(chunk.choices[0].delta, "content", "")
            bot_reply += part

        console.print("\n")

        formatted_response(bot_reply)  # gọi hàm để print

        console.print("\n\n----------\n")

        # Lưu phản hồi của bot vào danh sách messages
        messages.append({"role": "assistant", "content": bot_reply})

    except Exception as e:
        console.print(f"Error: {e}")


def select_model():
    """
    Hiển thị danh sách modal và cho phép người dùng chọn một modal.
    """
    print("Danh sách các modal khả dụng:")
    for idx, model in enumerate(available_models, start=1):
        print(f"{idx}. {model}")

    while True:
        try:
            choice = int(input("\nNhập số tương ứng để chọn modal: ")) - 1
            if 0 <= choice < len(available_models):
                selected_model = available_models[choice]
                print(f"Modal đã chọn: {selected_model}\n")
                return selected_model
            else:
                print("Vui lòng nhập số hợp lệ.")
        except ValueError:
            print("Lựa chọn không hợp lệ. Vui lòng nhập lại.")


def clear_terminal():
    """
    Xóa màn hình terminal trước khi chạy chương trình.
    """
    if sys.platform == "win32":  # Windows
        os.system("cls")
    else:
        os.system("clear")


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
        user_input = input(">>  ")
        if user_input.lower() == "thoát":
            print("Đã thoát chương trình.")
            break

        if user_input.lower() == "/models":
            selected_model = select_model()
            continue

        # Kiểm tra nếu user_input chứa @<tên_hàm>
        match = re.search(r"@<(\w+)>", user_input)
        if match:
            function_name = match.group(1)  # Lấy tên hàm trong <>
            prompt = user_input.replace(f"@<{function_name}>", "").strip()
            display_function_code(function_name, prompt)
            continue

        match = re.search(
            r"#<([\w\.\-]+)>", user_input
        )  # Cập nhật regex để bắt cả phần mở rộng file
        if match:
            file_name = match.group(1)  # Lấy tên file bao gồm phần mở rộng
            prompt = user_input.replace(f"#<{file_name}>", "").strip()
            display_file(file_name, prompt)
            continue

        send_to_ai(None, None, user_input, selected_model)


if __name__ == "__main__":

    main()
