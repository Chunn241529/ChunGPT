import streamlit as st
from datetime import datetime
from respositories.server_respository import Repository_server
from helper.database_client import create_database_client

# Khởi tạo đối tượng quản lý cơ sở dữ liệu
db_manager = Repository_server("chatbot_v2_server.sqlite3")

st.title("Đăng ký tài khoản mới")

# Khởi tạo các giá trị mặc định cho session_state nếu chưa có
if "name" not in st.session_state:
    st.session_state.name = ""
    st.session_state.username = ""
    st.session_state.email = ""
    st.session_state.password = ""
    st.session_state.confirm_password = ""
    st.session_state.phone = ""
    st.session_state.country_code = "VN"  # Giá trị mặc định
    st.session_state.bio = ""
    st.session_state.date_of_birth = datetime.now()

# Các trường nhập liệu
name = st.text_input("Họ và tên:", value=st.session_state.name, key="name")
username = st.text_input(
    "Tên đăng nhập:", value=st.session_state.username, key="username"
)
email = st.text_input("Email:", value=st.session_state.email, key="email")
password = st.text_input(
    "Mật khẩu:", type="password", value=st.session_state.password, key="password"
)
confirm_password = st.text_input(
    "Xác nhận mật khẩu:",
    type="password",
    value=st.session_state.confirm_password,
    key="confirm_password",
)

# Danh sách mã quốc gia, tên quốc gia và mã số điện thoại
country_codes = {
    "VN": {"name": "Việt Nam", "code": "+84"},
    "CN": {"name": "China", "code": "+86"},
    "US": {"name": "United States", "code": "+1"},
    "UK": {"name": "United Kingdom", "code": "+44"},
    "RU": {"name": "Russia", "code": "+7"},
    "KR": {"name": "South Korea", "code": "+82"},
    "JP": {"name": "Japan", "code": "+81"},
    "CU": {"name": "Cuba", "code": "+53"},
    "IN": {"name": "India", "code": "+91"},
}

# Hiển thị danh sách "Quốc gia + Mã điện thoại", trả về mã quốc gia
country_code = st.selectbox(
    "Mã quốc gia (tùy chọn):",
    options=country_codes.keys(),
    format_func=lambda code: f"{country_codes[code]['name']} {country_codes[code]['code']}",
    key="country_code",
)
phone = st.text_input(
    "Số điện thoại (tùy chọn):", value=st.session_state.phone, key="phone"
)

# Tải ảnh đại diện
profile_picture = st.file_uploader("Ảnh đại diện", type=["jpg", "jpeg", "png"])

# Giới thiệu và ngày sinh
bio = st.text_area("Giới thiệu về bản thân:", value=st.session_state.bio, key="bio")
date_of_birth = st.date_input(
    "Ngày sinh:", value=st.session_state.date_of_birth, key="date_of_birth"
)

if st.button("Đăng ký"):
    # Kiểm tra mật khẩu
    if password != confirm_password:
        st.error("Mật khẩu không khớp!")
        st.stop()

    # Kiểm tra email hợp lệ
    if "@" not in email or "." not in email.split("@")[-1]:
        st.error("Email không hợp lệ!")
        st.stop()

    # Chuẩn bị dữ liệu ảnh đại diện
    profile_picture_data = None
    if profile_picture:
        profile_picture_data = profile_picture.read()

    database_client = f"__{username}__.sqlite3"
    # Tạo tài khoản
    try:
        user_id = db_manager.insert_user(
            name=name,
            username=username,
            email=email,
            password=password,
            phone=phone.strip() or None,
            country_code=country_code.strip() or None,
            profile_picture=profile_picture_data,
            bio=bio,
            date_of_birth=date_of_birth,
            database_client=database_client,
        )
        st.success(f"Đăng ký thành công! Mã người dùng: {user_id}")
        create_database_client(database_client)

        # Reset các trường nhập liệu sau khi đăng ký thành công
        # Không cần gán lại giá trị cho các widget, chỉ làm sạch giá trị trong session_state
        st.session_state.name = ""
        st.session_state.username = ""
        st.session_state.email = ""
        st.session_state.password = ""
        st.session_state.confirm_password = ""
        st.session_state.phone = ""
        st.session_state.country_code = "VN"  # Mặc định
        st.session_state.bio = ""
        st.session_state.date_of_birth = datetime.now()

        # Nếu muốn làm mới lại ảnh, cần yêu cầu người dùng tải ảnh lại.
        # st.session_state.profile_picture = None  # Không thể reset file uploader.

    except ValueError as e:
        st.error(str(e))
    except Exception as e:
        st.error(f"Có lỗi xảy ra: {e}")

st.write("Hãy chắc chắn tất cả thông tin chính xác trước khi đăng ký!")
