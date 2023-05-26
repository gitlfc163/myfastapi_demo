from dataclasses import dataclass
from typing import Union;

from fastapi import FastAPI
from pydantic import BaseModel,Field

"""
FastAPI 是一个现代、快速（高性能）的 Web 框架，基于 Python 3.6+，并且完全兼容 Python 3.7+。
"""
app = FastAPI();

# 定义数据模型
# @dataclass(title="商品信息",description="商品信息")
class Item(BaseModel):
    # 姓名
    name: str=Field(...,title="姓名",description="姓名",max_length=50)
    # 价格
    price: float= Field(...,title="价格",description="价格",gt=0)
    # 是否为优惠商品
    is_offer: Union[bool,None]= Field(None,title="是否为优惠商品",description="是否为优惠商品")
    
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