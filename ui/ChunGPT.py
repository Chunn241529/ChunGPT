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
    "[View the source code](https://github.com/Chunn241529/ChunGPT/blob/main/ui/ChunGPT.py)"

st.title("💬 ChunGPT")
st.caption("🚀 ChunGPT powered by Ollama")

# Initialize message state with custom AI instructions
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": custom_ai},  # Add system instructions
        {"role": "assistant", "content": "Chào, tôi có thể giúp gì cho bạn?"},
    ]

# Display previous messages (but exclude system message from the chat)
for msg in st.session_state.messages:
    if msg["role"] != "system":
        st.chat_message(msg["role"]).write(msg["content"])


def generate_llama2_response(prompt):
    """Function to generate response from the AI server."""
    client = OpenAI(
        base_url="https://8668-171-243-49-10.ngrok-free.app/v1",
        api_key=ollama_api_key,
    )
    response = client.chat.completions.create(
        model="qwen2.5:14b", messages=st.session_state["messages"]
    )
    return response.choices[0].message.content


# Input from user
if prompt := st.chat_input(placeholder=" Nhập tin nhắn..."):
    if not ollama_api_key:
        st.info("Please add your Ollama API key to continue.")
        st.stop()

    # Append user input to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # Generate a new response if last message is not from assistant
    if st.session_state.messages[-1]["role"] != "assistant":
        with st.chat_message("assistant"):
            with st.spinner("🤔"):
                response = generate_llama2_response(prompt)
                placeholder = st.empty()
                full_response = ""
                for item in response:
                    full_response += item
                    placeholder.markdown(full_response)
                placeholder.markdown(full_response)
        message = {"role": "assistant", "content": full_response}
        st.session_state.messages.append(message)
