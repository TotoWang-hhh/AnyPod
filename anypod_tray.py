import string
import os
import sys
import time
import requests
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.filedialog as filebox
import tkinter.messagebox as msgbox
import win32.win32api as win32api
import win32.lib.win32con as win32con
import time
from PIL import ImageTk,Image
import pystray
import threading
import hashlib
import eyed3

#杂项准备工作
#屏幕尺寸
scr_w=win32api.GetSystemMetrics(win32con.SM_CXSCREEN)
scr_h=win32api.GetSystemMetrics(win32con.SM_CYSCREEN)

def loginui(event=''):
    global up,e_usr,e_pwd,e_api
    up = tk.Tk()
    up.title("登录")

    #第一行，用户名标签及输入框
    tk.Label(up,text='邮箱').pack(fill=tk.X)
    e_usr = ttk.Entry(up)
    e_usr.pack(fill=tk.X)
    tk.Label(up,text='密码').pack(fill=tk.X)
    e_pwd = ttk.Entry(up,show='●')
    e_pwd.pack(fill=tk.X)
    tk.Label(up,text='API域名').pack(fill=tk.X)
    e_api = ttk.Entry(up)
    e_api.pack(fill=tk.X)
    e_api.insert(0,"cloudmusic-api.txm.world")
     
    #第三行登陆按扭，command绑定事件
    tk.Label(up,text='您的密码将会以MD5存储于软件目录下，\nMD5编码是不可解码的\n作者保证不会窃取您的密码，登录即表示您信任我',fg='grey').pack(side=tk.BOTTOM,fill=tk.X)
    ttk.Button(up,text='登录并存储',command=login).pack(side=tk.BOTTOM,fill=tk.X)
    e_usr.bind('<KeyPress-Return>',lambda event:e_pwd.focus())
    e_pwd.bind('<KeyPress-Return>',lambda event:login())
    e_usr.focus()

    up.update()
    up.geometry('350x'+str(int(up.winfo_height())))
    up.resizable(0,0)

    up.mainloop()

def login():
    global usr,pwd,api#,path
    usr=e_usr.get()
    pwd=e_pwd.get()
    api=e_api.get()
    pwd=hashlib.md5(pwd.encode(encoding='UTF-8')).hexdigest()
    f=open("./usr.dat",'w',encoding='utf-8')
    f.write(usr+'\n'+pwd+'\n'+api)
    #path=filebox.askdirectory(title='请选择音乐保存路径')
    up.destroy()

def rpg(a,b,c):
    global pwin,pga,pgb,pgc
    pga['text']=str(a)
    pgb['text']=str(b)
    pgc['value']=int(c)
    pwin.update()

def rename():
    global filename,e_name,rwin
    filename=e_name.get()
    rwin.destroy()

