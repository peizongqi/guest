# -*- coding: utf-8 -*-
import pymysql.cursors

# 操作数据库示例
# Connect to the database
connection = pymysql.connect(host='127.0.0.1',
                             user='root',
                             password='123456',
                             db='guest',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
try:
  with connection.cursor() as cursor:
    # Create a new record
    sql = 'INSERT INTO sign_guest (realName, phone, email, sign, event_id,createTime) VALUES ("pzq",18800110001,"pzq@mail.com",0,1,NOW());'

    cursor.execute(sql)
    # connection is not autocommit by default. So you must commit to save
    # your changes.
    connection.commit()

  with connection.cursor() as cursor:
    # Read a single record
    sql = "SELECT realName,phone,email,sign FROM sign_guest WHERE phone=%s"
    cursor.execute(sql, ('18800110001',))
    result = cursor.fetchone()
    print(result)
finally:
 connection.close()
