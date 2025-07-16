import reflex as rx
from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer
from starlette.middleware.cors import CORSMiddleware
from typing import Annotated
from fastapi import FastAPI, Form
import httpx

from pydantic import BaseModel


# Create a FastAPI app with authentication
fastapi_app = FastAPI(title="Secure API")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# Create a transformer function that returns a transformed ASGI app
def add_cors_middleware(app):
    # Wrap the app with CORS middleware and return the wrapped app
    return CORSMiddleware(
        app=app,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )


# Create a transformer function
def add_logging_middleware(app):
    # This is a simple example middleware that logs requests
    async def middleware(scope, receive, send):
        # Log the request path
        path = scope["path"]
        print("Request:", path)
        await app(scope, receive, send)

    return middleware


# Add a protected route
@fastapi_app.get("/api/protected")
async def protected_route(
    token: str = Depends(oauth2_scheme),
):
    return dict(message="This is a protected endpoint")


# Create a token endpoint
# @fastapi_app.post("/token")
# async def login(username: str, password: str):
#     # In a real app, you would validate credentials
#     if username == "user" and password == "password":
#         return dict(
#             access_token="example_token",
#             token_type="bearer",
#         )
#     return dict(error="Invalid credentials")


# Add routes to the FastAPI app
@fastapi_app.get("/api/items")
async def get_items():
    return dict(items=["Item1", "Item2", "Item3"])


###########################################################################


class FormData(BaseModel):
    username: str
    password: str


@fastapi_app.post("/login/")
async def login(data: Annotated[FormData, Form()]):
    print("############################3")
    print(data)
    print("############################3")
    return data


###########################################################################


class FormState(rx.State):
    form_data: dict = {}
    login_data: dict = {}

    @rx.event
    def handle_submit(self, form_data: dict):
        """Handle the form submit."""
        self.form_data = form_data

    @rx.event
    async def handle_login(self, login_data: dict):
        """Handle the form submit."""
        self.login_data = login_data
        print(login_data)
        print("wowwww")

        async with httpx.AsyncClient() as client:
            response = await client.post(
                "http://127.0.0.1:8000/login/", data=login_data
            )
            # response.raise_for_status()
            print(response.json())


def index() -> rx.Component:
    # return rx.container()
    return rx.vstack(
        rx.form(
            rx.vstack(
                rx.input(
                    placeholder="Username",
                    name="username",
                ),
                rx.input(
                    placeholder="Password",
                    name="password",
                ),
                rx.hstack(
                    rx.checkbox("Checked", name="check"),
                    rx.switch("Switched", name="switch"),
                ),
                rx.button("Submit", type="submit"),
            ),
            # on_submit=FormState.handle_submit,
            on_submit=FormState.handle_login,
            reset_on_submit=True,
        ),
        rx.divider(),
        rx.heading("Results"),
        rx.text(FormState.login_data.to_string()),
    )


app = rx.App(api_transformer=[fastapi_app, add_cors_middleware, add_logging_middleware])
app.add_page(index)
