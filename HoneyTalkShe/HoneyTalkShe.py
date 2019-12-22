#!/usr/bin/env python3
# 文件名：socket_keHu.py
# 作者：聪明的瓦肯人
# 微信公众号：工业光线
# 个人主页：http://www.tech-xjc.com


# 导入 socket 等模块
import os
import time
import socket
import sqlite3
import win32api
import win32gui
from tkinter import *
import threading
from tkinter import scrolledtext
from tkinter.messagebox import showinfo

adr = input('>>请输入局域网或公网地址：')
port = input('>>请输入局域网或公网端口：')


#回调函数事件
event = '<Return>'  
error = '注意：对面的渣男试图关闭对话框，已被拦截！'

# 创建 socket 对象
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

# 连接服务，指定主机和端口
try:
    s.connect((adr, int(port)))
    print('连接成功！')
    print('5秒后隐藏窗口！')
    time.sleep(5)
    
    #隐藏控制台窗口
    ct = win32api.GetConsoleTitle()
    hd = win32gui.FindWindow(0,ct)
    win32gui.ShowWindow(hd,0)   
except:
    print('连接失败，地址端口错误或服务器未启动！')
    print('5秒后关闭程序')
    time.sleep(5)
    os._exit(0)

class GUI(object):
    def __init__(self,root):
        self.root = root
        self.root.geometry('270x360')
        self.root.resizable(width=False, height=False)
        self.root.title('HoneyTalk_SHE')
        self.root.iconbitmap('girl.ico')
        self.root['background'] = 'pink'
        self.root.attributes('-alpha',0.9)
        self.root.protocol('WM_DELETE_WINDOW',self.close)
        self.entry = Entry(self.root)
        self.entry.place(x=10,y=325)
        self.entry.bind("<Return>",self.callback)
        self.button = Button(self.root,text = 'Send',command = self.send)
        self.button.place(x=165,y=322)
        self.button0 = Button(self.root,text = 'More',command = self.more)
        self.button0.place(x=215,y=322)
        self.out = scrolledtext.ScrolledText(self.root)
        self.out.place(x=10,y=0,width=250)
        #设置tag即插入文字的大小,颜色等
        self.out.tag_config('tag0',foreground = 'hotpink') 
        self.out.tag_config('tag1',foreground = '#1E90FF')

    def close(self):
        #showinfo('提示','确认关闭程序吗？')
        s.close()
        os._exit(0)

    def send(self):
        content = self.entry.get()
        
        if content != '':
            self.out.config(state = 'normal')
        self.out.insert(END,'SHE:'+content+'\n\n','tag0')
        self.out.see(END)
        self.out.config(state = 'disable')
        
        try:
            s.send(content.encode('utf-8'))
            self.entry.delete(0,END)
        except:
            pass

    def callback(self,event):
        content = self.entry.get()
        
        if content != '':
            self.out.config(state = 'normal')
        self.out.insert(END,'SHE:'+content+'\n\n','tag0')
        self.out.see(END)
        self.out.config(state = 'disable')
        
        try:
            s.send(content.encode('utf-8'))
            self.entry.delete(0,END)
        except:
            pass

    def more(self):
        showinfo(title='关于',message='1.作者：聪明的瓦肯人 \n2.公众号：工业光线（GongYe_Light） \n3.个人主页：http://www.tech-xjc.com \n4.公众号发送“honeytalk”获得详细介绍 \n5.网络问题会造成回复延迟 \n6.正常使用时请勿重复启动 \n7.请先启动服务器再启动该客户端 \n')
    


def create():
    global gui
    global root
    root = Tk()
    gui = GUI(root)
    root.mainloop()


def rec():
    while True:
        try:
            msg = s.recv(1024)
            gui.out.config(state = 'normal')
            con = msg.decode('utf-8')
            
            if con == error:
                gui.out.insert(END,con+'\n\n')
            else:
                gui.out.insert(END,'HE:'+con+'\n\n','tag1')

            gui.out.see(END)
            gui.out.config(state = 'disable')
        except:
            gui.out.config(state = 'normal')
            gui.out.insert(END,'啊哦~！服务器疑似下线！请敦促男友重启！然后再重启客户端！\n\n')
            gui.out.see(END)
            gui.out.config(state = 'disable')
            
            break

if __name__ == '__main__':
    t1 = threading.Thread(target = create,name = 'create')
    t1.start()
    try:
        rec()
    except:
        pass
