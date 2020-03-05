import json
import pymysql
db = pymysql.connect(
    "localhost", "root", "yk84732225", "spiderurl")
cursor = db.cursor()


f = open("./text.txt", 'r', encoding='utf-8')
line = f.readline()
count = 0
while line:
    # print(line)# 在 Python 3 中使用
    line = f.readline()
    if line:

        load = json.loads(line)
        # print(load['father'],load['url'])
        sql = "INSERT IGNORE INTO json(url,father) VALUE ('%s','%s')" % (
            load['url'], load['father'])
        cursor.execute(sql)
        count = count+1
        print(count, end='|')
db.commit()
db.close()
f.close()
