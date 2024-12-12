import os
import sys

# Đi lên một cấp để đến thư mục gốc của dự án và sau đó thêm thư mục 'respositories'
sys.path.append(os.path.join("modules"))

from respositories.server_respository import Repository_server

# Tạo đối tượng repo từ Repository_server
repo = Repository_server("chatbot_v2_server.sqlite3")


# Hàm đăng ký
def register(
    name,
    username,
    email,
    password,
    phone,
    country_code,
    profile_picture,
    bio,
    date_of_birth,
    database_client,
):
    # Gọi phương thức insert_user để thêm người dùng vào cơ sở dữ liệu
    register1 = repo.insert_user(
        name,
        username,
        email,
        password,
        phone,
        country_code,
        profile_picture,
        bio,
        date_of_birth,
        database_client,
    )
    getUserByUserId(register1)
    return register1


def getUserByUserId(user_id):
    user = repo.get_user_by_id(user_id)
    # print(user)
    return user


# getUserByUserId(3)

# Gọi hàm register với các tham số
# a = register(
#     "trung",
#     "trung",
#     "trung@gmail.com",
#     "123",
#     "09123123123",
#     "84",
#     "abc",
#     "trung nè",
#     "24/01/2002",
#     "trung",
# )
