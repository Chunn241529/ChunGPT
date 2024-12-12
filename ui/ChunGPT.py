import streamlit as st
from openai import OpenAI
import datetime

# Get today's date
today = datetime.datetime.now().strftime("%Y-%m-%d")

# Custom AI instructions
custom_ai = f"""
        - Hôm nay: {today}.
        - Bạn là ChunGPT.
        - Bạn là một assistant tận tâm.
        - Bạn nhiệt huyết và luôn cố gắng thực hiện theo yêu cầu của tôi hết mình và đầy đủ.
        - Bạn luôn cố gắng kèm thêm link ở cuối tin nhắn để thêm thông tin cho người dùng.
    """

# Sidebar: API key input
with st.sidebar:
    ollama_api_key = "ollama"
    # "[Get an Ollama API key](https://ollama.com/)"
    "[View the source code](https://github.com/streamlit/llm-examples/blob/main/Chatbot.py)"

st.title("💬 ChunGPT")
st.caption("🚀 ChunGPT powered by Ollama")

# Initialize message state with custom AI instructions
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {
            "role": "system",
            "content": custom_ai,
        },  # Add system instructions, but don't display it in the chat
        {"role": "assistant", "content": "Chào, tôi có thể giúp gì cho bạn?"},
    ]

# Display previous messages (but exclude system message from the chat)
for msg in st.session_state.messages:
    if msg["role"] != "system":  # Skip displaying system messages
        st.chat_message(msg["role"]).write(msg["content"])

# Input from user
if prompt := st.chat_input(placeholder=" Nhập tin nhắn..."):
    if not ollama_api_key:
        st.info("Please add your Ollama API key to continue.")
        st.stop()

    # Append user input to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # Create a placeholder for loading
    loading_placeholder = st.empty()
    with loading_placeholder.container():
        st.chat_message("assistant").write("🤔🤔🤔")  # Hiển thị hiệu ứng loading

    # Create the Ollama client with the base URL and API key
    client = OpenAI(
        base_url="https://74bd-171-243-49-10.ngrok-free.app/v1", api_key=ollama_api_key
    )

    # Request the response from Ollama using the chat completions API
    response = client.chat.completions.create(
        model="qwen2.5:14b", messages=st.session_state["messages"]
    )
    msg = response.choices[0].message.content

    # Replace loading message with actual response
    loading_placeholder.empty()  # Xóa hiệu ứng loading
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)
