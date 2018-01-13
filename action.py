import os
import cv2
import getpic

action = {}
def click(pos):
    x = action[pos][0]
    y = action[pos][1]
    cmd = 'adb shell input tap %d %d'%(y,x)
    print(cmd)
    os.system(cmd)

def pull_screenshot():
    os.system('adb shell screencap -p /sdcard/buffer.bmp')
    os.system('adb pull /sdcard/buffer.bmp .')
    
def detect(pname,pos,w=30): # ok ! pull before detect
    global action
    x = action[pos][0]
    y = action[pos][1]
    p = getpic.pic(fname=pname,x=x,y=y,w=w)
    sim = p.compare()
    
    print(pos,sim)
    
    if sim > 0.9:
        return True
    else:
        return False
    
def init():
    global action
    f = open("save.txt")
    s = f.readline().strip()
    while s: 
        name,x,y=s.split(' ')
        action[name] = (int(x),int(y))
        s = f.readline()
    f.close()

import time
def clear_box():# ok！
    error_time = 0
    while True:
        time.sleep(0.5)
        pull_screenshot()
        if detect("1up.bmp","up") or detect("2up.bmp","up"):
            click("up")
            error_time = 0
        elif detect("1mid.bmp","mid") or detect("2mid.bmp","mid"):
            click("mid")
            error_time = 0
        elif detect("1down.bmp","down") or detect("2down.bmp","down"):
            click("down")
            error_time = 0
        elif detect("full.bmp","full"):
            print("盒子满了!!! \a\a")
            input()
        else:
            error_time += 1
            if error_time<3:
                continue
            print("结束 \a\a 是否继续?(y/n)" )
            if input()=='y':
                continue
            break
            
            
# don't need detect in first 1000 hits
def chouj(ct=5,thr=1000):
    temp = thr
    while ct:
        while temp>0:
            click('chouj')
            temp -= 1
        click('chouj')
        click('chouj')
        click('chouj')
        click('chouj')
        click('chouj')
        click('chouj')
        click('chouj')
        click('chouj')
        click('chouj')
        pull_screenshot()
        if detect('reset.bmp','reset'):
            click('reset')
            time.sleep(1)
            click('reset_ok')
            time.sleep(1.7)
            click('reset_over')
            ct-=1
            temp = thr

init()

while True:# ok .
    print(u"输入一次性抽取池子数目")
    ans = int(input())
    chouj(ans)
    print(u"前往邮箱任意领取一个物品后开始自动筛选清理(y/n)")
    ans = input()
    if ans =='y':
        clear_box()
        
        
        
        
        
        
        #

