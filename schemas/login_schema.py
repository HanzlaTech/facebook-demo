from pydantic import BaseModel


class login_schema (BaseModel):
    email:str
    password:str


    