#!/usr/bin/env python3
# 服务端
# 文件名：HoneyTalkHe.py
# 作者：聪明的瓦肯人
# 微信公众号：工业光线
# 个人主页：http://www.tech-xjc.com

import socket
import time
import win32api
import win32gui
from tkinter import *
import threading
from tkinter import scrolledtext
from tkinter.messagebox import showerror
from tkinter.messagebox import showinfo

#回调函数事件
event = '<Return>'     
error = '注意：对面的渣男试图关闭对话框，已被拦截！'


s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

#获取本机电脑名
myname = socket.gethostname()
#获取本机ip
myaddr = socket.gethostbyname(myname)

print(myname)
print(myaddr)
s.bind((myaddr,8888))

s.listen(1)
print("waiting......")
print('5秒后将隐藏窗口！')
time.sleep(5)

#隐藏控制台窗口
ct = win32api.GetConsoleTitle()
hd = win32gui.FindWindow(0,ct)
win32gui.ShowWindow(hd,0)                           

class GUI(object):
    def __init__(self,root):
        self.root = root
        self.root.geometry('270x360')
        self.root.resizable(width=False, height=False)
        self.root.title('HoneyTalk_HE')
        self.root.iconbitmap('boy.ico')
        self.root['background'] = 'lightskyblue'
        self.root.attributes('-alpha',0.9)
        self.root.protocol('WM_DELETE_WINDOW',self.close)
        self.entry = Entry(self.root)
        self.entry.place(x=10,y=325)
        self.entry.bind("<Return>",self.callback)
        self.button = Button(self.root,text = 'send',command = self.sending)
        self.button.place(x=165,y=322)
        self.button0 = Button(self.root,text = 'More',command = self.more)
        self.button0.place(x=215,y=322)
        self.sock = sock
        self.out = scrolledtext.ScrolledText(self.root)
        self.out.place(x=10,y=0,width=250)
        #设置tag即插入文字的大小,颜色等
        self.out.tag_config('tag0',foreground = 'hotpink') 
        self.out.tag_config('tag1',foreground = '#1E90FF')

    def close(self):
        try:
            showerror('警告','渣男好大的胆，你无权关闭对话框！')
            self.sock.send(error.encode('utf-8'))
        except:
            self.sock.send(error.encode('utf-8'))
            pass
        return
        
    def sending(self):
        content = self.entry.get()
        
        if content != '':
            self.out.config(state = 'normal')
        self.out.insert(END,'HE:'+content+'\n\n','tag1')
        self.out.see(END)
        self.out.config(state = 'disable')
        
        try:
            self.sock.send(content.encode('utf-8'))
            self.entry.delete(0,END)
        except:
            sock.shutdown(2)
            sock.close()
            pass

    #回调函数
    def callback(self,event):                   
        content = self.entry.get()
        
        if content != '':
            self.out.config(state = 'normal')
        self.out.insert(END,'HE:'+content+'\n\n','tag1')
        self.out.see(END)
        self.out.config(state = 'disable')
        
        try:
            self.sock.send(content.encode('utf-8'))
            self.entry.delete(0,END)
        except:
            pass

    def more(self):
        try:
            showinfo(title='关于',message='1.作者：聪明的瓦肯人 \n2.公众号：工业光线（GongYe_Light） \n3.个人主页：http://www.tech-xjc.com \n4.公众号发送“honeytalk”获得详细介绍 \n5.网络问题会造成回复延迟 \n6.正常使用时请勿重复启动 \n7.请先启动该服务器再启动客户端 \n')
        except:
            pass

        
def create():
    global gui
    global root
    root = Tk()
    gui = GUI(root)
    

def rec():
    while True:
        try:
            msg = sock.recv(1024)
            gui.out.config(state = 'normal')
            con = bytes.decode(msg)
            gui.out.insert(END,'SHE:'+con+'\n\n','tag0')
            gui.out.see(END)
            gui.out.config(state = 'disable')
        except:
            sock.shutdown(2)
            sock.close()
            break
    root.quit()
    

if __name__ == '__main__':
    while True:
        sock,addr = s.accept()

        t1 = threading.Thread(target = rec,name = 'rec')
        t1.setDaemon(True)
        create()
        t1.start()
        root.mainloop()

        root.destroy()
