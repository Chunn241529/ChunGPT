from datetime import date
import sys

from openai import OpenAI
from helpers.formatted import *
from helpers.clean_pycache import *
from func.models import *
from func.clear_terminal import *

# respository
from respositories.client_respository import Repository_client

repo = Repository_client("client_db_1.sqlite3")

# url = main_ngrok() or "http://localhost:11434/"
# Initialize OpenAI client
client = OpenAI(base_url=f"http://localhost:11434/v1", api_key="ollama")

# messages = []
function_list = []

console = Console()


def new_chat(custom_ai):
    new_chat = repo.insert_brain_ai(custom_ai)
    return new_chat


def get_brain_ai():
    brain = repo.get_brain_ai()
    return brain


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

    brain_id = 1
    # Lấy lịch sử trò chuyện từ database thay vì sử dụng messages rỗng
    history = repo.get_brain_history_chat()  # Lấy lịch sử trò chuyện

    # Chuyển đổi lịch sử thành dạng mà OpenAI API yêu cầu
    messages = [{"role": role, "content": content} for _, role, content, _ in history]
    today = date.today()

    custom_ai = f"""
        - Hôm nay: {today}
        - Bạn dùng tiếng Việt là chủ yếu. Nên chú ý tới ngữ cảnh, hoàn cảnh phù hợp để nói tiếng Việt không bị SAI.
        - Bạn là một assistant tận tâm, nhiệt huyết và luôn cố gắng thực hiện theo yêu cầu của tôi hết mình và đầy đủ.
    """

    messages.append({"role": "system", "content": custom_ai})

    # Chuẩn bị nội dung tin nhắn
    message = f"{_content_}\n\n{prompt}\n"
    messages.append({"role": "user", "content": message})
    # repo.insert_brain_history_chat(brain_id,"user", message)

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
        # messages.append({"role": "assistant", "content": bot_reply})
        repo.insert_brain_history_chat(brain_id, "assistant", bot_reply)
        if bot_reply.lower() == ".exit":
            console.print("Đã thoát chương trình.")

    except Exception as e:
        console.print(f"Error: {e}")
