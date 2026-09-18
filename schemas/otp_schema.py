from pydantic import BaseModel

class otp_schem(BaseModel):
    otp:str
    userid:int