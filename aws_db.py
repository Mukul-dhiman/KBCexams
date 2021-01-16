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
    # print("reconnecting...")
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

def ticket_generator(size, chars=string.ascii_letters + string.digits):
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



def get_contest_details(contestID):
    reconnect()
    try:
        with conn.cursor() as cur:
            sql = "select * from ContestAwardDetails where ContestID = %s order by StartRank ASC;"
            cur.execute(sql,contestID)
            data = cur.fetchall()
            return data

    except Exception as e:
        print("error in getting Contest data, error: ",e)
        return


def get_contest_pay(contestID):
    reconnect()
    try:
        with conn.cursor() as cur:
            sql = "select TicketPrice from ContestMaster where ContestID = %s"
            cur.execute(sql,contestID)
            data = cur.fetchall()
            return data

    except Exception as e:
        print("error in getting contest entry fees, error:",e)
        return "error"


def get_Current_Wallet_Balance(userid):
    reconnect()
    try:
        with conn.cursor() as cur:
            sql = "select WalletBalance from UserMaster where UserID = %s"
            cur.execute(sql,userid)
            data = cur.fetchall()
            return data

    except Exception as e:
        print("error in getting Wallet Balance, error:",e)
        return "error"


def get_ticket(contestID,UserID):
    reconnect()
    try:
        with conn.cursor() as cur:

            sql = "select WalletBalance from UserMaster where UserID = %s"
            cur.execute(sql,UserID)
            walletBallance = cur.fetchall()[0][0]

            sql ="select TicketPrice from ContestMaster where ContestID = %s"
            cur.execute(sql,contestID)
            TicketPrice = cur.fetchall()[0][0]


            if(walletBallance < TicketPrice):
                return "Money_limit"
            
            ticketid = ticket_generator(64)

            TicketState = 0

            sql = "insert into UserContestParticipationDetails (TicketID, UserID, ContestID, TicketState) value (%s,%s,%s,%s)"
            cur.execute(sql,(ticketid, UserID, contestID, TicketState))
            # if TicketState equals 0: means ticket is not used 
            # if 1: means ticket is used
            # if 2: means ticket is expired without use
            # if 3: means ticket is expired and used 
            conn.commit()

            return "complete"

    except Exception as e:
        print("error in getting ticket, error:",e)
        return "error"



def get_Current_Wallet_Balance(userid):
    reconnect()
    try:
        with conn.cursor() as cur:
            sql = "select WalletBalance from UserMaster where UserID = %s"
            cur.execute(sql,userid)
            data = cur.fetchall()
            return data

    except Exception as e:
        print("error in getting Wallet Balance, error:",e)
        return "error"

def ticket_history(UserID,contestID):
    reconnect()
    try:
        with conn.cursor() as cur:
            if contestID == "all":
                sql = "select * from UserContestParticipationDetails where UserID = %s order by CreatedDate desc"
                cur.execute(sql,UserID)
                data = cur.fetchall()
                return data

            else:
                sql = "select * from UserContestParticipationDetails where UserID = %s and ContestID = %s order by CreatedDate desc"
                cur.execute(sql,(UserID,contestID))
                data = cur.fetchall()
                return data

        
    except Exception as e:
        print("error in getting ticket history, error:",e)
        return "error"