from flask import request, make_response, jsonify, Response, redirect
from nawalcube.common import error_logics as errhand

import psycopg2
import psycopg2.extras

ENV = 1
# 0 - DEV
# 1- HEROKU
# 2 - UAT
# 3 - PROD
CON_STR = ["host='127.0.0.1' dbname='postgres' user='postgres' password='password123'",
            #"host='tantor.db.elephantsql.com' dbname='vizbcyai' user='vizbcyai' password='wtN1QNGIjImJTUIEc7h14oi72C7jXoAt'",
            "host='ec2-174-129-29-101.compute-1.amazonaws.com' dbname='de2hh491m8g59e' user='lcnqgjowljqhyr' password='7009ce19c17429fae7aaaabb3e7290a6a5fb60c5c5ef1910f6eef3289371aca6'",
            "",
            "host='nawalcube.c5eo06dso01d.ap-south-1.rds.amazonaws.com' dbname='nawalcube' user='nawalcube' password='dddd!'"
          ]

def mydbfunc(con,cur,command):
    s = 0
    f = None
    t = None
    
    try:
        cur.execute(command)
    except psycopg2.Error as e:
        print(e)
        """
        print(type(e))
        print(e.diag)
        print(e.args)
        print(e.cursor)
        print(e.pgcode)
        print(e.pgerror)
        myerror= {'natstatus':'error','statusdetails':''}
        """
        s, f, t = errhand.get_status(s, 200, f, e.pgcode + e.pgerror, t , "no")
    except psycopg2.Warning as e:
        print(e)
        #myerror={'natstatus':'warning','statusdetails':''}
        #myerror = {'natstatus':'warning','statusdetails':e}
        s, f = errhand.get_status(s, -100, f, e.pgcode + e.pgerror, t , "no")
    finally:
        if s > 0:    
            con.rollback()
            cur.close()
            con.close()
    return cur, s, f

def mydbopncon():
    s = 0
    f = None
    t = None
    try:
        con
    except NameError:
        print("con not defined so assigning as null")
        #conn_string = "host='localhost' dbname='postgres' user='postgres' password='password123'"
        #conn_string = "host='nawalcube.c5eo06dso01d.ap-south-1.rds.amazonaws.com' dbname='nawalcube' user='nawalcube' password='Nirudhi1!'"
        conn_string = CON_STR[ENV]
        print('after conn string')
        try:
            print('preparing con')
            con=psycopg2.connect(conn_string)
        except Exception as e:
            print("unable to connect")
            print(e)
        finally:
            print("unable to connect finally")
        print('con')
        print(con)
        cur = con.cursor(cursor_factory=psycopg2.extras.DictCursor)
        print('cur')
        print(cur)
    else:            
        if con.closed:
            #conn_string = "host='localhost' dbname='postgres' user='postgres' password='password123'"
            #conn_string = "host='nawalcube.c5eo06dso01d.ap-south-1.rds.amazonaws.com' dbname='nawalcube' user='nawalcube' password='Nirudhi1!'"
            conn_string = CON_STR[ENV]
            try:
                print('preparing con')
                con = psycopg2.connect(conn_string)
            except Exception as e:
                print("unable to connect")
                print(e)
            else:
                cur = con.cursor(cursor_factory=psycopg2.extras.DictCursor)
    print('connection successful')
    return con,cur, s, f

def mydbcloseall(con,cur):
#close cursor and connection before exit
    try:
        con
    except NameError:
        print("No active connection to close")
    else:
        con.commit()
        cur.close()
        con.close()

def mydbbegin(con,cur):
    s = 0
    f = None
    t = None
    command = cur.mogrify("BEGIN;")
    cur, s, f = mydbfunc(con,cur,command)
    
    if cur.closed == True:
        s, f, t = errhand.get_status(s, 200, f, "BEGIN statement execution failed", t , "no")
    else:
        print("BEGIN statment execution successful")
    
    return s, f 