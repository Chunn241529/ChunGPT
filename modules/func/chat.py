import sys

from openai import OpenAI
from helpers.formatted import *
from helpers.clean_pycache import *
from func.models import *
from func.clear_terminal import *

# url = main_ngrok() or "http://localhost:11434/"
# Initialize OpenAI client
client = OpenAI(base_url=f"http://localhost:11434/v1", api_key="ollama")

messages = []
function_list = []

console = Console()


def send_to_ai(_name_, _content_, prompt, models):
    """
    Gửi đoạn code của hàm cùng prompt tới AI và nhận phản hồi.

    Args:
        function_name (str): Tên hàm.
        function_code (str): Mã nguồn của hàm.
        prompt (str): Lời nhắc gửi đến AI.
        models (str): Tên mô hình AI để sử dụng.

    Returns:
        None
    """
    # Kiểm tra và xử lý function_code nếu bị None
    if _content_ is None:
        _content_ = ""

    messages.append({"role": "system", "content": "Dùng tiếng Việt là chủ yếu"})

    # Chuẩn bị nội dung tin nhắn
    message = f"{_content_}\n\n{prompt}\n"
    messages.append({"role": "user", "content": message})

    try:
        # Gửi yêu cầu đến API với JSON nén
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
