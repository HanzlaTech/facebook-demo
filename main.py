from fastapi import FastAPI
from fastapi import HTTPException,staticfiles,status,Request,Response
from routes.user import router as user_router
from log import log
from fastapi.staticfiles import StaticFiles
import jwt
from datetime import datetime,timedelta
import os
from dotenv import load_dotenv
load_dotenv()
app=FastAPI()
from fastapi.responses import JSONResponse

app.mount("/uploads",StaticFiles(directory="upload"),name="uploads")
app.include_router(user_router)

log.info("include user router")

from fastapi.middleware.cors import CORSMiddleware



@app.middleware("http")
async def middleware(request:Request,call_next):
   log.info("requeset recv at middleware")
   try:
    access=request.cookies.get("access")
    if request.url.path in ["/login","/signup","/otp","/refresh"]:
      log.info("url in list path")
      result= await call_next(request)
      return result
    if access is not None:
     log.info("request is not none")
    
     data=jwt.decode(
       access,
       os.environ["Secret"],
       algorithms= [os.environ["algorithm"]]
    )
     request.state.user={
        "userid":data["userid"]
      }
     log.info("request state user ")
     result=await call_next(request)
     return result
    else:
         log.info("token is none")
         return JSONResponse(
           status_code=401,
           content={"msg":"error occur"}
         )
   except jwt.ExpiredSignatureError:
      log.info("token is expired")
      return JSONResponse(
                status_code=401,
                content={"msg":"error occur"}
              )
   except jwt.InvalidTokenError:
       log.info("token is changed")  
       return JSONResponse(
                  status_code=401,
                  content={"msg":"error occur"}
                )
   

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/refresh")
def refresh(request:Request,response:Response):
   refresh=request.cookies.get("refresh")
   if refresh is not None:
     
    data=jwt.decode(
     refresh,
     os.environ["Secret"],
     algorithms=[os.environ["algorithm"]]
   )
    if data is not None:
     payload={
      "userid":data["userid"],
      "exp":datetime.now()+timedelta(minutes=10)
   }
     access=jwt.encode(
      payload,
       os.environ["Secret"],
      algorithm=os.environ["algorithm"]
   )

     response.set_cookie(
      key="access",
      value=access,
      httponly=True,
      secure=False,
      samesite="lax",
      path="/",
      max_age=10*60
   )

    refresh_payload={
       "userid":data["userid"],
            "exp":datetime.now()+timedelta(days=7)
         }
    
    refresh=jwt.encode(
       refresh_payload,
        os.environ["Secret"],
       algorithm=os.environ["algorithm"]
     )
    if refresh is not None:
     response.set_cookie(
       key="refresh",
       value=refresh,
       httponly=True,
       secure=False,
       samesite="lax",
       path="/refresh",
       max_age=7*24*60*60
     )



