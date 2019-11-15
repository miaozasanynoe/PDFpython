for i in datadict:
    try:
        exstr =  "insert into record_v2 (patient_name,age,sex,first_visit,chief_complaint,content,orgin) values('%s','%s','%s','%s','%s','%s','%s')"%(pymysql.escape_string(datadict[i])['姓名'],pymysql.escape_string(datadict[i])['年龄'],pymysql.escape_string(datadict[i])['性别'],pymysql.escape_string(datadict[i])['初诊时间'],pymysql.escape_string(datadict[i])['主诉及病历']
        ,pymysql.escape_string(datadict[i])['全文'],'中国现代名中医医案精粹第2集')
        print(exstr)
        conn.query(exstr)
        conn.commit()
    except Exception as e:
        print(str(e))