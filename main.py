from fastapi import FastAPI # import fastapi

app = FastAPI() # init fastapi instance

# create path/endpoint/route operation, operation refers to the one of the HTTP methods (post, get, put, delete, ... )
@app.get("/") # define path operation decorator
async def root():
    return {"message": "Hello World"}
