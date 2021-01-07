import pymysql
import aws_credentials as rds
conn = pymysql.connect(
    host = rds.host,
    port = rds.port,
    user = rds.user,
    password = rds.password,
    db = rds.databasename,
)

import string
import random

def id_generator(size, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def signup(email,password):
    try:
        UserID = id_generator(64)
        with conn.cursor() as cur:
            sql = "insert into UserMaster (UserId, EmailAddress, PasswordHash) value (%s,%s,%s)"
            cur.execute(sql,(UserID, email,password))
            conn.commit()

    except Exception as e:

        print("error in sign up for email",email,"error: ",e)
