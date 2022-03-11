import psycopg2
from psycopg2 import Error
import os

# Connect to an existing database
db_user = os.environ.get("DB_USER")
db_pw = os.environ.get("DB_PW")
db_host = os.environ.get("DB_HOST")
db_port = os.environ.get("DB_PORT")
db_name = os.environ.get("DB_NAME")
def conn():
    connection = psycopg2.connect(
                                user=db_user,
                                password=db_pw,
                                host=db_host,
                                port=db_port,
                                database=db_name
                                )
    return connection
def createT():
    con = conn()
    cur = con.cursor()
    create_table = """
                    CREATE TABLE logs
                    (DATE    TEXT    PRIMARY KEY    NOT NULL,
                    LOG    JSONB    NOT NULL);
                    """
    cur.execute(create_table)
    con.commit()
    cur.close()
    con.close()
    return True



async def insert(t_date,e_log):
    con = conn()
    cur = con.cursor()
    insert_query = """ 
                    INSERT INTO logs (DATE,LOG) 
                    VALUES (%s,%s)
                    """
    cur.execute(insert_query,(t_date,e_log,))
    con.commit()
    cur.close()
    #await ctx.send("logs saved !!")

async def update(t_date,e_log,ctx):
    con = conn()
    cur = con.cursor()
    update_query = """Update logs set log = %s where date = %s """


    cur.execute(update_query,(e_log,t_date,))
    con.commit()
    cur.close()
    await ctx.send("records initialized !!")


def retrieve(t_date):
    con = conn()
    cur = con.cursor()
    retrieve_query= """
                    SELECT log 
                    FROM logs 
                    WHERE date = %s 
                    """
    cur.execute(retrieve_query,(t_date,))
    row = cur.fetchone()
    while row is not None:
        log = row
        row = cur.fetchone()
    con.commit()
    cur.close()
    return dict(log[0])

