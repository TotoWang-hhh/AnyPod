## 反弹滑动切换
import tkinter as tk
import tkinter.ttk as ttk
import string
import os
from PIL import ImageTk,Image

def fluent_change(i=0):
    global backbtn
    fluent_list = [0.02,0.02,0.06,0.1,0.18,0.3,0.18,0.1,0.06,0.02,0.02,-0.03,-0.03]
    for f in flst:
        f.place(x=int(f.place_info()['x'])-640*fluent_list[i])
    #返回按钮
    if int(flst[0].place_info()['x'])==0 or int(flst[0].place_info()['x'])==-3200:
        backbtn['bg']='#0078d7'
    else:
        backbtn['bg']='white'
    if i<len(fluent_list)-1:root.after(30,fluent_change,i+1)#30ms移动一次

def fluent_back(i=0):
    global backbtn
    fluent_list = [0.02,0.02,0.06,0.1,0.18,0.3,0.18,0.1,0.06,0.02,0.02,-0.03,-0.03]
    for f in flst:
        f.place(x=int(f.place_info()['x'])+640*fluent_list[i])
    #返回按钮
    if int(flst[0].place_info()['x'])==0 or int(flst[0].place_info()['x'])==-3200:
        backbtn['bg']='#0078d7'
    elif int(flst[0].place_info()['x'])>640:
        backbtn['bg']='#f0f0f0'
    else:
        backbtn['bg']='white'
    if i<len(fluent_list)-1:root.after(30,fluent_back,i+1)#30ms移动一次

def init_place(i=0):
    global backbtn
    for f in flst:
        f.place(width=640,height=480,x=640*flst.index(f))
    #返回按钮
    if int(flst[0].place_info()['x'])==0:
        backbtn['bg']='#0078d7'
    else:
        backbtn['bg']='white'

def reg():
    global dskregtxt
    dskregtxt['text']='设备：'+str(dskenter.get())
    dirregtxt['text']=get_path(pathstr=direnter.get('1.0',tk.END))
    fluent_change()

def mkcfg(dsk,path):
    f=open(str(dsk)+'/anypod.cfg','w',encoding='utf-8')
    f.write(str(path))
    f.close()
    fluent_change()

def get_path(pathstr):#路径处理函数
    new=''
    lst=pathstr.split('\n')
    lst.remove('')
    for i in lst:
        if len(i)>0:#检测是否空项
            i=i.replace('\\','/')#统一使用正斜杠
            if i[len(i)-1]!='/':
                i+='/'
            if ':' in i:#检测是否有盘符
                new+=i[2:len(i)-1]+'\n'
            elif i[0]!='/':#检测开头是否是斜杠
                new+='/'+i+'\n'
    paths=new
    return paths

def get_vol():
    global vol
    vol=dskenter.get()
    fluent_change()

def get_disklist():#获取所有盘符（暴力警告
    disk_list = []
    for c in string.ascii_uppercase:
        disk = c + ':'
        if os.path.isdir(disk):
            disk_list.append(disk)
    return disk_list

root = tk.Tk()
root.geometry('640x480')
root.title('设置新的AnyPod设备')
root.resizable(0,0)

#直接显示在root上的内容
fbottom=tk.Frame(root)

fbottom.place(width=640,height=480)

tk.Label(fbottom,text='看上去您遇到了麻烦',font=('等线',35)).place(x=50,y=50)
tk.Label(fbottom,text='别担心！您马上就能回去！',font=('等线',15)).place(x=50,y=150)
tk.Label(fbottom,text='您不会丢失任何更改',font=('等线',15)).place(x=50,y=180)
tk.Button(fbottom,text='回到开始',bd=0,bg='#0078d7',fg='white',font=('等线',20),command=init_place).place(x=50,y=300)
tk.Label(fbottom,text='当然，如果您是来找彩蛋的',font=('等线',10)).place(x=50,y=400)
tk.Label(fbottom,text='那么恭喜您来对了:)',font=('等线',10)).place(x=50,y=415)

#页面Frame
flst=[tk.Frame(root,bg='#0078d7'),tk.Frame(root,bg='white'),tk.Frame(root,bg='white'),tk.Frame(root,bg='white'),tk.Frame(root,bg='white'),tk.Frame(root,bg='#0078d7')]

#返回
backbtn=tk.Button(root,text='◀ 返回',bd=0,bg='white',fg='#0078d7',font=('等线',15),command=fluent_back,anchor='w')
backbtn.place(x=10,y=10)

init_place()

