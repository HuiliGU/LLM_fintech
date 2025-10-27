# Python类型提示
def get_full_name(first_name: str, last_name: str):
    full_name = first_name.title() + " " + last_name.title()
    return full_name

# Pydantic模型
from pydantic import BaseModel
class User(BaseModel):
    id: int
    name: str
    email: str

# 使用Pydantic模型
def create_user(data: dict) -> User:
    user = User(**data)
    return user

# 示例数据
data = {'id': 1, 'name': 'john doe', 'email': 'john.doe@example.com'}
user = create_user(data)
print(user)

# 输出完整姓名
print(get_full_name(user.name.split()[0], user.name.split()[1]))
