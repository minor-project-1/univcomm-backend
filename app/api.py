from fastapi import FastAPI, Body, HTTPException
from fastapi.encoders import jsonable_encoder



app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}