#第1页
tk.Label(flst[0],text='设置新的AnyPod设备',bg='#0078d7',fg='white',font=('等线',40)).pack(pady=70)
tk.Label(flst[0],text='在此向导的帮助下，这将不会很难',bg='#0078d7',fg='white',font=('等线',15)).pack(pady=5)
tk.Label(flst[0],text='您只需要按照软件的指导进行操作',bg='#0078d7',fg='white',font=('等线',15)).pack(pady=5)
tk.Button(flst[0],text='  让我们开始吧  ',bd=0,bg='white',fg='#0078d7',font=('等线',20),command=fluent_change).pack(pady=50)

#第2页
tk.Label(flst[1],text='清理设备存储根目录',bg='white',font=('等线',40)).pack(pady=40)
tk.Label(flst[1],text='软件会在根目录下存储一个配置文件',bg='white',font=('等线',15)).pack(pady=5)
tk.Label(flst[1],text='这不会占用很多空间',bg='white',font=('等线',15)).pack(pady=5)
tk.Label(flst[1],text='但我还是建议您先整理根目录',bg='white',font=('等线',15)).pack(pady=5)
tk.Label(flst[1],text='您可以在整理完成后点击“继续”',bg='white',font=('等线',15)).pack(pady=5)
tk.Label(flst[1],text='也可以直接继续来跳过',bg='white',font=('等线',15)).pack(pady=5)
tk.Button(flst[1],text='     继续     ',bd=0,bg='#0078d7',fg='white',font=('等线',20),command=fluent_change).pack(pady=40)

#第3页
tk.Label(flst[2],text='选择您想添加的设备',bg='white',font=('等线',30)).pack(pady=20)
tk.Label(flst[2],text='请点击“刷新设备列表”，然后在下拉框中选择代表您设备的盘符',bg='white',font=('等线',15)).pack(pady=5)
values = get_disklist()
dskenter = ttk.Combobox(flst[2],values=values,font=('等线',20))
dskenter.pack(fill=tk.X,padx=150,pady=40)
tk.Button(flst[2],text='刷新设备列表',bd=0,bg='lightgray',fg='black',font=('等线',20),command=lambda:dskenter.configure(values=get_disklist())).pack(pady=10)
tk.Button(flst[2],text='     继续     ',bd=0,bg='#0078d7',fg='white',font=('等线',20),command=get_vol).pack(pady=40)

#第4页
tk.Label(flst[3],text='添加需要同步的路径',bg='white',font=('等线',30)).pack(pady=20)
tk.Label(flst[3],text='在下面添加所有您想进行音乐同步的路径，以回车分隔',bg='white',font=('等线',15)).pack(pady=5)
direnter=tk.Text(flst[3],bd=0,height=10,bg='#CCCCCC',font=('consolas',13))
direnter.pack(fill=tk.X,padx=30)
tk.Button(flst[3],text='     继续     ',bd=0,bg='#0078d7',fg='white',font=('等线',20),command=reg).pack(pady=40)

#第5页
tk.Label(flst[4],text='那么，总结下来',bg='white',font=('等线',30)).pack(pady=20)
tk.Label(flst[4],text='将会以此配置设置新的AnyPod设备',bg='white',font=('等线',15)).pack(pady=5)
dskregtxt=tk.Label(flst[4],text='加载中',bg='white',font=('等线',15))
dskregtxt.pack(pady=5)
dirregtxt=tk.Label(flst[4],text='加载中',bg='white',font=('等线',15))
dirregtxt.pack(pady=5)
tk.Button(flst[4],text='   开始设置   ',bd=0,bg='#0078d7',fg='white',font=('等线',20),command=lambda:mkcfg(vol,get_path(direnter.get('1.0',tk.END)))).pack(pady=40)

#第6页
tk.Label(flst[5],text='完成',bg='#0078d7',fg='white',font=('等线',40)).pack(pady=70)
tk.Label(flst[5],text='已成功设置新的AnyPod设备',bg='#0078d7',fg='white',font=('等线',15)).pack(pady=5)
tk.Label(flst[5],text='向导已结束，请按“关闭”来退出\n若同步未开始，请重新插拔设备或重启软件\n以后您可以直接编辑anypod.cfg来设置要同步的路径',bg='#0078d7',fg='white',font=('等线',15)).pack(pady=5)
tk.Button(flst[5],text='     关闭     ',bd=0,bg='white',fg='#0078d7',font=('等线',20),command=root.destroy).pack(pady=50)

root.mainloop()
#root.bind('<Button-1>',lambda e:fluent_change())#鼠标左键切换界面
