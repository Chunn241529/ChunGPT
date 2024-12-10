import re
from rich.console import Console
from rich.syntax import Syntax
from rich.markdown import Markdown

# Khởi tạo đối tượng Console
console = Console()


def formatted_code_block(parts):
    """
    Định dạng đoạn mã code từ các phần của phản hồi bot.
    """
    # Tìm ngôn ngữ của đoạn mã code
    language = "plaintext"  # Mặc định là plain text

    if len(parts) > 1 and parts[1].strip():
        first_line = parts[1].strip().split("\n")[0]
        if len(first_line.split()) == 1:
            language = first_line.strip()
            code = "\n".join(parts[1].strip().split("\n")[1:])
        else:
            code = parts[1].strip()

        # Định dạng đoạn mã code với ngôn ngữ
        syntax = Syntax(code, language, theme="gruvbox-dark", line_numbers=False)
        return syntax


def formatted_response(response):
    """
    Bắt các khối code block trong phản hồi và thay thế bằng định dạng đã tùy chỉnh.
    """
    # BOLD_COLOR = "#ce2479"
    # response = re.sub(r"\*\*(.*?)\*\*", rf"[bold][magenta]\1[/][/]", response)

    # Regex tìm các khối code block: ```ngôn_ngữ\ncode\n```
    code_block_pattern = r"```(.*?)\n(.*?)```"

    # Dùng `finditer` để tìm tất cả các khối code block
    matches = list(re.finditer(code_block_pattern, response, flags=re.DOTALL))
    last_index = 0

    for match in matches:
        # Lấy đoạn văn bản trước khối code block
        text_before = response[last_index : match.start()]
        if text_before.strip():
            console.print(Markdown(text_before), end="")  # In văn bản thường

        # Lấy ngôn ngữ và mã code
        language = match.group(1).strip() or "plaintext"
        code = match.group(2)
        parts = ["", f"{language}\n{code}"]
        syntax = formatted_code_block(parts)

        # Hiển thị khối mã đã định dạng
        console.print(syntax)

        # Cập nhật chỉ số để tiếp tục xử lý đoạn tiếp theo
        last_index = match.end()

    # Hiển thị phần còn lại của văn bản sau khối code cuối
    remaining_text = response[last_index:]
    if remaining_text.strip():
        console.print(Markdown(remaining_text), end="")


# response = (
#     "Hello **world** \n\n"
#     "```python\ndef tinh_tong(n):\n\n"
#     "    return (n * (n + 1)) // 2\n\n"
#     "# Lấy giá trị của n từ người dùng\nn = int(input('Nhập vào một số tự nhiên n: '))\n"
#     "print(f'Độ lớn của n là: {n}')\ntong = tinh_tong(n)\n"
#     "print(f'Tổng các số tự nhiên từ 1 đến {n} là: {tong}')\n```\n\n"
#     "**and welcome**"
# )
# formatted_response(
#     "\n\n---------------------[DEBUG]---------------------\n\n"
#     + response
#     + "\n\n---------------------[DEBUG]---------------------\n\n"
# )
