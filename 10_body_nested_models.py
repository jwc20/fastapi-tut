from fastapi import FastAPI
from pydantic import BaseModel, HttpUrl

app = FastAPI()


# class Item(BaseModel):
#     name: str
#     description: str | None = None
#     price: float
#     tax: float | None = None
#     # tags: list[str] = []
#     tags: set[str] = set()


# @app.put("/items/{item_id}")
# async def update_item(item_id:int, item: Item):
#     results = {"item_id": item_id, "item": item}
#     return results


#################################################

# nested models


# define a submodel
class Image(BaseModel):
    url: str
    name: str


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: set[str] = set()
    image: Image | None = None  # use submodel as a type


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    results = {"item_id": item_id, "item": item}
    return results


"""

=> {
    "name": "Foo",
    "description": "The pretender",
    "price": 42.0,
    "tax": 3.2,
    "tags": ["rock", "metal", "bar"],
    "image": {
        "url": "http://example.com/baz.jpg",
        "name": "The Foo live"
    }
}

doing just that declaration, with FastAPI you get:

- Editor support (completion, etc.), even for nested models
- Data conversion
- Data validation
- Automatic documentation
"""


#################################################

# special types and validation


# from pydantic import BaseModel, HttpUrl

class Image(BaseModel):
    url: HttpUrl
    name: str


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: set[str] = set()
    # image: Image | None = None
    image: list[Image] | None = None # lists of submodel


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    results = {"item_id": item_id, "item": item}
    return results

"""
=> {
    "name": "Foo",
    "description": "The pretender",
    "price": 42.0,
    "tax": 3.2,
    "tags": [
        "rock",
        "metal",
        "bar"
    ],
    "images": [
        {
            "url": "http://example.com/baz.jpg",
            "name": "The Foo live"
        },
        {
            "url": "http://example.com/dave.jpg",
            "name": "The Baz"
        }
    ]
}
"""


#################################################
# when you want to have keys of another type (e.g. int)

@app.post("/index-weights/")
async def create_index_weights(weights: dict[int, float]):
    return weights


