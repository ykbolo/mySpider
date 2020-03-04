import json
import pymysql
db = pymysql.connect(
            "localhost", "root", "password", "spiderurl")
cursor = db.cursor()


f = open("sudaNews2.json",encoding='UTF-8')               # 返回一个文件对象   
line = f.readline()               # 调用文件的 readline()方法   
count=0
while line:   
    # print(line)# 在 Python 3 中使用   
    line = f.readline()
    load=json.loads(line)
    # print(load['father'],load['url'])
    sql = "INSERT IGNORE INTO json(url,father) VALUE ('%s','%s')" % (
            load['url'], load['father'])
    cursor.execute(sql)
    count=count+1
    
db.commit()
db.close()
f.close()