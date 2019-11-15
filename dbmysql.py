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

path=r'data/第六集.json'
f = open(path, 'r', encoding = 'utf-8')
datadict=json.load(f)
print(datadict)
for i in datadict:
    try:
        exstr =  "insert into record_v2 (patient_name,age,sex,first_visit,chief_complaint,content,orgin) values('%s','%s','%s','%s','%s','%s','%s')"%(pymysql.escape_string(datadict[i]['姓名']),pymysql.escape_string(datadict[i]['年龄']),pymysql.escape_string(datadict[i]['性别']),pymysql.escape_string(datadict[i]['初诊时间']),pymysql.escape_string(datadict[i]['主诉及病历'])
        ,pymysql.escape_string(datadict[i]['全文']),'中国现代名中医医案精粹第6集')
        print(exstr)
        conn.query(exstr)
        conn.commit()
    except Exception as e:
        print(str(e))


#1366 - Incorrect string value: '\xE9\x82\xA3\xE6\insert into Records (record_content,record_origin) values('111','中国现代名中医医案精粹第三集')