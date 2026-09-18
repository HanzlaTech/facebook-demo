import pymysql

import os
from dotenv import load_dotenv
load_dotenv()

connection=pymysql.connect(
    host=os.environ["host"],
    user=os.environ["user"],
    password=os.environ["password"],
    database=os.environ["database"],
    port=int(os.environ["port"])
)