#toaster.show_toast('程序仍在工作','请勿惊慌，程序仍在后台工作！',threaded=True)
def favdown(path):
    global usr,pwd,pga,pgb,pgc,pwin,filename,e_name,rwin
    try:
        pwin.overrideredirect(True)
        pwin.attributes('-topmost',True)
        
        #imagine_this_is_an(error)#取消注释这行代码可以直接跳进异常处理部分来测试异常处理是否出问题

        rpg('准备下载','获取登录Cookie',0)
        res=requests.get(url="https://"+api+"/login?email="+usr+"&md5_password="+pwd)
        json=res.json()
        cookie=json['cookie']
        
        #过渡动画
        for i in range(1,12+1):
            pgc['value']+=2
            pwin.update()
            time.sleep(0.01)
      
        rpg('准备下载','获取用户ID',25)
        res=requests.get(url="https://"+api+"/user/account?cookie="+str(cookie))
        json=res.json()
        uid=str(json['account']['id'])

        #过渡动画
        for i in range(1,12+1):
            pgc['value']+=2
            pwin.update()
            time.sleep(0.01)

        rpg('准备下载','获取收藏歌单ID',50)
        res=requests.get(url="https://"+api+"/user/playlist?limit=1&uid="+uid)
        json=res.json()
        favlstid=str(json['playlist'][0]['id'])

        #过渡动画
        for i in range(1,12+1):
            pgc['value']+=2
            pwin.update()
            time.sleep(0.01)

        rpg('准备下载','获取收藏歌单',75)
        res=requests.get(url="https://"+api+"/playlist/track/all?id="+favlstid+"&cookie="+cookie)
        json=res.json()

        #过渡动画
        for i in range(1,12+1):
            pgc['value']+=2
            pwin.update()
            time.sleep(0.01)
          
        favlst=[]#id
        favnamelst=[]#歌名
        favarlst=[]#艺人
        favallst=[]#专辑

        rpg('准备下载','整理信息',100)
        #收藏音乐信息挨个存列表
        for song in json['songs']:
            favlst.append(str(song['id']))
            favnamelst.append(str(song['name']))
            favallst.append(str(song['al']['name']))
            favarlst.append([])
            for ar in song['ar']:
                favarlst[json['songs'].index(song)].append(ar['name'])

        for mid in favlst:
            rpg('正在下载（'+str(favlst.index(mid)+1)+'/'+str(len(favlst))+'）',favnamelst[favlst.index(mid)],(favlst.index(mid)/len(favlst))*100)
            if not os.path.exists(path+'/'+favnamelst[favlst.index(mid)]+".mp3"):#避免重复下载
                try:#遇到问题跳过而不中断
                    res=requests.get(url="https://"+api+"/song/url?id="+mid+"&br=320000"+'&cookie='+cookie)
                    json=res.json()
                    murl=json['data'][0]['url']
                    if murl==None:
                        pga['text']='无版权 将跳过'
                        icon.notify('无版权，将跳过 '+favnamelst[favlst.index(mid)],title='可接受的错误')
                        pwin.update()
                        time.sleep(5)
                        pwin.update()
                    else:
                        if 'freeTrialInfo' in list(json['data'][0].keys()):
                            if json['data'][0]['freeTrialInfo']!=None:
                                freesec=json['data'][0]['freeTrialInfo']['end']-json['data'][0]['freeTrialInfo']['start']
                                pga['text']='试听 将跳过'
                                icon.notify(favnamelst[favlst.index(mid)]+' 仅可试听 '+str(freesec)+' 秒，将跳过',title='可接受的错误')
                                pwin.update()
                                time.sleep(5)
                                pwin.update()
                                pass
                        filename=favnamelst[favlst.index(mid)]
                        if '*' in favnamelst[favlst.index(mid)] or '/' in favnamelst[favlst.index(mid)] or '\\' in favnamelst[favlst.index(mid)] or ':' in favnamelst[favlst.index(mid)] or '"' in favnamelst[favlst.index(mid)] or \
                           '?' in favnamelst[favlst.index(mid)] or '|' in favnamelst[favlst.index(mid)]:#防止歌曲名称带非法字符导致下载失败
                            dorename=msgbox.askyesno('网易云收藏音乐下载','歌曲 '+favnamelst[favlst.index(mid)]+' 无法按照原名保存，您需要重命名吗？')
                            if dorename:
                                rwin = tk.Tk()
                                rwin.title("重命名音乐")

                                tk.Label(rwin,text='旧名称：'+favnamelst[favlst.index(mid)]+'.mp3').pack(fill=tk.X)
                                
                                ef=tk.Frame(rwin)
                                tk.Label(ef,text='新名称：').pack(fill=tk.X,side=tk.LEFT)
                                e_name = ttk.Entry(ef)
                                tk.Label(ef,text='.mp3').pack(fill=tk.X,side=tk.RIGHT)
                                e_name.pack(fill=tk.X)
                                ef.pack(fill=tk.X)
                                  
                                ttk.Button(rwin,text='以该名称保存',command=rename).pack(fill=tk.X,expand=True)
                                  
                                e_name.bind('<KeyPress-Return>',lambda event:rename())
                                e_name.focus()
                                  
                                rwin.update()
                                if rwin.winfo_width()<=350:
                                    rwin.geometry('350x'+str(int(rwin.winfo_height())))
                                else:
                                    rwin.geometry(str(int(rwin.winfo_width()))+'x'+str(int(rwin.winfo_height())))
                                rwin.resizable(0,0)
                                while True:
                                    try:#别无选择，只能通过在无法成功刷新的时候break出循环来实现效果
                                        rwin.update()
                                    except:
                                        break
                                #print('重命名操作完成 '+favnamelst[favlst.index(mid)])
                        res=requests.get(url=murl)
                        m=res.content
                        #print('正在下载 '+favnamelst[favlst.index(mid)]+' 至目录 '+path+filename+".mp3")
                        f=open(path+filename+".mp3",'wb')
                        f.write(m)
                        f.close()
                        #编辑信息
                        ars=''
                        for i in favarlst[favlst.index(mid)]:
                            ars+=i+';'
                        ars=ars[0:len(ars)-1]
                        #infres=requests.get(url="https://cloudmusic-api.txm.world/song/detail?ids="+mid)
                        #infjson=infres.json()
                        #inf=infjson['songs'][0]
                        audiofile = eyed3.load(path+filename+".mp3")
                        audiofile.initTag()
                        audiofile.tag.title = favnamelst[favlst.index(mid)]
                        audiofile.tag.artist = ars
                        audiofile.tag.album = favallst[favlst.index(mid)]
                        #audiofile.tag.images.set(type_=3,img_data=img,mime_type='image/jpeg')  # 封面，但是用不了
                        #audiofile.tag.recording_date = str(pubyear)  # 年份，但是去掉可以省很多事
                        audiofile.tag.save()
                except Exception as e:
                    #toaster.show_toast('可接受的错误','下载 '+favnamelst[favlst.index(mid)]+' 时遇到错误，将跳过本音乐\n\n'+str(e),duration=10)
                    print(str(e))
                    pga['text']='下载错误 将跳过'
                    icon.notify('下载错误，将跳过 '+favnamelst[favlst.index(mid)],title='可接受的错误')
                    pwin.update()
                    time.sleep(5)
                    pwin.update()

        pga['text']='下载完成！'
        pgb['text']='恭喜！全部音乐下载完成！'
        icon.notify('恭喜！全部音乐下载完成！',title='下载完成！')
        pwin.update()

    except Exception as e:
        try:
            pwin.configure(background='#FF9090')
            pga['bg']='#FF9090'
            pgb['bg']='#FF9090'
            pwin.attributes('-alpha',1)
            pga['text']='错误'
            pgb['text']=json['message']
            #pframe.add_info((4,2),info_text=pga['text']+'：'+pgb['text'])
            print(str(e))
        except:
            pwin.configure(background='#FF9090')
            pga['bg']='#FF9090'
            pgb['bg']='#FF9090'
            pwin.attributes('-alpha',1)
            pga['text']='本地错误'
            pgb['text']=str(e)
            #pframe.add_info((4,2),info_text=pga['text']+'：'+pgb['text'])
            print(str(e))

