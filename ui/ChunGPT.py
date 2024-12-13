import streamlit as st
from openai import OpenAI
import datetime
import subprocess

st.set_page_config(page_title="ChunGPT", initial_sidebar_state="auto")


# Function to generate response using CLI
def chat_with_cli(prompt):
    try:
        # Run the CLI command to fetch the chat response
        result = subprocess.run(
            ["ollama", "run", "qwen2.5:14b"],
            input=prompt,
            capture_output=True,
            text=True,
        )
        # Check if the command was successful
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            st.error(
                f"Failed to retrieve response from CLI. Error: {result.stderr.strip()}"
            )
            st.stop()
    except FileNotFoundError:
        st.error(
            "CLI command not found. Ensure the CLI is installed and the correct command is used."
        )
        st.stop()
    except Exception as e:
        st.error(f"Error running CLI command: {e}")
        st.stop()


# Get today's date
today = datetime.datetime.now().strftime("%Y-%m-%d")

# Custom AI instructions
custom_ai = f"""
        - Hôm nay: {today}.
        - Bạn là ChunGPT.
        - Bạn là một assistant tận tâm.
        - Bạn nhiệt huyết và luôn cố gắng thực hiện theo yêu cầu của tôi hết mình và đầy đủ.
        - Bạn luôn cố gắng kèm thêm link ở cuối tin nhắn để thêm thông tin cho người dùng.
        - Bạn có thể đưa emoji vào tùy trường hợp.
        - Trừ tiếng Anh và Tiếng Việt, bạn không đưa ngôn ngữ khác vào.
        - No Yapping, Limit Prose, No Fluff
    """

# Sidebar: API key input
with st.sidebar:
    ollama_api_key = "ollama"
    "[Source của tôi](https://github.com/Chunn241529/ChunGPT/blob/main/ui/ChunGPT.py)"
    st.empty()

st.title("💬 ChunGPT")
st.caption("🚀 ChungGPT được cung cấp bởi OllamaAI")

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

# Input from user
if prompt := st.chat_input(placeholder="Nhập tin nhắn..."):
    # Append user input to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # Generate response using CLI
    with st.chat_message("assistant"):
        # Create a placeholder for the spinner and response
        spinner_placeholder = st.empty()
        response_placeholder = st.empty()

        with spinner_placeholder:
            with st.spinner("Đang xử lý..."):
                # Call the CLI chat function
                full_response = chat_with_cli(prompt)
                response_placeholder.markdown(full_response)  # Display full response

        # Remove spinner after displaying response
        spinner_placeholder.empty()

        # Add response to chat history
        st.session_state.messages.append(
            {"role": "assistant", "content": full_response}
        )
