import mysql.connector, asyncio
from colorama import Fore

HOST = ""
USER = ""
PASSWORD = ""
DATABASE_NAME = ""

db_connection = mysql.connector.connect(host=HOST, user=USER, password=PASSWORD, database=DATABASE_NAME)

def SETUP(guild_id: str, logs=None):
    global db_connection
    cursor = db_connection.cursor()
    query  = "INSERT INTO protect (guild_id, logs) VALUES ('%s', '%s')"
    cursor.execute(query, (guild_id, logs))
    db_connection.commit()
    cursor.close()

def ELOGS(guild_id: str, logs_id: str):
    global db_connection
    cursor = db_connection.cursor()
    query = "UPDATE protect SET logs='%s' WHERE guild_id='%s'"
    cursor.execute(query, (logs_id, guild_id))
    db_connection.commit()
    return "success"

def INSERT(guild_id: str, table: str, objet: str, value):
    global db_connection
    cursor = db_connection.cursor()
    query  = f"INSERT INTO {table} (guild_id, {objet})" + " VALUES ('%s', '%s')"
    cursor.execute(query, (guild_id, value))
    db_connection.commit()
    cursor.close()

def UPDATE(guild_id: str, table: str, objet: str, value):
    global db_connection
    cursor = db_connection.cursor()
    query = f"UPDATE {table} SET {objet}" + "='%s' WHERE guild_id='%s'"
    cursor.execute(query, (value, guild_id))
    db_connection.commit()

def GET(guild_id: str, table: str, objet: str):
    global db_connection
    cursor = db_connection.cursor()

    if objet == "logs":
        query = "SELECT logs FROM protect WHERE guild_id='%s'"
        cursor.execute(query, (guild_id,))
    else:
        query  = f"SELECT {objet} FROM {table}" + " WHERE guild_id='%s'"
        cursor.execute(query, (guild_id,))

    content = [row[0] for row in cursor.fetchall()]
    cursor.close()
    return content

def REMOVE(table: str, guild_id: str):
    global db_connection
    cursor = db_connection.cursor()
    query = f"DELETE FROM {table}" + " WHERE guild_id='%s'"
    cursor.execute(query, (guild_id,))
    db_connection.commit()

def get(bot: str):
    if bot == "ebot":
        return ''
    
async def dbc_update():
    while True:
        global db_connection
        if db_connection.is_connected() == False:
            print(Fore.YELLOW + f"\nReconnection à la base de donnée.." + Fore.RESET)
            try:
                db_connection = mysql.connector.connect(host=HOST, user=USER, password=PASSWORD, database=DATABASE_NAME)
            except:
                print(Fore.RED + f"\nTentative reconnection à la base de donnée échoué." + Fore.RESET)
        await asyncio.sleep(60)