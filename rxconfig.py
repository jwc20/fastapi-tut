import reflex as rx

config = rx.Config(
    app_name="fastapi_tut",
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
    ],
)