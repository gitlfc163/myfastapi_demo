
from enum import Enum
from typing import Union
from click import File;

from pydantic import BaseModel,Field
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from fastapi import Cookie, Depends, Form, HTTPException,Header,FastAPI,File, UploadFile,status


app = FastAPI();

# 定义安全模式 OAuth2PasswordBearer 为安全模式的一种 用于获取token 用于认证 用于权限 用于限流等
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# 定义token模型
fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "fakehashedsecret",
        "disabled": True,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "fakehashedsecret2",
        "disabled": True,
    },
}

# 定义用户模型
class User(BaseModel):
    username: str
    email: Union[str, None] = Field(None, title="邮箱", description="邮箱", max_length=50)
    full_name: Union[str, None] = Field(None, title="姓名", description="姓名", max_length=50)
    disabled: Union[bool, None] = Field(None, title="是否禁用", description="是否禁用")

# 定义用户模型
class UserInDB(User):
    hashed_password: str

# 获取用户信息
def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)

# 解析token
def fake_decode_token(token):
    # This doesn't provide any security at all
    # Check the next version
    user = get_user(fake_users_db, token)
    return user

# 获取当前用户
async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

# 生成token
def fake_hash_password(password: str):
    return "fakehashed" + password

# 获取当前活跃用户
async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

# 获取当前用户信息
@app.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user

# `OAuth2PasswordRequestForm` 为安全模式的一种 用于获取token 
@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = UserInDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {"access_token": user.username, "token_type": "bearer"}







# 数据源
fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"},{"item_name": "test1"}, {"item_name": "test2"}, {"item_name": "test3"}]

# 定义数据模型
# @dataclass(title="商品信息",description="商品信息")
class Item(BaseModel):
    # 姓名
    name: str=Field(...,title="姓名",description="姓名",max_length=50)
    # 价格
    price: float= Field(...,title="价格",description="价格",gt=0)
    # 是否为优惠商品
    is_offer: Union[bool,None]= Field(None,title="是否为优惠商品",description="是否为优惠商品")

    # 配置
    class Config:
        # 模型配置
        schema_extra = {
            "example": {
                "name": "Foo",
                "price": 35.4,
                "is_offer": True
            }
        }

# 定义枚举
class ModelName(str,Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

    # 配置
    class Config:
        # 枚举值大小写不敏感
        case_sensitive = True
        schema_extra = {
            "example": {
                "model_name": "alexnet"
            }
        }
 
# 默认入口
@app.get("/",summary="默认入口", description="默认入口", tags=["default"])
def index() -> Union[dict, str]:
    return {
        "message": "Hello, World!"
    };

# 获取商品信息
@app.get("/items/{item_id}",summary="获取商品信息", description="获取商品信息", tags=["items"])
async def read_item(item_id: int, q: Union[bool, None] = None,token: str = Depends(oauth2_scheme)):
    return {"item_id": item_id, "q": q}

# 更新数据
@app.put("/items/{item_id}", summary="更新商品信息", description="更新商品信息", tags=["items"])
async def update_item(item_id: int, item: Item, token: str = Depends(oauth2_scheme)):
    return {"item_name": item.name, "item_id": item_id}

# 获取模型信息
@app.get("/models/{model_name}", summary="获取模型信息", description="获取模型信息", tags=["models"])
async def get_model(model_name: ModelName, token: str = Depends(oauth2_scheme)):
    if model_name == ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}
    elif model_name == ModelName.lenet:
        return {"model_name": model_name, "message": "LeCNN all the images"}
    return {"model_name": model_name, "message": "Have some residuals"}

# 获取模型信息
@app.get("/getitem/{item_id}", summary="获取模型信息", description="获取模型信息", tags=["fake_items"], response_model=Item)
async def read_item_model(item_id: int, q: str = None, token: str = Depends(oauth2_scheme)):
    item = await fake_items_db(item_id, q)
    return item

# 获取分页模型信息
@app.get("/items/", summary="获取分页模型信息", description="获取分页模型信息", tags=["items"], response_model=Item)
async def read_items_pages(skip: int = 0, limit: int = 10, token: str = Depends(oauth2_scheme)):
    return fake_items_db[skip: skip + limit]

# Cookie参数
@app.get("/readcookie/", summary="Cookie参数", description="Cookie参数", tags=["readcookie"])
async def read_cookie(adsid: Union[str, None] = Cookie(default=None), token: str = Depends(oauth2_scheme)):
    return {"adsid": adsid}

# Header参数
@app.get("/header/", summary="Header参数", description="Header参数", tags=["header"])
async def read_header(strange_header: Union[str, None] = Header(default=None), token: str = Depends(oauth2_scheme)):
    return {"strange_header": strange_header}

# 获取表单参数
@app.post("/create_item/", summary="获取表单参数", description="获取表单参数", tags=["form_demo"])
async def create_item(item: Item, token: str = Depends(oauth2_scheme)):
    return item

# 获取表单参数
@app.post("/login/", summary="获取表单参数", description="获取表单参数", tags=["form_demo"])
async def login_test(username: str = Form(), password: str = Form(), token: str = Depends(oauth2_scheme)):
    # print(username,password)
    return {"username": username}

# 请求文件
@app.post("/files/", summary="请求文件", description="请求文件", tags=["files_demo"])
async def create_file(file: bytes = File(...),  token: str = Depends(oauth2_scheme)):
    return {"file_size": len(file)}

# 上传文件
@app.post("/uploadfile/", summary="上传文件", description="上传文件", tags=["files_demo"])
async def create_upload_file(file: UploadFile,  token: str = Depends(oauth2_scheme)):
    return {"filename": file.filename}

# 请求表单与文件
@app.post("/upload_and_form/", summary="请求表单与文件", description="请求表单与文件", tags=["files_demo"])
async def create_upload_file(file: UploadFile = File(...), token: str = Depends(oauth2_scheme)):
    return {"filename": file.filename, "token": token}