# -*- coding:utf-8
#打开test.txt文本，将里边得文本使用正则表达式筛选出数字那一部分，再存入test1.txt文件中
import re
import json
f = open("sorce/meddict.json", "r", encoding='utf-8')
data = f.read()
f.close()
path=r'sorce/meddict.json'
f1 = open(path, 'r', encoding = 'utf-8')
datadict=json.load(f1)
result = re.findall(r'"(\d+\d.\d*)+":\s*"(\S+?),([男|女]),(\d+岁)\S*初诊:([^>]+?日)。?主诉及病史[^>]*?:(\S+?)。',data)
dict={}
cnt=0
for i in result:
    #print(i[0]+" "+i[1]+"  "+i[2]+" "+i[3]+" "+i[4]);
    cnt=cnt+1
    dictm={}
    dictm["姓名"]=i[1]
    dictm["年龄"]=i[2]
    dictm["性别"]=i[3]
    dictm["初诊时间"]=i[4]
    dictm["主诉及病历"]=i[5]
    dictm["全文"]=datadict[i[0]]
    dict[str(cnt)]=dictm
    print(i[0])
    dictjson=json.dumps(dict,ensure_ascii=False)
    with open('sorce/meddict1.json','wb') as f:
        f.write(dictjson.encode())
#print(result)