import pymysql
import json,os

def db_insert():
    try:
        conn = pymysql.connect(host='', user='', passwd='3', db='', port=3306, charset='utf8')
        cur = conn.cursor()
        cur.execute('desc medie')
        data = cur.fetchall()
        for d in data:
            print("id: "+str(d[0])+' 密码：'+d[2])
        cur.close()
        conn.close()
    except Exception as e:
        print(str(e))
conn = pymysql.connect(host='106.54.23.221',
user='root', passwd='miaoz1103', db='med', port=3306, charset='utf8')
#cur = conn.cursor()

path=r'sorce/meddict.json'
f = open(path, 'r', encoding = 'utf-8')
datadict=json.load(f)
for i in datadict:
    try:
        exstr =  "insert into Record (record_content,origin) values('%s','中国现代名中医医案精粹第三集')"%(pymysql.escape_string(datadict[i]))
        print(exstr)
        conn.query(exstr)
        conn.commit()
    except Exception as e:
        print(str(e))


#1366 - Incorrect string value: '\xE9\x82\xA3\xE6\insert into Records (record_content,record_origin) values('111','中国现代名中医医案精粹第三集')