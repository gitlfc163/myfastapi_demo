
# Importing the required modules
from pydantic import BaseModel

# 创建模型 ItemBase，它包含 title 和 description 属性，但 description 是可选的。
class ItemBase(BaseModel):
    title: str
    description: str | None = None

# 创建模型 Item，它扩展 ItemBase 并添加 id 和 owner_id 属性。
class ItemCreate(ItemBase):
    pass

# 创建模型 Item，它扩展 ItemBase 并添加 id 和 owner_id 属性。
class Item(ItemBase):
    id: int
    owner_id: int

    # 通过 orm_mode 配置 Pydantic 以从 ORM 模型转换。
    class Config:
        orm_mode = True

# 创建模型 UserBase，它包含 email 属性。
class UserBase(BaseModel):
    email: str

# 创建模型 UserCreate，它扩展 UserBase 并添加 password 属性。
class UserCreate(UserBase):
    password: str

# 创建模型 User，它扩展 UserBase 并添加 id、is_active 和 items 属性。
class User(UserBase):
    id: int
    is_active: bool
    items: list[Item] = []

    # 通过 orm_mode 配置 Pydantic 以从 ORM 模型转换。
    class Config:
        orm_mode = True