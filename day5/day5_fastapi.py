from fastapi import FastAPI
from enum import Enum

class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"
    기타 =  "기타"

fake_items_db = [{"item_name":"Foo"}, {"item_name": "Bar"}, {"item_name":"baz"}]

app = FastAPI()

# http://127.0.0.1:8000

@app.get("/")
def read_root():
    return{"Hello" : "Word"}

# http://127.0.0.1:8000/items/{4444}

@app.get("/item/{items_id}")
def read_item(item_id:int, q:str | None=None):
    return{"item_id":item_id, "q":q}

# http://127.0.0.1:8000/users/me

@app.get("/users/me")
async def read_user_me():
    return {"user_id": "나는 me입니다"}

# http://127.0.0.1:8000/users/사용자

@app.get("/users/{user_id}")
async def read_user(user_id: str):
    return {"user_id": user_id}

# 경로가 중복인 경우 순차적으로 경로가 먼저 매칭되기 때문에 첫 번째 것이 항상 사용 됨.

@app.get("/users")
async def read_users():
    return ["Rick", "Morty"]


@app.get("/users")
async def read_users2():
    return ["Bean", "Elfo"]

# http://127.0.0.1:8000/models

@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    #키를 요청하면,  값을 return
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    # 값을 요청하면,  키를 return
    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}
    # 그 외의 나머지 값
    return {"model_name": model_name, "message": "Have some residuals"}

# http://127.0.0.1:8000/items

@app.get("/items/")
async def read_item(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]
    #return fake_items_db[0:10]
    #return fake_items_db[0:2]
    # 범위 연산자

# https://127.0.0.1:8000/items2/{test}
# https://127.0.0.1:8000/items2/{test}?q=None
# https://127.0.0.1:8000/items2/{test}?q=qqqq


@app.get("/items2/{item_id}")
async def read_item(item_id: str, q: str | None=None):
    if q:
        return{"item_id": item_id, "q":q}
    return {"item_id":item_id}