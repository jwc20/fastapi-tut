from enum import Enum
from fastapi import FastAPI  # import fastapi
from pydantic import BaseModel
from typing import Annotated
from fastapi import FastAPI, Query, Path
from pydantic import AfterValidator
import random
from pydantic import BaseModel, Field

from typing import Annotated, Literal


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
# @app.get("/items/")
# async def read_items(skip: int = 0, limit: int = 10):
#     # The query is the set of key-value pairs that go after the ? in a URL, separated by & characters.
#     # http://127.0.0.1:8000/items/?skip=0&limit=10
#     return fake_items_db[skip : skip + limit]


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

# @app.get("/users/{user_id}/items/{item_id}")
# async def read_user_item(
#     user_id: int, item_id: str, q: str | None = None, short: bool = False
# ):
#     item = {"item_id": item_id, "owner_id": user_id}
#     if q:
#         item.update({"q": q})
#     if not short:
#         item.update(
#             {"description": "This is an amazing item that has a long description"}
#         )
#     return item


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


# declare request body model using BaseModel from pydantic
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


# @app.post("/items/")
# async def create_item(item: Item):
#     return item

# ---------------------------------------------------------


@app.post("/items/")
async def create_item(item: Item):
    item_dict = item.dict()
    if item.tax is not None:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict


# ---------------------------------------------------------

# request body + path parameters
# fastapi will automatically recognize that the function parameter should be taken from the
# path parameter if it has the same name ('item_id')
# and recognize that the function parameter that was declared by the Pydantic model
# should be taken from the request body

# @app.put("/items/{item_id}")
# async def update_item(item_id: int, item: Item):
#     return {"item_id": item_id, **item.dict()}

# ---------------------------------------------------------

# request body + path + query parameters

# **item.dict()
#  dictionary unpacking operator


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item, q: str | None = None):
    result = {
        "item_id": item_id,
        **item.dict(),
    }  # merge contents from item's dictionary to result
    if q:
        result.update({"q": q})
    return result


# ---------------------------------------------------------

# @app.get("/items/")
# async def read_items(q: str | None = None):
#     results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
#     if q:
#         results.update({"q": q})
#     return results

# ---------------------------------------------------------

# query parameters and string validations

# from typing import Annotated
# from fastapi import FastAPI, Query

# Annotated is used to add metadata to parameters

# we are adding validation to check if the query parameter q is of length 50

# @app.get("/items/")
# async def read_items(q: Annotated[str | None, Query(max_length=50)] = None):
#     results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
#     if q:
#         results.update({"q": q})
#     return results

# ---------------------------------------------------------

# query as the default value or in Annotated

# this is not allowed, since it's not clear if the default value is rick or morty
# q: Annotated[str, Query(default="rick")] = "morty"

# should be
# q: Annotated[str, Query()] = "rick"

# Using Annotated is recommended instead of the default value in function parameters, it is better for multiple reasons. 🤓


# ---------------------------------------------------------

# add more validations
# @app.get("/items/")
# async def read_items(q: Annotated[str | None, Query(min_length=3 , max_length=50)] = None):
#     results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
#     if q:
#         results.update({"q": q})
#     return results

### add regular expressions
# @app.get("/items/")
# async def read_items(
#     q: Annotated[
#         str | None, Query(min_length=3, max_length=50, pattern="^fixedquery$")
#     ] = None,
# ):
#     results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
#     if q:
#         results.update({"q": q})
#     return results


### changing the default value of q
# async def read_items(q: Annotated[str | None, Query(min_length=3 , max_length=50)] = "CHANGED_DEFAULT_VALUE):

### make the query parameter q required
# by not declaring the default value and not declaring the None value type
# async def read_items(q: Annotated[str, Query(min_length=3 , max_length=50)]):

### we can make change to accept None by declaring the None value type and not declaring the default value
# async def read_items(q: Annotated[str | None, Query(min_length=3 , max_length=50)]):

### we can define the query parameter to receive list of values
# async def read_items(q: Annotated[list[str] | None, Query()] = None):
### then the url will be http://localhost:8000/items/?q=foo&q=bar

### we can define multiple default values if we are receiving list of values
# async def read_items(q: Annotated[list[str], Query()] = ["foo", "bar"]):

# ---------------------------------------------------------

