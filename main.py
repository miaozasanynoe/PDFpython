# -*- coding:utf-8
import sys,os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # __file__获取执行文件相对路径，整行为取上一级的上一级目录
sys.path.append(BASE_DIR)
import json
import math
import tempfile
import re
from glob import glob
from PIL import Image
from pdf2image import convert_from_path
from PyPDF2 import PdfFileReader, PdfFileWriter
from aip import AipOcr

#百度api参数设置---------
APP_ID = ''
API_KEY = ''
SECRET_KEY = ''
#新建一个AipOcr
client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
#可选参数
options = {}
options["language_type"] = "CHN_ENG"
options["detect_direction"] = "true"
options["detect_language"] = "true"
options["probability"] = "true"
#---------------------

#读取本地图片-----------
def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()
#---------------------
#压缩图片
def resize_Images(source_dir, target_dir, threshold):
    filenames = glob('{}/*'.format(source_dir))
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    for filename in filenames:
        filesize = os.path.getsize(filename)
        if filesize >= threshold:
            print(filename)
            with Image.open(filename) as im:
                width, height = im.size
                if width >= height:
                    new_width = int(math.sqrt(threshold/2))
                    new_height = int(new_width * height * 1.0 / width)
                else:
                    new_height = int(math.sqrt(threshold/2))
                    new_width = int(new_height * width * 1.0 / height)
                resized_im = im.resize((new_width, new_height))
                output_filename = filename.replace(source_dir, target_dir)
                resized_im.save(output_filename)
#---------------------
#pdf转图片-------------
def pdf_to_Image(filename, outputDir):
    print('filename=', filename)
    print('outputDir=', outputDir)
    with tempfile.TemporaryDirectory() as path:
        images = convert_from_path(filename)
        for index, img in enumerate(images):
            img.save('%s/page_%s.png' % (outputDir, index))
#---------------------
#百度pai图片识别转文字---
def baiduOCR_Image_to_Txt(filepath):
    image = get_file_content(filepath)
    api_json_str=client.basicGeneral(image, options)
    #print(api_json_str)
    #api_json=json.dumps(api_json_str,ensure_ascii=False)
    #print(textjson)
    #print(api_json)
    #print(api_json_str["words_result"])
    
    f = open('sorce/apitxtmin.txt','a')
    for i in api_json_str["words_result"]:
        try:
            print(i["words"])
            f.write(i["words"])
        except:
            continue
#---------------------
#第二季传处理json-------
def second_JSON():
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
#---------------------
#正则表达式处理txt文件---
def re_Txt(filepath):
    f = open(filepath, "r", encoding='utf-8')     
    data = f.read()                         
    f.close()
    w=['某','按语','例','初诊','主诉及病史','二诊','三诊','四诊','处方','号方']                                   
    pat1=re.compile('..(?<='+w[0]+').*?(?='+w[1]+')')
    result = pat1.findall(data)                  
    dict={}   
    cnt=0           
    for i in result:
        #print(i)
        split_res=re.split('('+w[2]+'..'+w[0]+')',i)
        tmp_res=["".join(split_res[0])]
        split_res = ["".join(i) for i in zip(split_res[1::2],split_res[2::2])]
        split_res.insert(0,tmp_res[0])
        
        for x in split_res:
            cnt=cnt+1
            print('第'+str(cnt)+"次===================")
            dict[str(cnt)]=x
    dictjson=json.dumps(dict,ensure_ascii=False)
    with open('sorce/meddict.json','wb') as f:
        f.write(dictjson.encode())
    return dict

pdf_to_Image(r'sorce/1.pdf', 'imageset/1')
for i in range(2,1000):
    try:
        filepath='imageset/6/page_'+str(i)+'.png'
        baiduOCR_Image_to_Txt(filepath)
    except:
        continue
re_Txt("sorce/apitxtmin.txt")
second_JSON()
