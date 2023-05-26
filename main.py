
from enum import Enum
from typing import Union
from click import File;

from fastapi import Cookie, Form,Header,FastAPI,File, UploadFile
from pydantic import BaseModel,Field


app = FastAPI();

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
async def read_item(item_id: int, q: Union[bool, None] = None):
    return {"item_id": item_id, "q": q}

# 更新数据
@app.put("/items/{item_id}", summary="更新商品信息", description="更新商品信息", tags=["items"])
async def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}

# 获取模型信息
@app.get("/models/{model_name}", summary="获取模型信息", description="获取模型信息", tags=["models"])
async def get_model(model_name: ModelName):
    if model_name == ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}
    elif model_name == ModelName.lenet:
        return {"model_name": model_name, "message": "LeCNN all the images"}
    return {"model_name": model_name, "message": "Have some residuals"}

# 获取模型信息
@app.get("/getitem/{item_id}", summary="获取模型信息", description="获取模型信息", tags=["fake_items"], response_model=Item)
async def read_item(item_id: int, q: str = None):
    item = await fake_items_db(item_id, q)
    return item

# 获取分页模型信息
@app.get("/items/", summary="获取分页模型信息", description="获取分页模型信息", tags=["items"], response_model=Item)
async def read_items_pages(skip: int = 0, limit: int = 10):
    return fake_items_db[skip: skip + limit]

# Cookie参数
@app.get("/readcookie/", summary="Cookie参数", description="Cookie参数", tags=["readcookie"])
async def read_cookie(adsid: Union[str, None] = Cookie(default=None)):
    return {"adsid": adsid}

# Header参数
@app.get("/header/", summary="Header参数", description="Header参数", tags=["header"])
async def read_header(strange_header: Union[str, None] = Header(default=None)):
    return {"strange_header": strange_header}

# 获取表单参数
@app.post("/create_item/", summary="获取表单参数", description="获取表单参数", tags=["form_demo"])
async def create_item(item: Item):
    return item

# 获取表单参数
@app.post("/login/", summary="获取表单参数", description="获取表单参数", tags=["form_demo"])
async def login(username: str = Form(), password: str = Form()):
    # print(username,password)
    return {"username": username}

# 请求文件
@app.post("/files/", summary="请求文件", description="请求文件", tags=["files_demo"])
async def create_file(file: bytes = File(...)):
    return {"file_size": len(file)}

# 上传文件
@app.post("/uploadfile/", summary="上传文件", description="上传文件", tags=["files_demo"])
async def create_upload_file(file: UploadFile):
    return {"filename": file.filename}

# 请求表单与文件
@app.post("/upload_and_form/", summary="请求表单与文件", description="请求表单与文件", tags=["files_demo"])
async def create_upload_file(file: UploadFile = File(...), token: str = Form(...)):
    return {"filename": file.filename, "token": token}