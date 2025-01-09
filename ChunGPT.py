import streamlit as st
from openai import OpenAI
import datetime
from respositories.client_respository import (
    Repository_client,
)  # Import your repository class

# Set up your SQLite database path (adjust if necessary)
db_path = "client_db_1.sqlite3"
repo_client = Repository_client(db_path)

st.set_page_config(page_title="ChunGPT", initial_sidebar_state="auto")

# url_ngrok = "https://da22-171-243-49-10.ngrok-free.app"
url_local = "http://localhost:11434"

# Get today's date
today = datetime.datetime.now().strftime("%Y-%m-%d")

# Custom AI instructions
custom_ai = f"""
        - Hôm nay: {today}.
        - Bạn là ChunGPT.
        - Bạn là một assistant tận tâm.
        - Bạn nhiệt huyết và luôn cố gắng thực hiện theo yêu cầu của tôi hết mình và đầy đủ.
        - Bạn luôn có thể kèm link ở cuối tin nhắn để thêm thông tin cho người dùng.
        - Bạn có thể đưa emoji vào tùy trường hợp.
        - Trừ tiếng Anh và Tiếng Việt, bạn không đưa ngôn ngữ khác vào.
        - No Yapping, Limit Prose, No Fluff
    """

# Sidebar: API key input
with st.sidebar:
    ollama_api_key = "ollama"
    "[My source](https://github.com/Chunn241529/ChunGPT/blob/main/ui/ChunGPT.py) 🗃️"
    "[Buy me a coffee](https://github.com/Chunn241529/ChunGPT/blob/main/ui/assets/img/buymecoffee.png?raw=true) ❤️"
    button_clicked = st.sidebar.button("Xóa tin nhắn")
    if button_clicked:
        repo_client.delete_brain_history_chat_all()


st.title("💬 ChunGPT")
st.caption("🚀 ChungGPT được cung cấp bởi OllamaAI")

history = repo_client.get_brain_history_chat()

# Initialize message state with custom AI instructions
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": custom_ai},  # Add system instructions
        {"role": "assistant", "content": "Chào, tôi có thể giúp gì cho bạn?"},
    ]
    # If there is any existing history, add it to the session state
    if history:
        for _, role, content, _ in history:
            st.session_state["messages"].append({"role": role, "content": content})

# Display previous messages (but exclude system message from the chat)
for msg in st.session_state.messages:
    if msg["role"] != "system":
        st.chat_message(msg["role"]).write(msg["content"])


def generate_llama2_response(prompt):
    """Function to generate response from the AI server."""
    client = OpenAI(
        base_url=f"{url_local}/v1",
        api_key=ollama_api_key,
    )

    # Sử dụng stream để nhận dữ liệu từng phần, giúp phản hồi nhanh hơn
    response = client.chat.completions.create(
        model="qwen2.5-coder:7b",
        messages=st.session_state["messages"],
        stream=True,
    )

    return response


# Input from user
if prompt := st.chat_input(placeholder="Nhập tin nhắn..."):
    if not ollama_api_key:
        st.info("Please add your Ollama API key to continue.")
        st.stop()

    # Append user input to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # Insert the user message into the database
    repo_client.insert_brain_history_chat(role="user", content=prompt)

    # Generate a new response if last message is not from assistant
    if st.session_state.messages[-1]["role"] != "assistant":
        with st.chat_message("assistant"):
            # Create a placeholder for the spinner and response
            spinner_placeholder = st.empty()
            response_placeholder = st.empty()

            with spinner_placeholder:
                with st.spinner(""):  # Hiển thị spinner trong khi đang xử lý
                    # Gọi hàm lấy phản hồi từ AI với stream
                    response = generate_llama2_response(prompt)
                    full_response = ""

                    # Hiển thị phản hồi từng phần
                    for chunk in response:
                        content = (
                            chunk.choices[0].delta.content
                            if hasattr(chunk.choices[0].delta, "content")
                            else ""
                        )
                        full_response += content
                        response_placeholder.markdown(
                            full_response
                        )  # Cập nhật mỗi phần của phản hồi

                    # Sau khi có đủ phản hồi, xóa spinner
                    spinner_placeholder.empty()

                # Thêm phản hồi vào lịch sử tin nhắn
                st.session_state.messages.append(
                    {"role": "assistant", "content": full_response}
                )

                # Insert the assistant's response into the database
                repo_client.insert_brain_history_chat(
                    role="assistant", content=full_response
                )
