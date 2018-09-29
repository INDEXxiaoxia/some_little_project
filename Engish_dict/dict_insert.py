import pymysql
import re

f=open("dict.txt","rt")
db=pymysql.connect("localhost","root","123456","dict")
cursor=db.cursor()

for line in f:
    l=re.split(r'\s+',line)#用空字符分开单词与解释生成列表
    word=l[0]
    interpret=' '.join(l[1:])#用空格拼接处单词外的
    sql="insert into words (word,interpret) values('%s','%s')"%(word,interpret)
    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()
f.close()