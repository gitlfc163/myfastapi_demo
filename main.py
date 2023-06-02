# 导入Depends, FastAPI, HTTPException, Session
from fastapi import FastAPI, Depends, HTTPException
# 导入sqlalchemy.orm包下的Session
from sqlalchemy.orm import Session
# 导入sql_app包下的crud, models, schemas
from sql_app import models,schemas,crud

# 导入sql_app包下engine
from sql_app.database import engine,get_db

# 创建所有表
models.Base.metadata.create_all(bind=engine)

# 创建FastAPI实例
app = FastAPI()


# 创建用户 /users/，它接受一个 user 参数，返回创建的用户。
@app.post("/users/", response_model=schemas.User,description="创建用户",summary="创建用户")
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # 调用crud.py中的get_user_by_email函数，判断用户是否存在
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

# 获取用户 /users/，它接受一个 skip 参数和一个 limit 参数，返回数据库中的用户。
@app.get("/users/", response_model=list[schemas.User],description="获取用户",summary="获取用户")
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    # 调用crud.py中的get_users函数，获取用户
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

# 按用户ID获取用户 /users/{user_id}，它接受一个 user_id 参数，返回数据库中的用户。
@app.get("/users/{user_id}", response_model=schemas.User,description="按用户ID获取用户",summary="按用户ID获取用户")
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

# 按用户ID获取用户项目 /users/{user_id}/items/，它接受一个 user_id 参数，返回数据库中的项目。
@app.post("/users/{user_id}/items/", response_model=schemas.Item,description="按用户ID获取用户项目",summary="按用户ID获取用户项目")
def create_item_for_user(user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)):
    return crud.create_user_item(db=db, item=item, user_id=user_id)

# 获取项目 /items/，它接受一个 skip 参数和一个 limit 参数，返回数据库中的项目。
@app.get("/items/", response_model=list[schemas.Item],description="获取项目",summary="获取项目")
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items