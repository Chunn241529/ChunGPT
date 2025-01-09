import streamlit as st
from datetime import datetime
from respositories.server_respository import Repository_server
from helper.database_client import create_database_client

# Khởi tạo đối tượng quản lý cơ sở dữ liệu
db_manager = Repository_server("chatbot_v2_server.sqlite3")

st.title("Đăng nhập tài khoản")

username = st.text_input("Tên đăng nhập:")
password = st.text_input("Mật khẩu:", type="password")
if st.button("Đăng nhập"):
    try:
        user = db_manager.get_user_by_username(username)
        if user and user["password"] == password:
            st.success(f"Đăng nhập thành công! Xin chào {user['name']}")
            st.switch_page("home")
        else:
            st.error("Tên đăng nhập hoặc mật khẩu không chính xác!")
    except Exception as e:
        st.error(f"Có lỗi xảy ra: {e}")
