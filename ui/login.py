import streamlit as st
from streamlit_option_menu import option_menu

st.set_page_config(page_title="User Management", layout="wide")


# Chức năng đăng nhập
def login():
    with st.form("login_form"):
        username = st.text_input("Tên Đăng Nhập")
        password = st.text_input("Mật Khẩu", type="password")
        if st.form_submit_button("Đăng nhập"):
            # Đặt logic xác thực ở đây
            st.success(f"Bạn đã đăng nhập với tên {username}!")


# Chức năng đăng ký
def register():
    with st.form("register_form"):
        username = st.text_input("Tên Tài Khoản")
        email = st.text_input("Địa Chỉ Email")
        password = st.text_input("Mật Khẩu", type="password")
        confirmPassword = st.text_input("Xác Nhận Mật Khẩu", type="password")

        if st.form_submit_button("Tạo tài khoản"):
            # Đặt logic tạo user ở đây
            st.success("Đã tạo tài khoản thành công!")


# Chức năng quên mật khẩu
def forgot_password():
    email = st.text_input("Email của bạn:")
    if st.button("Gửi yêu cầu"):
        # Đặt logic gửi mã xác nhận hoặc gợi ý đổi mật khẩu ở đây
        st.success("Chúng tôi đã gửi hướng dẫn vào hộp thư đến.")


# Giao diện option menu
with st.sidebar:
    selected = option_menu(
        menu_title="Menu",
        options=["Đăng nhập", "Tạo tài khoản", "Quên mật khẩu"],
        icons=["sign-in", "person-check", "envelope"],
        default_index=2,  # Default Index
        styles={
            "container": {"padding": "0!important", "background-color": "#F5F5DC"},
            "icon": {"color": "#FB6B41", "font-size": "20px"},
            "nav-link": {
                "font-size": "18px",
                "text-align": "left",
                "margin": "0px",
                "--hover-color": "#F5F5DC",
            },
            "nav-menu": {"display": "flex"},
        },
    )

if selected == "Đăng nhập":
    login()
elif selected == "Tạo tài khoản":
    register()
elif selected == "Quên mật khẩu":
    forgot_password()
