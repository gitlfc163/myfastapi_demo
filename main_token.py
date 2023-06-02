
import datetime
import statistics
from typing import Union

from pydantic import BaseModel,Field
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from fastapi import Depends, HTTPException,FastAPI,status

from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta


app = FastAPI();

# 定义token模型
SECRET_KEY = "ea3451e8975a49486794a2a4373b89a757d1e0f7b1ebf42cb427e9594dd1d569"
# 生成token的算法
ALGORITHM = "HS256"
# token过期时间
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# 定义token模型
fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": True,
    }
}

# 定义token模型
class Token(BaseModel):
    access_token: str=Field(None, title="token", description="token")
    token_type: str=Field(None, title="token类型", description="token类型")

# 定义token模型
class TokenData(BaseModel):
    username: str =Field(None, title="用户名", description="用户名")

# 定义用户模型
class User(BaseModel):
    username: str
    email: Union[str, None] = Field(None, title="邮箱", description="邮箱", max_length=50)
    full_name: Union[str, None] = Field(None, title="姓名", description="姓名", max_length=50)
    disabled: Union[bool, None] = Field(None, title="是否禁用", description="是否禁用")

# 定义用户模型
class UserInDB(User):
    hashed_password: str

# 
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 定义安全模式 OAuth2PasswordBearer 为安全模式的一种 用于获取token 用于认证 用于权限 用于限流等
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# 验证密码
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# 获取密码hash
def get_password_hash(password):
    return pwd_context.hash(password)

# 获取用户
def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)
    
# 用于身份验证，并返回用户

def authenticate_user(fake_db, username: str, password: str):
    if username not in fake_db:
        return None
    user_dict = fake_db[username]
    # 验证密码
    if not verify_password(password, user_dict["hashed_password"]):
        return None
    # 返回用户
    return UserInDB(**user_dict)

# 定义令牌端点响应的 Pydantic 模型
def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# 获取当前用户 解码并校验接收到的令牌，然后，返回当前用户
async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # 解码token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # 获取用户名
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

# 获取当前活动的用户
async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

# 用令牌过期时间创建 timedelta 对象 用于身份验证，并返回用户
@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=statistics.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# 用于身份验证，并返回用户
@app.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user

# 用于身份验证，
@app.get("/users/me/items/")
async def read_own_items(current_user: User = Depends(get_current_active_user)):
    return [{"item_id": "Foo", "owner": current_user.username}]