from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

# 导入基本映射类 Base 类 
from .database import Base

# 定义数据库模型-User
class User(Base):
    # 定义数据库表名 users
    __tablename__ = "users"
    # 定义数据库模型字段 id, email, hashed_password, is_active
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    # 定义数据库模型关系 items 一对多 items.owner_id = users.id
    items = relationship("Item", back_populates="owner")

# 定义数据库模型-Item
class Item(Base):
    # 定义数据库表名 items
    __tablename__ = "items"
    # 定义数据库模型字段 id, title, description, owner_id
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    # 定义数据库模型关系 owner 多对一 items.owner_id = users.id
    owner = relationship("User", back_populates="items")