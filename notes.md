# notes

---

## first-steps

### api docs

- http://127.0.0.1:8000/docs
- http://127.0.0.1:8000/redoc
- http://127.0.0.1:8000/openapi.json

### terms:

- path

  - url, route, endpoint

- operation

  - HTTP methods (post, get, put, delete, ...)

- path operation decorator

  - ex: @app.get("/")
  - take the function below and do something with it

- path operation function

  - when received a request to the url via the decorator, call this function

- async
  - asynchronous code - wait for something to finish before doing something else

---

## path parameters

### terms

- path parameter

  - path parameter can be predefined using Enum
  - cannot contain paths (ex: /files/{file_path} -> /files/home/johndoe/myfile.txt)
    - can use path converter (ex: /files/{file_path:path})

- parameter typing

- data conversion

  - with type declaration, fastapi gives automatic request parsing

- data validation

  - data validation is performed by Pydantic

- path converter

---

## query parameter

### terms

- query parameters

  - other function parameters that are not part of the path parameters, they are automatically interpreted as "query" parameters.
  - The query is the set of key-value pairs that go after the ? in a URL, separated by & characters.
    - http://127.0.0.1:8000/items/?skip=0&limit=10

- query parameter defaults

- optional query parameters

- query parameter type conversion

---

## request body

### terms

- request body

  - data that is sent from client to api and get a response
  - in fastapi, use Pydantic models to declare request body
    - `from pydantic import BaseModel`

- fastapi can declare request body, path parameter, and query parameter at the same time

---

## query parameters and string validations

- Annotated from typing is used to add metadata to parameters
- and using Query from fastapi to add validations

---

## 10 body - nested models

Pydantic model benefits

- Editor support (completion everywhere!)
- Data conversion (a.k.a. parsing / serialization)
- Data validation
- Schema documentation
- Automatic docs


---


When using any of:

Path()
Query()
Header()
Cookie()
Body()
Form()
File()

you can also declare a group of examples with additional information that will be added to their JSON Schemas inside of OpenAPI.

---

## 17 response model - return type 

### terms:

- response 
- return type 
- type annotations 


- we want the model to filter/remove some data, we can use classes and inheritance to take advantage of function type annotations to get better support in the editor and tools, and still get the FastAPI data filtering.

```python 
class BaseUser(BaseModel): 
    username: str 
    email: EmailStr 
    full_name: str | None = None 

class UserIn(BaseUser): 
    password: str 

@app.post("/user/") 
async def create_user(user: UserIn) -> BaseUser: 
    return user 
```









