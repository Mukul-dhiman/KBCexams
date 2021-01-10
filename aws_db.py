import pymysql
import aws_credentials as rds
conn = pymysql.connect(
    host = rds.host,
    port = rds.port,
    user = rds.user,
    password = rds.password,
    db = rds.databasename,
)

def reconnect():
    print("reconnecting...")
    try:
        conn = pymysql.connect(
            host = rds.host,
            port = rds.port,
            user = rds.user,
            password = rds.password,
            db = rds.databasename,
        )
    except Exception as e:
        print("error in reconnecting to database, error: ",str(e))

import string
import random

def id_generator(size, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def signup(email,password):
    reconnect()
    try:
        UserID = id_generator(64)
        with conn.cursor() as cur:
            sql = "insert into UserMaster (UserId, EmailAddress, PasswordHash) value (%s,%s,%s)"
            cur.execute(sql,(UserID, email,password))
            conn.commit()

    except Exception as e:
        print("error in sign up for email",email,"error: ",e)

def login(email,password):
    reconnect()
    try:
        with conn.cursor() as cur:
            sql = "select UserId, Name, PasswordHash, WalletBalance, CreateDate from UserMaster where EmailAddress=%s"
            cur.execute(sql,(email))
            data = cur.fetchall()

            if(password == data[0][2]):
                return {'correct': "correct","UserID": data[0][0], "Name": data[0][1], "WalletBallance": data[0][3], "CreatedDate": data[0][4]}
            else:
                return {'correct': "wrong"}


    except Exception as e:
        print("error in loging-in for email",email,"error: ",str(e))
        return {'correct': "wrong"}


def UserExist(email):
    reconnect()
    try:
        with conn.cursor() as cur:
            sql = "select exists(select * from UserMaster where EmailAddress=%s)"
            cur.execute(sql,(email))
            exist = cur.fetchall()

            return exist[0][0]


    except Exception as e:
        print("error in UserExist API for email",email,"error: ",str(e))
        return 0


def change_password(email,password):
    reconnect()
    try:
        with conn.cursor() as cur:
            sql = "update UserMaster set PasswordHash = %s where EmailAddress=%s"
            cur.execute(sql,(password, email))
            conn.commit()


    except Exception as e:
        print("error in change_password API for email",email,"error: ",str(e))
        return 0


def contestList():
    reconnect()
    try:
        with conn.cursor() as cur:
            sql = "select * from ContestMaster where date(CompletionDate) > date(now());"
            cur.execute(sql)
            data = cur.fetchall()
            return data

    except Exception as e:
        print("error in Listing Contest error: ",e)
        return