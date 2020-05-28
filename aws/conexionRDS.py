import sys
import logging
import pymysql

rds_host = "database-1.cz9eknblo0yl.eu-west-2.rds.amazonaws.com"

username = "admin"
password ="12345678"
dbname = "pruebaRDS"

try:
    conn = pymysql.connect(rds_host, user=username, passwd=password, db=dbname, connect_timeout=10)
except pymysql.MySQLError as e:
    print (e)
    sys.exit()
    
def lambda_handler(event , context):
    try:
        with conn.cursor() as cur:
            #cur.execute("create table tableRDS2 ( name varchar(20) NOT NULL ,  lastname varchar(20) NOT NULL )")
            #cur.execute(event['query'])
            #cur.execute("insert into tableRDS values ( 'a',2)")
            conn.commit()
            #cur.execute("select * from tableRDS")
            #cur.execute(event['query'])
            cur.execute("insert into tableRDS values ('" + event['name'] +             "','" +event['lastname']+"')")
            conn.commit()
            for row in cur:
                print(row)
    except pymysql.MySQLError as e:    
        print (e)
        sys.exit()
    
    print ("executed!")
    return ""

