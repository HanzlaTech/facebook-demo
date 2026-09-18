from fastapi import APIRouter,Request,HTTPException
from schemas.login_schema import login_schema
from fastapi import Response
from services import user
import pymysql
from log import log
router=APIRouter()
from database import connection
from fastapi import UploadFile,File,Form
from datetime import date
from schemas.otp_schema import otp_schem
from schemas.profile_schema import profile
import os
@router.post("/signup")
async def signup(request:Request,email:str=Form(),password:str=Form(),birth:date=Form(),pic:UploadFile=File()):
 log.info(request.cookies.get("access")) 
 log.info("req recieved at signup function")
 connection.ping(reconnect=True)
 cursor=connection.cursor(pymysql.cursors.DictCursor)
 log.info("cursor is made in singup.js")
 result=await user.signup_user(cursor,email,password,birth,pic)
 connection.commit()
 log.info("func of service is called for singup")
 return result



@router.post("/login")
def login(data:login_schema,response:Response,request:Request):
 log.info(request.cookies.get("access")) 
 log.info("requst recieved at route login")
 connection.ping(reconnect=True) 
 cursor=connection.cursor(pymysql.cursors.DictCursor)
 log.info("cursor is made in login route")
 user.login_user(cursor,data.email,data.password,response)
 log.info("func of service is calleds")


@router.post("/otp")
def otp(data:otp_schem,request:Request):
  log.info(request.cookies.get("access")) 
  log.info("requst recieved at route otp")
  connection.ping(reconnect=True) 
  cursor=connection.cursor(pymysql.cursors.DictCursor)
  log.info("cursor is made in otp route")
  user.verify_otp(data.otp,cursor,data.userid)
  connection.commit()
  log.info("service otp runs completely")




@router.get("/picture")
def picture(request:Request):
  log.info(request.cookies.get("access"))
  log.info("requst recieved at route picture")
  userr=request.state.user
  use=int(userr["userid"])
  connection.ping(reconnect=True) 
  cursor=connection.cursor(pymysql.cursors.DictCursor)
  log.info("cursor is made in profile route")
  result=user.profile(use,cursor)
  return result


@router.post("/post")
async def post(request:Request,pic:UploadFile=File()):
    log.info("request recieved at add post router")
    connection.ping(reconnect=True) 
    cursor=connection.cursor(pymysql.cursors.DictCursor)
    log.info("cursor connection occur in add post router")
    userr=request.state.user
    use=int(userr["userid"])
    await user.post(pic,cursor,use)
    connection.commit()
    log.info("service function for add post runs")


import base64
@router.get("/show_post")
def show_post(request:Request):
      log.info("request recieved at show post router")
      connection.ping(reconnect=True)
      cursor=connection.cursor(pymysql.cursors.DictCursor)
      log.info("cursor connection occur in show post router")
      use=request.state.user
      use=int(use["userid"])
      images=user.show_post(cursor,use)
      log.info("service function for show post runs")
      if images:
       for image in images:
         image["image_url"]=base64.b64encode(image["image_url"]).decode("utf-8")
       return images
      else:
        raise HTTPException(
          status_code=200,
          detail="no pic"
        )


@router.get("/user_post")
def user_post(request:Request):
        log.info("request recieved at user post router")
        connection.ping(reconnect=True)
        cursor=connection.cursor(pymysql.cursors.DictCursor)
        log.info("cursor connection occur in user post router")
        use=request.state.user
        use=int(use["userid"])
        images=user.user_post(cursor,use)
        for image in images:
           image["image_url"]=base64.b64encode(image["image_url"]).decode("utf-8")
        return images   
