import sqlite3
from collections import namedtuple


def createUser(user_id):
    with sqlite3.connect("instagramBotDataBase.db") as connection:
        cursor = connection.cursor()
        # cursor.execute("DROP TABLE `User`;")
        cursor.execute("CREATE TABLE IF NOT EXISTS `User`(token TEXT, user_id TEXT NOT NULL PRIMARY KEY);")
        cursor.execute("INSERT INTO `User` (user_id) VALUES ('{0}');".format(user_id))
        connection.commit()

        result = cursor.execute("SELECT * FROM `User`;")
        for item in result:
            print(item)


def getUser(userid):
    try:
        with sqlite3.connect("instagramBotDataBase.db") as connection:
            cursor = connection.cursor()
            result = cursor.execute("SELECT * FROM `User` WHERE user_id = '{0}';".format(userid)).fetchone()

        return namedtuple('User', ['token', 'id'])(result[0], result[1])
    except Exception as e:
        print(f"getUser except: {e}")
        return None


def updateToken(token, userid):
    with sqlite3.connect("instagramBotDataBase.db") as connection:
        cursor = connection.cursor()
        cursor.execute("UPDATE `User` SET token = '{0}' WHERE user_id = '{1}'".format(token, userid))
        connection.commit()

        result = cursor.execute("SELECT * FROM `User`;")
        for item in result:
            print(item)
