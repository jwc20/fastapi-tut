from typing import Annotated

from fastapi import FastAPI, Path, Query
from pydantic import BaseModel


app = FastAPI()


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


################################################################################################

##### mix of path, query, and request body parameters
# @app.put("/items/{item_id}")
# async def update_item(
#     item_id: Annotated[int, Path(title="The ID of the item to get", ge=0, le=100)],
#     q: str | None = None,
#     item: Item | None = None,
# ):
#     results: dict[str, object] = {"item_id": item_id}


#     if q:
#         results.update({"q": q})

#     if item:
#         results.update({"item": item})

#     return results


class User(BaseModel):
    username: str
    full_name: str | None = None


# @app.put("/items/{item_id}")
# async def update_item(item_id: int, item: Item, user: User):
#     results = {"item_id": item_id, "item": item, "user": user}
#     return results

################################################################################################
# singular value in body

from fastapi import Body, FastAPI


@app.put("/items/{item_id}")
async def update_item(
    item_id: int, item: Item, user: User, importance: Annotated[int, Body()]
):
    results = {"item_id": item_id, "item": item, "user": user, "importance": importance}
    return results

################################################################################################
# multiple body params and query
# this is showing that we can use multiple params


@app.put("/items/{item_id}")
async def update_item(
    *,
    item_id: int,
    item: Item,
    user: User,
    importance: Annotated[int, Body(gt=0)],
    q: str | None = None,
):
    results = {"item_id": item_id, "item": item, "user": user, "importance": importance}
    if q:
        results.update({"q": q})
    return results

################################################################################################
# embed a single body param
# => item: Item = Body(embed=True)


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Annotated[Item, Body(embed=True)]):
    results = {"item_id": item_id, "item": item}
    return results


"""
then the expected body would be 
{
    "item": {
        "name": "Foo",
        "description": "The pretender",
        "price": 42.0,
        "tax": 3.2
    }
}

instead of 
{
    "name": "Foo",
    "description": "The pretender",
    "price": 42.0,
    "tax": 3.2
}
"""

################################################################################################
