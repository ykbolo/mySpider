import json
import pymysql

db = pymysql.connect(
    "localhost", "root", "password", "spiderurl")
cursor = db.cursor()


f = open("sudaMUrls.txt", 'r', encoding='utf-8')
line = f.readline()
count = 0
while line:
    # print(line)# 在 Python 3 中使用
    line = f.readline()
    if line:
        load = json.loads(line)
        if 'doc' not in load['url']:
          # print(load['father'],load['url'])
          sql = "INSERT IGNORE INTO M_T(url,father) VALUE ('%s','%s')" % (
              load['url'],load['father'])
          cursor.execute(sql)
          count = count+1
          print(count, end='|')
db.commit()
db.close()
f.close()
