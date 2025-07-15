from enum import Enum
from fastapi import FastAPI  # import fastapi


class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

app = FastAPI()  # init fastapi instance


# ---------------------------------------------------------


# create path/endpoint/route operation, operation refers to the one of the HTTP methods (post, get, put, delete, ... )
@app.get("/")  # define path operation decorator
async def root():
    return {"message": "Hello World"}


# @app.get("/items/{item_id}")
# async def read_item(item_id):
#     return {"item_id": item_id}


# @app.get("/items/{item_id}")
# async def read_item(item_id: int):
#     return {"item_id": item_id}


# order matters -------------------------------------------


@app.get("/users/me")
async def read_user_me():
    return {"user_id": "the current user"}


@app.get("/users/{user_id}")
async def read_user(user_id: str):
    return {"user_id": user_id}


# ---------------------------------------------------------


@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}


# ---------------------------------------------------------


# path converter
# /files/{file_path} -> /files/home/johndoe/myfile.txt
@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}


# ---------------------------------------------------------


# query parameters
@app.get("/items/")
async def read_items(skip: int = 0, limit: int = 10):
    # The query is the set of key-value pairs that go after the ? in a URL, separated by & characters.
    # http://127.0.0.1:8000/items/?skip=0&limit=10
    return fake_items_db[skip : skip + limit]


# ---------------------------------------------------------

# optional query parameters
# in this case, the q is optional and will be None by default
# @app.get("/items/{item_id}")
# async def read_item(item_id: str, q: str | None = None):
#     if q:
#         return {"item_id": item_id, "q": q}
#     return {"item_id": item_id}


# ---------------------------------------------------------


# query parameter type conversion
@app.get("/items/{item_id}")
async def read_item(item_id: str, q: str | None = None, short: bool = False):
    item = {"item_id": item_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item


# ---------------------------------------------------------

# multiple path and query parameters
@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(
    user_id: int, item_id: str, q: str | None = None, short: bool = False
):
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item


# ---------------------------------------------------------

# required query parameters
# when you want to make a query parameter required, you can just not declare any default value:

# @app.get("/items/{item_id}")
# async def read_user_item(item_id: str, needy: str):
#     item = {"item_id": item_id, "needy": needy}
#     return item

@app.get("/items/{item_id}")
async def read_user_item(
    item_id: str, needy: str, skip: int = 0, limit: int | None = None
):
    item = {"item_id": item_id, "needy": needy, "skip": skip, "limit": limit}
    return item

# needy, a required str.
# skip, an int with a default value of 0.
# limit, an optional int.

# ---------------------------------------------------------
