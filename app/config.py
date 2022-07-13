from hashlib import algorithms_available
from pydantic import BaseSettings
import os
from pathlib import Path
from dotenv import load_dotenv
import dotenv

#the enviroment variable is assinged only after typing load_dotenv() in the code 
load_dotenv()

class Settings(BaseSettings):
    database_hostname: str 
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    
    class Config():
        env_file = ".env"
    
    
    
settings = Settings()