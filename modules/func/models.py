# List of available models
available_models = [
    "qwen2.5-coder:14b",
    "llama3.2-vision:11b",
    "llama3.1:8b",
    "qwen2.5:14b",
]
default_model = "llama3.1:8b"
default_model_code = "qwen2.5-coder:14b"


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
