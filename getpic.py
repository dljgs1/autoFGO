import os
import cv2
import threading

from numpy import *
from tkinter import *
from PIL import Image, ImageTk



tk = Tk()
canvas = Canvas(width=200,height=100)
canvas.pack()

def pull_screenshot():
    os.system('adb shell screencap -p /sdcard/buffer.bmp')
    os.system('adb pull /sdcard/buffer.bmp .')

    
def tobinary(image):
    img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return cv2.threshold(img, 127, 255, cv2.THRESH_BINARY_INV)

class pic:
    def __init__(self,fname,x=200,y=200,w=100):
        self.fname = fname
        self.img = cv2.imread(fname)
        try:
            if self.img==None:
                print("error file,",fname)
                self.img = cv2.imread(fname)
        except:
            pass
        self.x = int(x)
        self.y = int(y)
        self.w = int(w)
    
    def get_cut(self):
        w = self.w/2
        x1 = int(self.x-w)
        x2 = int(self.x+w)
        y1 = int(self.y-w)
        y2 = int(self.y+w)
        b,g,r = cv2.split(self.img[y1:y2,x1:x2])
        img = cv2.merge((r,g,b))
        im = Image.fromarray(img)
        imgtk = ImageTk.PhotoImage(image=im)
        return imgtk
        
    def transxy(self):
        x = self.img.shape[1]-self.x
        y = self.y
        return x,y
        
    def save_xy(self):
        print("input pos name")
        s = input()
        f = open("save.txt","a")
        s+=" %d %d\n"%(self.transxy())
        f.write(s)
        f.close()
        
    def modi_w(self):
        print("input w")
        w = input()
        self.w = int(w)
        
    def flush_pic(self):
        pull_screenshot()
        self.img = cv2.imread(self.fname)
        
        
        
        
    def compare(self,pname="buffer.bmp"):
        img = pic(pname,self.x,self.y,self.w)
        x,y = img.transxy()
        w = self.w/2
        x1 = int(x-w)
        x2 = int(x+w)
        y1 = int(y-w)
        y2 = int(y+w)
        
        print(x1,x2,y1,y2)
        
        img1 = img.img[y1:y2,x1:x2]
        img2 = self.img
        
        try:
            if img1 == None or img2==None:
                self.img = cv2.imread(self.fname)
                return self.compare(pname)
        except:
            pass

        #原始图片是压缩了的 因此要二值化处理后再进行比较
        ret,img1 = tobinary(img1)
        ret,img2 = tobinary(img2)
        
            
        #print(img1.shape,img2.shape)
        xor = cv2.bitwise_xor(img1,img2)
        #cv2.imshow('w',xor)
        #cv2.waitKey(0)
        #cv2.imshow('w1',img1)
        #cv2.imshow('w2',img2)
        #cv2.waitKey(0)
        ct = count_nonzero(xor)
        all = (x2-x1)*(y2-y1)
        return (all-ct)/all
        
        
    def save_pic(self):
        w = self.w/2
        print("input pic name")
        name = input()
        x1 = int(self.x-w)
        x2 = int(self.x+w)
        y1 = int(self.y-w)
        y2 = int(self.y+w)
        img = self.img[y1:y2,x1:x2]
        cv2.imwrite(name,img)
        
orgpic = pic("buffer.bmp",200,480,30) 
label = None

def push_pic():
    global tk
    global orgpic
    global label
    imgtk = orgpic.get_cut()
    label.configure(image=imgtk)
    tk.draw()
    try:
        tk.draw()
    except:
        pass
    
def move_pic(t):
    if t=="s":
        orgpic.save_xy()
    if t=="w":
        orgpic.modi_w()
    if t=="p":
        orgpic.save_pic()
    if t=="f":
        orgpic.flush_pic()
        
    if t=="Up":
        orgpic.y -= 10
    if t=="Right":
        orgpic.x += 10
    if t=="Left":
        orgpic.x -= 10
    if t=="Down":
        orgpic.y += 10
    push_pic()
    
    
def echo_event(evt):
    if evt.type == "2":
        print("键盘：%s" % evt.keysym)
        if evt.keysym!="m":
            move_pic(evt.keysym)
    
    print(evt.type)

    
def init():
    #键盘事件
    canvas.bind_all("<KeyPress>",echo_event)
    #如果绑定指定的键盘，则"<Key>" 或者"<KeyPress>"都可以，具体到指定键的话后面加入下划线和指定的键就好了，如：绑定小写字母t和Left键
    canvas.bind_all("<KeyPress-t>",echo_event)
    canvas.bind_all("<KeyPress-Left>",echo_event)
    #鼠标事件
    canvas.bind_all("<Double-Button-1>",echo_event)
    canvas.bind_all("<Button-1>",echo_event)
    canvas.bind_all("<Button-2>",echo_event)
    canvas.bind_all("<Button-3>",echo_event)  
    
    global label,orgpic
    imgtk = orgpic.get_cut()
    label = Label(tk, image = imgtk)
    label.bm = imgtk
    label.pack()
    


if __name__ == "__main__":    
    init()
    tk.mainloop()
    
    
    
    
    
	
# pull_screenshot()
# img = cv2.imread('autojump.bmp')
# cv2.imshow('w',img)
# cv2.waitKey(0)