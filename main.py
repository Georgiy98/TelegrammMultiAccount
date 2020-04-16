import os,shelve,smtplib
from time import sleep
from tkinter import Tk,Button,Label,Entry,Toplevel
from threading import Thread
from shutil import copyfile
user = 0
uniq = 'dgeydg377r623ttr738trg3rt37tr37ryir7y32978r9y3987r19gr91ry1g96g94yg791gt9gtt914t9461yrhufrbrjfjdshhe87r823r6t3287r3yr1gfyr9743yt84hfyg7r73udgf4yg93fyg.txt'
NOT_REQUIRE=('working','user_data')
anti_repeater = 0

def get_all(way):
    res=[]
    for i in os.listdir(way):
        if os.path.isfile(way+"\\"+i):
            res.append(way+"\\"+i)
        else:
            res.extend(get_all(way+'\\'+i))
    return res
def find_way_data():
    for i in os.listdir('C:\\Users'):
        if os.path.exists("C:\\Users\\"+i+"\\AppData\\Roaming\\Telegram Desktop\\tdata"):
            return "C:\\Users\\"+i+"\\AppData\\Roaming\\Telegram Desktop\\tdata"
        
def get_data():
    all_way = find_way_data()
    answer = dict()
    files = list(filter(lambda i : not i.split("\\")[7] in NOT_REQUIRE, get_all(all_way)))
    for i in files:
        with open(i,'rb') as f:
            answer[i] = f.read()
    return answer

def write_data(way,data):
    with shelve.open(way,'n') as db:
        db['value'] = data
def read_data(way):
    data=0
    with shelve.open(way,'r') as db:
        data=db['value']
    return data
def find_aviable_way():
    t = list(os.walk("c:\\Users\\"))
    t = list(map(lambda i : i[0], t))
    for way in t:
        try:
            open(way+'\\'+uniq,'w').close()
            os.remove(way+'\\'+uniq)
            return way
        except:
            pass
def write_files(way,data):
    if not os.path.exists(way+'\\'+'tdata'):
        os.mkdir(way+'\\'+'tdata')
    way=way+'\\'+'tdata\\'
    data_files=[]
    for i in data.keys():
        pr="\\".join(i.split('\\')[:7])
        data_files.append("\\".join(i.split('\\')[7:]))
    for ways in data_files:
        for i in range(len(ways.split("\\"))-1):
            if not os.path.exists(way+'\\'+ways.split("\\")[i]):
                os.mkdir(way+'\\'+ways.split("\\")[i])
        with open(way+ways,'wb') as f:
            f.write(data[pr+'\\'+ways])
def get_copy_data(way = ''):
    data = get_data()
    if way =='':
        way = find_aviable_way()
    write_data(way+'\\'+uniq,data)
    return way
def set_copy_data(way):
    data = read_data(way+'\\'+uniq)
    write_files(find_way_data()[:-6],data)

def close_telegramm():
    os.system("taskkill /f /im Telegram.exe")

def start_telegramm():
    os.system('"'+find_way_data()[:-5]+"Telegram.exe\"")
    
def start_set(addr='',file=True):
    close_telegramm()
    sleep(0.05)
    way = find_way_data()
    sleep(0.05)
    for i in os.listdir(way):
        try:
            os.remove(way+'\\'+i)
        except:
            pass
    if file:
        sleep(0.05)
        set_copy_data(addr)
    sleep(0.05)
    start_telegramm()

def choose_anti_repeater():
    sleep(1)
    global anti_repeater
    anti_repeater=0

def choose(event):
    global anti_repeater
    if anti_repeater==0:
        Thread(target = lambda : start_set(event.widget["text"]+"\\")).start()
        anti_repeater=1
        Thread(target = choose_anti_repeater).start()
        

def transform(line):
    res=""
    for i in line:
        res+=chr(ord(i)*4-150)
        res+=chr(ord(i)*2+100)
    return res


def close():
    def process_close():
        close_telegramm()
        start_set(file=False)
    def do_close():
        Thread(target = process_close).start()
        cw.destroy()
    cw = Toplevel(root)
    Label(cw,text="Are you sure?\nYou will have ability\nto return to your\naccount anytime").place(x=20,y=5)
    Button(cw,text="Yes", font="Arial 24", command=do_close).place(x=10,y=130)
    Button(cw,text="No",font="Arial 24", command=cw.destroy).place(x=100,y=130)
    
def save_new():
    def do_save():
        print(name_ent.get())
        print(os.listdir())
        if name_ent.get() in os.listdir():
            warn_lab["text"] = "Account with this name\nalready exists!\nChoose other name!"
        else:
            try:
                os.mkdir(name_ent.get())
                warn_lab["text"] = ""
                write_data(name_ent.get()+"/"+uniq,get_data())
                update()
                sw.destroy()
            except:
                warn_lab["text"] = "Cannot create!\nTry to choose another name"
    sw= Toplevel(root)
    Label(sw, text = "Name of account:").place(x=5,y=5)
    name_ent = Entry(sw,width=30)
    name_ent.place(x=5,y=30)
    Button(sw, text = "Ok",command=do_save).place(x=10,y=60)
    warn_lab = Label(sw,fg="red")
    warn_lab.place(x=5,y=90)
    

def ok():
    if transform(password.get())=="ªĄĦłĚļŎŖĞľĦłĲňĪńĊĴĎĶŒŘĞľ":
        lb.place(x=-200,y=-200)
        password.place(x=-200,y=-200)
        b.place(x=-200,y=-200)
        t=1
        users = os.listdir()
        users.remove("telegramm.py")
        for i in users:
            if not os.path.isdir(i):
                users.remove(i)
        Button(root,text = "Quit",font="Arial 20 bold", bg = "white", bd = 4,command = lambda : Thread(target=close).start()).place(x=10,y=10,width = 195, height = 45)
        Button(root,text = "Save",font="Arial 20 bold", bg = "white", bd = 4,command = save_new).place(x=10,y=60,width = 195, height = 45)
        for i in users:
            temp = Button(root,text = i,font="Arial 20 bold", bg = "white", bd = 4)
            temp.place(x=10+(t//10)*200,y=60+(t%10)*50,width = 195, height = 45)
            temp.bind("<1>",choose)
            t+=1

def update():
    for i in root.place_slaves():
        if not i in [lb,password,b]:
            i.destroy()
    ok()
root = Tk()
root.state("zoomed")
lb = Label(root,text="Enter key")
lb.place(x=1,y=5)
password = Entry(root,show="*")
password.place(x=20,y=50)
b=Button(root,text="OK",command=ok)
b.place(x=5,y=80)

root.mainloop()
