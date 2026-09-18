import pymysql
import jwt
import os
from dotenv import load_dotenv
from fastapi import Response
from log import log
import os
from PIL import Image
from io import BytesIO
from fastapi import UploadFile,File,Form
from email_validator import EmailNotValidError,validate_email
import smtplib
from email.message import EmailMessage
import secrets
import uuid
from fastapi.staticfiles import StaticFiles
from datetime import date
import jwt
from datetime import datetime, timedelta
from fastapi import HTTPException,status
load_dotenv()

secret=os.environ["Secret"]
algorithm="HS256"
def login_user(cursor:pymysql.cursors.DictCursor,email:str,password:str,response:Response):
    log.info("request recieced at service login func")
    cursor.execute("Select * from user where email=%s and Verified=%s and password=%s",(email,True,password))
    user=cursor.fetchone()
    log.info("db query run in service login")
    
    if user is not None:
        log.info("user exist")
        payload={
            "userid":user["Userid"],
            "exp":datetime.now()+timedelta(minutes=10)
        }
        log.info("paylaod is made i serive login")
        access=jwt.encode(
           payload,
           secret,
           algorithm=algorithm
        )
        log.info("jwt accss is ade in servie login")

        response.set_cookie(
            key="access",
            value=access,
            httponly=True,
            secure=False,
            samesite="lax",
            path="/",
            max_age=10*60
            )
        pay={
           "userid":user["Userid"],
           "exp":datetime.now()+timedelta(days=7)
        }
        refresh=jwt.encode(
           pay,
           secret,
           algorithm=algorithm
        )
        response.set_cookie(
                      key="refresh",
                      value=refresh,
                      httponly=True,
                      secure=False,
                      samesite="lax",
                      path="/refresh",
                      max_age=7*24*60*60
                      )
        
        log.info("cookis is made in login service")
          
        
    else:
           raise HTTPException(
              status_code=500,
              detail="user dont exist"
           )

async def signup_user(cursor:pymysql.cursors.DictCursor,email:str,password:str,birth:date,pic:UploadFile):
    extension=""
    log.info("req recieved at sevice singp")
    data=await pic.read()
    validate=validate_email(email)  
    if not validate:
#   invalid format
     pass
    log.info("email is valid")
   
    if pic.filename is not None:
       extension=os.path.splitext(pic.filename)[1]
       
       if len(data)>5 *1024*1024:
        #   greater size
         log.info("data is less than 5mb")
       elif extension.lower() not in  [".jpg",".png",".jpeg"]:
        #    diff extension
         log.info("extnesion is incorrect")
         
       elif pic.content_type not in  ["image/jpg","image/jpeg","image/png"]:
        # diff content type
        log.info("content type is incorrect")
         

       elif True:
        try:
           image=Image.open(BytesIO(data))
           image.verify()
           log.info("image is verified")
        
        except:
           pass
        try:
         image=Image.open(BytesIO(data))
         width,height=image.size
         if width>4000 or height >4000 :
              log.info("dimensiions is greater")
              pass 
        except:
           pass
    filen=str(uuid.uuid4())
    filename=filen+extension
    file=open("upload/"+filename,"wb")
    file.write(data)
    file.close()
    log.info("file is saved")
   
    try:
        cursor.execute("Insert into user (Email,Password,Verified,image,Gender,BirthDate)values(%s,%s,%s,%s,%s,%s)",(email,password,False,filename,"Male",birth))
        cursor.execute("select *from user where Email=%s",email)
        use=cursor.fetchone()
        log.info("db query is execute")
        otp=secrets.randbelow(1000000)
        otp=f"{otp:06d}"    
        app_password="rclp kxtu acbk emvf"
        msg=EmailMessage()
        sender="hafeezhanzla24@gmail.com"
        reciever=email
        msg["From"]=sender
        msg["To"]=reciever
        msg["Subject"]="Your OTP"
        log.info("ms subject is set ")
        msg.set_content("your otp is "+otp)

        server=smtplib.SMTP("smtp.gmail.com",586)
        server.starttls()
        server.login(sender,app_password)
        server.send_message(msg)
        server.quit()
        log.info("otp is send")
        if use is not None:
         cursor.execute("insert into otp (userid,otp)values(%s,%s)",(use["Userid"],otp))
         return use["Userid"]
    except Exception as e:
       log.info(type(e).__name__)

    raise HTTPException(
       status_code=200,detail="correct"
    )


# this is demo branch commit
def verify_otp(otp:str,cursor:pymysql.cursors.DictCursor,userid:int):
   log.info("req recieved at servie otp")
   cursor.execute("select * from otp where userid=%s",(userid))
   log.info("db query excute")
   user=cursor.fetchone()
   if user is not None:
    log.info("user exist of that userid")
    ot=str(user["otp"])
    if otp==ot:
      log.info("otp verified")
      cursor.execute("update user set verified=%s where userid=%s",(True,user["userid"]))
      
    else:
      log.info("invalid otp")
      raise HTTPException(
         status_code=500,
         detail="incorrect otp"
      )
         
def profile(userid:int,cursor:pymysql.cursors.DictCursor):
 log.info("requst recv at service profiel")
 cursor.execute("select * from user where userid=%s",(userid,))
 log.info("db query execute")

 user=cursor.fetchone()
 if user is not None:
    log.info("user exist")
    return user["image"]




async def post(pic:UploadFile,cursor:pymysql.cursors.DictCursor,userid:int):
  log.info("request recieved at add post service")
  data=await pic.read()
  log.info("pic data is read")
  if pic.filename is not None:
    log.info("pic filename is not none")
    extension=os.path.splitext(pic.filename)[1]
    if extension.lower() not in [".jpg",".jpeg",".png",".gif"]:
      log.info("extension dont match")
      raise HTTPException(
        status_code=500,
        detail="extension dont match"
      )
    elif len(data)>=10*1024*1024:
       log.info("file size exceeds")
       raise HTTPException(
              status_code=500,
              detail="greater size"
            )
    elif pic.content_type not in ["image/jpg","image/png","image/jpeg","image/gif",]:
       log.info("content_type dont match")
       raise HTTPException(
                    status_code=500,
                    detail="content type is not image"
                  )
    elif True:
     try:
      image=Image.open(BytesIO(data))
      image.verify()
      log.info("image is verified")
     except:
         raise HTTPException(
              status_code=500,
              detail="image dont verify"
            )
     width,height=image.size
     if width>4000 or height >4000:
         raise HTTPException(
              status_code=500,
              detail="greater dimension"
            )

     cursor.execute("insert into photos(userid,image_url,image_type)values(%s,%s,%s)",(userid,data,pic.content_type))
     log.info("photo is saved in photos table")



def show_post(cursor:pymysql.cursors.DictCursor,userid:int):
   log.info("request recieved at show post service")
   
   cursor.execute("select image_url,image_type from photos where not userid =%s",userid)
   log.info("cursor execute")
   images=cursor.fetchall()
   log.info("fetch all")
   log.info("return images")
   return images



def user_post(cursor:pymysql.cursors.DictCursor,userid:int):
   log.info("request recieved at user post service")
   
   cursor.execute("select image_url,image_type from photos where userid =%s",userid)
   log.info("cursor execute")
   images=cursor.fetchall()
   log.info("fetch all")
   log.info("return images")
   return images