import pymysql
import aws_credentials as rds
conn = pymysql.connect(
    host = rds.host,
    port = rds.port,
    user = rds.user,
    password = rds.password,
    db = rds.databasename,
)

def test_show():
    cur=conn.cursor()
    cur.execute("select * from vehicle")
    details = cur.fetchall()
    return details