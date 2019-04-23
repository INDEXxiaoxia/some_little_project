import tkinter as tk
from tkinter import messagebox

def vrhr(file_in,typeCode):
    file_out=file_in.split('.')[0]+'【转换】.'+file_in.split('.')[1]
    try:
        with open(file_in,'rb') as f:
            contents=f.read().decode(typeCode)
        with open(file_out,'wb') as f:
            f.write(contents.encode())
    except Exception as e:
        contents=e
    return contents

showindow=tk.Tk()
showindow.title('txt乱码转换')
showindow.geometry('420x350')
l=tk.Label(showindow,text='文件路径:',bg='white',
           font=('Arial',10),width=8,height=1).place(x=10,y=25,anchor='nw')
ll=tk.Label(showindow,text='编码类型:',bg='white',
           font=('Arial',10),width=8,height=1).place(x=10,y=60,anchor='nw')
lll=tk.Label(showindow,text='''
	请输入完整文件路径
	常用编码类型：GBK、utf-8、latin1
	made by 茵夏
	''',bg='white',
           font=('Arial',10),width=49,height=3).place(x=10,y=95,anchor='nw')
llll=tk.Label(showindow,text='转换结果及预览',bg='white',
           font=('Arial',10),width=49,height=1).place(x=10,y=160,anchor='nw')
e_in=tk.Entry(showindow,width=40,show=None)#输入框
e_in.place(x=100,y=25,anchor='nw')#输入框配置

e_type=tk.Entry(showindow,width=40,show=None)#输入框
e_type.place(x=100,y=60,anchor='nw')#输入框配置

var=tk.StringVar()
def getval():
    var_in=e_in.get()#获取文件名
    var_type=e_type.get()
    contents=vrhr(var_in,var_type)#读取到的文件内容
    #用于显示
    l = tk.Label(showindow, text=contents, bg='white', font=('Arial', 8), width=65, height=11).place(x=10, y=160)
b=tk.Button(showindow,text='转换',width=6,height=3,command=getval).place(x=360,y=22)


showindow.mainloop()