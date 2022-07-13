import sys
import os
import uvicorn
from pathlib import Path
import os.path
import sys
from mimetypes import init
from msilib.schema import Error
from fastapi.middleware.cors import CORSMiddleware
from pyexpat import model
from turtle import title
from xmlrpc.client import boolean
from fastapi import FastAPI, Response, status, HTTPException, Depends
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import  models
from database import engine 
from routers import post, user, auth, vote
from pydantic import BaseSettings
from config import Settings



# models.Base.metadata.create_all(bind=engine)


app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router) 
app.include_router(user.router) 
app.include_router(auth.router)
app.include_router(vote.router)

 
# requests Get method url: "/"
@app.get("/")
def root():
    return {"messages": "Hello World test api"}

    
