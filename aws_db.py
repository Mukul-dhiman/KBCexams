import pymysql
import aws_credentials as rds




import string
import random
import datetime

def id_generator(size, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def ticket_generator(size, chars=string.ascii_letters + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def signup(email,password):
    conn = pymysql.connect(
        host = rds.host,
        port = rds.port,
        user = rds.user,
        password = rds.password,
        db = rds.databasename,
    )
    try:
        UserID = id_generator(64)
        with conn.cursor() as cur:
            sql = "insert into UserMaster (UserId, Name, EmailAddress, PasswordHash) value (%s,%s,%s,%s)"
            name=email.split("@")[0]
            cur.execute(sql,(UserID, name, email,password))
            conn.commit()

    except Exception as e:
        print("error in sign up for email",email,"error: ",e)

def login(email,password):
    conn = pymysql.connect(
        host = rds.host,
        port = rds.port,
        user = rds.user,
        password = rds.password,
        db = rds.databasename,
    )
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
    conn = pymysql.connect(
        host = rds.host,
        port = rds.port,
        user = rds.user,
        password = rds.password,
        db = rds.databasename,
    )
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
    conn = pymysql.connect(
        host = rds.host,
        port = rds.port,
        user = rds.user,
        password = rds.password,
        db = rds.databasename,
    )
    try:
        with conn.cursor() as cur:
            sql = "update UserMaster set PasswordHash = %s where EmailAddress=%s"
            cur.execute(sql,(password, email))
            conn.commit()


    except Exception as e:
        print("error in change_password API for email",email,"error: ",str(e))
        return 0


def contestList():
    conn = pymysql.connect(
        host = rds.host,
        port = rds.port,
        user = rds.user,
        password = rds.password,
        db = rds.databasename,
    )
    try:
        with conn.cursor() as cur:
            sql = "select * from ContestMaster where date(CompletionDate) > date(now());"
            cur.execute(sql)
            data = cur.fetchall()
            return data

    except Exception as e:
        print("error in Listing Contest error: ",str(e))
        return



def get_contest_details(contestID):
    conn = pymysql.connect(
        host = rds.host,
        port = rds.port,
        user = rds.user,
        password = rds.password,
        db = rds.databasename,
    )
    try:
        with conn.cursor() as cur:
            sql = "select * from ContestAwardDetails where ContestID = %s order by StartRank ASC;"
            cur.execute(sql,contestID)
            data = cur.fetchall()
            return data

    except Exception as e:
        print("error in getting Contest data, error: ",e)
        return "error"


def get_contest_pay(contestID):
    conn = pymysql.connect(
        host = rds.host,
        port = rds.port,
        user = rds.user,
        password = rds.password,
        db = rds.databasename,
    )
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
    conn = pymysql.connect(
        host = rds.host,
        port = rds.port,
        user = rds.user,
        password = rds.password,
        db = rds.databasename,
    )
    try:
        with conn.cursor() as cur:
            sql = "select WalletBalance from UserMaster where UserID = %s"
            cur.execute(sql,userid)
            data = cur.fetchall()
            return data

    except Exception as e:
        print("error in getting Wallet Balance, error:",e)
        return "error"


def isspotsLeft(contestID):
    conn = pymysql.connect(
        host = rds.host,
        port = rds.port,
        user = rds.user,
        password = rds.password,
        db = rds.databasename,
    )
    try:
        with conn.cursor() as cur:
            sql = "select SpotsLeft from ContestMaster where contestID = %s"
            cur.execute(sql,contestID)
            data = cur.fetchone()
            if(data[0]>0):
                return True
            return False

    except Exception as e:
        print("error in checking Spots lefts, error:",e)
        return "error"




def get_ticket(contestID,UserID):
    conn = pymysql.connect(
        host = rds.host,
        port = rds.port,
        user = rds.user,
        password = rds.password,
        db = rds.databasename,
    )
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


            return ticketid

    except Exception as e:
        print("error in getting ticket, error:",e)
        return "error"



def get_Current_Wallet_Balance(userid):
    conn = pymysql.connect(
        host = rds.host,
        port = rds.port,
        user = rds.user,
        password = rds.password,
        db = rds.databasename,
    )
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
    conn = pymysql.connect(
        host = rds.host,
        port = rds.port,
        user = rds.user,
        password = rds.password,
        db = rds.databasename,
    )
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





def ticket_state(ticketID):
    conn = pymysql.connect(
        host = rds.host,
        port = rds.port,
        user = rds.user,
        password = rds.password,
        db = rds.databasename,
    )
    try:
        with conn.cursor() as cur:
            sql = "select TicketState from UserContestParticipationDetails where TicketID = %s"
            cur.execute(sql,ticketID)
            data = cur.fetchone()
            return data[0]

    except Exception as e:
        print("error in getting ticket State, error:",e)
        return "error"


def ticket_start_time(ticketID):
    conn = pymysql.connect(
        host = rds.host,
        port = rds.port,
        user = rds.user,
        password = rds.password,
        db = rds.databasename,
    )
    try:
        with conn.cursor() as cur:
            sql = "select TestStartDate from UserContestParticipationDetails where TicketID = %s"
            cur.execute(sql,ticketID)
            data = cur.fetchone()
            return data[0]

    except Exception as e:
        print("error in getting ticket Start date, error:",e)
        return "error"


def ticket_info(ticketID):
    conn = pymysql.connect(
        host = rds.host,
        port = rds.port,
        user = rds.user,
        password = rds.password,
        db = rds.databasename,
    )
    try:
        with conn.cursor() as cur:
            sql = "select * from UserContestParticipationDetails where TicketID = %s"
            cur.execute(sql,ticketID)
            data = cur.fetchone()
            return data

    except Exception as e:
        print("error in getting ticket info, error:",e)
        return "error"



question_map={}


def get_random_questions(ticketid):
    if ticketid in question_map:
        return question_map[ticketid]


    conn = pymysql.connect(
        host = rds.host,
        port = rds.port,
        user = rds.user,
        password = rds.password,
        db = rds.databasename,
    )
    try:
        with conn.cursor() as cur:
            sql = "select QuestionID, QuestionDescription, Option1, Option2, Option3, Option4 from QuestionBank order by rand() limit 10;"
            cur.execute(sql)
            data = cur.fetchall()
            question_map[ticketid]=data
            return data

    except Exception as e:
        print("error in getting questions, error:",e)
        return "error"

def use_ticket(startdate, ticketid):
    conn = pymysql.connect(
        host = rds.host,
        port = rds.port,
        user = rds.user,
        password = rds.password,
        db = rds.databasename,
    )
    try:
        with conn.cursor() as cur:
            sql = "update UserContestParticipationDetails set TestStartDate = %s where TicketID=%s"
            cur.execute(sql,(startdate, ticketid))
            conn.commit()


            return "done"

    except Exception as e:
        print("error in useing ticket, error: ",str(e))
        return "error"



def finish_ticket(starttime, ticketid, q_response_dic):
    conn = pymysql.connect(
        host = rds.host,
        port = rds.port,
        user = rds.user,
        password = rds.password,
        db = rds.databasename,
    )
    total = len(q_response_dic)
    marks_obtain = 0

    for key,value in q_response_dic.items():
        check = iscorrect(key,value)
        if(check=="error"):
            return "error"
        elif(check==1):
            marks_obtain+=1

    state = ticket_state(ticketid)

    if(state=="error"):
        return "error"
    elif(state==0):
        state=1
    

    try:
        with conn.cursor() as cur:
            sql = "update UserContestParticipationDetails set ObtainedScore = %s, MaximumScore =%s, TestSubmitDate = %s,TicketState = %s  where TicketID=%s"
            cur.execute(sql,(marks_obtain, total, starttime, state, ticketid))
            conn.commit()


            return "done"

    except Exception as e:
        print("error in finish ticket, error: ",str(e))
        return "error"




def iscorrect(questionID, response):
    conn = pymysql.connect(
        host = rds.host,
        port = rds.port,
        user = rds.user,
        password = rds.password,
        db = rds.databasename,
    )
    try:
        with conn.cursor() as cur:
            sql = "select CorrectOption from QuestionBank where QuestionID=%s"
            cur.execute(sql,questionID)
            correct_option = cur.fetchone()
            if(correct_option[0] == response):
                return 1
            else:
                return 0

    except Exception as e:
        print("error in checking question correctness, error: ",str(e))
        return "error"



def CreateContest(ContestID, CompletionDate, TicketPrice, TotalSpots):
    conn = pymysql.connect(
        host = rds.host,
        port = rds.port,
        user = rds.user,
        password = rds.password,
        db = rds.databasename,
    )
    try:
        with conn.cursor() as cur:
            sql = "Insert into ContestMaster (ContestID, CompletionDate, TicketPrice, TotalSpots, SpotsLeft) value ('"+ContestID+"','"+CompletionDate+"',"+TicketPrice+","+TotalSpots+","+TotalSpots+")"
            cur.execute(sql)
            conn.commit()

    except Exception as e:
        print("error in Creating Contest, error: ",str(e))
        return "error"


def create_event(ContestID, CompletionDate):
    conn = pymysql.connect(
        host = rds.host,
        port = rds.port,
        user = rds.user,
        password = rds.password,
        db = rds.databasename,
    )
    try:
        with conn.cursor() as cur:
            event_name = "event_"+str(ContestID)
            sql = "create event " + event_name +" ON SCHEDULE AT '" + CompletionDate +"' DO update UserContestParticipationDetails set TicketState = TicketState + 2 where ContestID = %s"
            cur.execute(sql,ContestID)
            conn.commit()

    except Exception as e:
        print("error in Creating Contest end event, error: ",str(e))
        return "error"



def get_all_contest():
    conn = pymysql.connect(
        host = rds.host,
        port = rds.port,
        user = rds.user,
        password = rds.password,
        db = rds.databasename,
    )
    try:
        with conn.cursor() as cur:
            sql = "select * from ContestMaster"
            cur.execute(sql)
            return cur.fetchall()

    except Exception as e:
        print("error in getting all Contest, error: ",str(e))
        return "error"


def add_contest_details(StartRank, EndRank, Prize,contestid):
    conn = pymysql.connect(
        host = rds.host,
        port = rds.port,
        user = rds.user,
        password = rds.password,
        db = rds.databasename,
    )
    try:
        with conn.cursor() as cur:
            sql = "insert into ContestAwardDetails (ContestID, StartRank, EndRank, AwardAmount) values ('"+contestid+"','"+StartRank+"','"+EndRank+"','"+Prize+"')"
            cur.execute(sql)
            conn.commit()

    except Exception as e:
        print("error in adding Contest details, error: ",str(e))
        return "error"


def delete_contest_details(StartRank, EndRank, contestid):
    conn = pymysql.connect(
        host = rds.host,
        port = rds.port,
        user = rds.user,
        password = rds.password,
        db = rds.databasename,
    )
    try:
        with conn.cursor() as cur:
            sql = "delete from ContestAwardDetails where StartRank ="+StartRank+" and EndRank = "+EndRank+" and ContestID = '"+contestid+"'"
            cur.execute(sql)
            conn.commit()

    except Exception as e:
        print("error in deleting Contest details, error: ",str(e))
        return "error"