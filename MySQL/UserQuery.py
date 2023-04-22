import pymysql

from PrivateConfig import PASSWORD_DATABASE, DATABASE_NAME, USER_DATABASE, HOST_DATABASE


def connect_db():
    return pymysql.connect(
        host=HOST_DATABASE,
        user=USER_DATABASE,
        password=PASSWORD_DATABASE,
        db=DATABASE_NAME,
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor
    )
