from fastapi import FastAPI

server = FastAPI()


@server.get("/")
async def root():
    return {"message": "Hello World"}


@server.get("/home")
async def home():
    return {"message": "Hello Home"}