# declare more metadata for api documentation
# @app.get("/items/")
# async def read_items(
#     q: Annotated[
#         str | None,
#         Query(
#             title="Query string",
#             description="Query string for the items to search in the database that have a good match",
#             min_length=3,
#         ),
#     ] = None,
# ):
#     results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
#     if q:
#         results.update({"q": q})
#     return results
#

# ---------------------------------------------------------
"""
Imagine that you want the parameter to be item-query.

Like in:


http://127.0.0.1:8000/items/?item-query=foobaritems
But item-query is not a valid Python variable name.

The closest would be item_query.

But you still need it to be exactly item-query...

Then you can declare an alias, and that alias is what will be used to find the parameter value:
"""

# @app.get("/items/")
# async def read_items(
#     q: Annotated[
#         str | None,
#         Query(
#             title="Query string",
#             description="Query string for the items to search in the database that have a good match",
#             min_length=3,
#             alias="item-query",
#         ),
#     ] = None,
# ):
#     results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
#     if q:
#         results.update({"q": q})
#     return results

# ---------------------------------------------------------

# show the path as deprecated in api doc
# Query(deprecated=True)

# @app.get("/items/")
# async def read_items(
#     q: Annotated[
#         str | None,
#         Query(
#             alias="item-query",
#             title="Query string",
#             description="Query string for the items to search in the database that have a good match",
#             min_length=3,
#             max_length=50,
#             pattern="^fixedquery$",
#             deprecated=True,
#         ),
#     ] = None,
# ):
#     results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
#     if q:
#         results.update({"q": q})
#     return results


# ---------------------------------------------------------

# to exclude parameters from openAPI
# Query(include_in_schema=False)

# @app.get("/items/")
# async def read_items(
#     hidden_query: Annotated[str | None, Query(include_in_schema=False)] = None,
# ):
#     if hidden_query:
#         return {"hidden_query": hidden_query}
#     else:
#         return {"hidden_query": "Not found"}

# ---------------------------------------------------------

# we can add custom validation for validations that is not shown above using Query
# e.g. after validating the value is a int, we want to check if it's even
# we can do this by using Pydantic's AfterValidator inside Annotated

# from pydantic import AfterValidator


data = {
    "isbn-9781529046137": "The Hitchhiker's Guide to the Galaxy",
    "imdb-tt0371724": "The Hitchhiker's Guide to the Galaxy",
    "isbn-9781439512982": "Isaac Asimov: The Complete Stories, Vol. 2",
}


def check_valid_id(id: str):
    if not id.startswith(("isbn-", "imdb-")):
        raise ValueError('Invalid ID format, it must start with "isbn-" or "imdb-"')
    return id


# @app.get("/items/")
# async def read_items(
#     id: Annotated[str | None, AfterValidator(check_valid_id)] = None,
# ):
#     if id:
#         item = data.get(id)
#     else:
#         id, item = random.choice(list(data.items()))
#     return {"id": id, "name": item}


# ---------------------------------------------------------

# Path parameters and numerical validations

# from typing import Annotated
# from fastapi import FastAPI, Path, Query


# @app.get("/items/{item_id}")
# async def read_items(
#     item_id: Annotated[int, Path(title="The ID of the item to get")], # adding title metadata
#     q: Annotated[str | None, Query(alias="item-query")] = None,
# ):
#     results = {"item_id": item_id}
#     if q:
#         results.update({"q": q})
#     return results


# the doc mentions that if we have non-default value and not using Annotated could cause error
# using Annotated just avoids the error

# @app.get("/items/{item_id}")
# async def read_items(
#     q: str, item_id: Annotated[int, Path(title="The ID of the item to get")]
# ):
#     results = {"item_id": item_id}
#     if q:
#         results.update({"q": q})
#     return results


## numeric validations
# gt: greater than
# ge: greater than or equal
# lt: less than
# le: less than or equal


@app.get("/items/{item_id}")
async def read_items(
    *,
    item_id: Annotated[int, Path(title="The ID of the item to get", ge=0, le=1000)],
    q: str,
    size: Annotated[float, Query(gt=0, lt=10.5)],
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    if size:
        results.update({"size": size})
    return results


# ---------------------------------------------------------


class FilterParams(BaseModel):
    # can add this to prevent extra data sending
    # model_config = {"extra": "forbid"}

    limit: int = Field(100, gt=0, le=100)
    offset: int = Field(0, ge=0)
    order_by: Literal["created_at", "updated_at"] = "created_at"
    tags: list[str] = []


@app.get("/items/")
async def read_items(filter_query: Annotated[FilterParams, Query()]):
    return filter_query