def get_disklist():#获取所有盘符（暴力警告
    disk_list = []
    for c in string.ascii_uppercase:
        disk = c + ':'
        if os.path.isdir(disk):
            disk_list.append(disk)
    return disk_list

def change_icon(icona,item):
    icon.notify('抱歉，但是本功能尚不可用',title='尚不可用')

def show_window():#显示/隐藏进度窗
    global show
    if not show:
        pwin.deiconify()
        for i in range(1,27+1):
            pwin.geometry('250x68'+'+'+str(int(scr_w-250))+'+'+str(int(scr_h-(108-28*4+i*4))))
            time.sleep(0.005)
            pwin.update()
        pwin.geometry('250x68+'+str(int(scr_w-250))+'+'+str(int(scr_h-108)))
        pwin.update()
        show=True
    else:
        for i in range(1,27+1):
            pwin.geometry('250x68'+'+'+str(int(scr_w-250))+'+'+str(int(scr_h-(108-i*4))))
            time.sleep(0.005)
            pwin.update()
        pwin.withdraw()
        pwin.update()
        show=False

def sync():#同步函数
    lastdsks=[]
    while True:
        dsks=get_disklist()
        for dsk in dsks:
            if dsk not in lastdsks:#这意味着这是一个新插入的磁盘
                if os.path.isfile(dsk+'/anypod.cfg'):#如果这里有配置文件，说明这是AnyPod设备
                    icon.notify(dsk+'是AnyPod设备，将开始同步',title=dsk+'是AnyPod设备')
                    f=open(dsk+'/anypod.cfg','r',encoding='utf-8')
                    dirstr=f.read()
                    f.close()
                    dirs=dirstr.split('\n')
                    if '' in dirs:
                        dirs.remove('')#去除空行，避免出错
                    for i in dirs:
                        i.replace('\\','/')#反斜杠换正斜杠
                        if i[len(i)-1]!='/':#给目录结尾加上斜杠
                            i+='/'
                        favdown(dsk+i)
        lastdsks=dsks
        time.sleep(0.5)


if os.path.exists("./usr.dat"):
    f=open("./usr.dat",'r',encoding='utf-8')
    try:
        data=f.read().split('\n')
        usr=data[0]
        pwd=data[1]
        api=data[2]
    except:
        msgbox.showerror('错误','账户数据文件格式错误，请删除配置文件（usr.dat）后重启软件重新登录。')
        sys.exit()
else:
    loginui()

pwin=tk.Tk()
pwin.title('网易云收藏音乐下载')
pga=tk.Label(pwin,text='进度A未显示')
pga.pack(fill=tk.X)
pgb=tk.Label(pwin,text='进度B未显示')
pgb.pack(fill=tk.X)
pgc=ttk.Progressbar(pwin,length=250,value=0)
pgc.pack(fill=tk.X)
show=False
pwin.withdraw()

#托盘
use_color_icon=False
menu = (pystray.MenuItem('显示进度',show_window,default=True),pystray.MenuItem('退出',exit))
iconimg = Image.open("icon.png")
icon = pystray.Icon("AnyPod",iconimg,"AnyPod",menu)
icon.run_detached()

#lastdsks=get_disklist()

synct=threading.Thread(target=sync)
synct.start()

pwin.mainloop()
