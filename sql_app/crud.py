
# 导入 Session 类，用于创建数据库会话
from sqlalchemy.orm import Session

# 从 . import models, schemas 导入模型和模式
from sql_app import models, schemas

# 创建 get_user 函数，它接受一个 db 参数和一个 user_id 参数，返回数据库中的用户。
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

# 创建 get_user_by_email 函数，它接受一个 db 参数和一个 email 参数，返回数据库中的用户。
def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

# 创建 get_users 函数，它接受一个 db 参数、一个 skip 参数和一个 limit 参数，返回数据库中的用户。
def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

# 创建 create_user 函数，它接受一个 db 参数和一个 user 参数，返回创建的用户。
def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# 创建 get_items 函数，它接受一个 db 参数、一个 skip 参数和一个 limit 参数，返回数据库中的项目。
def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()

# 创建 create_user_item 函数，它接受一个 db 参数、一个 item 参数和一个 user_id 参数，返回创建的项目。
def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
    db_item = models.Item(**item.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item