from contextlib import asynccontextmanager
from rich import print
from fastapi import FastAPI


@asynccontextmanager
async def lifespan_handler(app: FastAPI):
    print("Server started...", border_style="green")
    yield
    print("...stopped!!!", border_style="red")


app = FastAPI(lifespan=lifespan_handler)


@app.get("/")
def read_the_root():
    return {"detail": "server is running..."}
