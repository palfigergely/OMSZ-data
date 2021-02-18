##############################################################################
"""-------------------------------------------------------------------------""
    Az OMSZ honlapjáról történő kompozit radarképek letöltése.
    A script bekéri a kezdő időpontot és a megadott időtől letölti az
    elérhető radarképeket (vagy az aktuális dátumig vagy a megadottig).
""-------------------------------------------------------------------------"""
##############################################################################

# --- Az aktuális dátum definiálása ---#
import datetime
now = datetime.datetime.now()
cdatetime = [now.year, now.month, now.day, now.hour, now.minute]

###############################################################################
# --- GUI --#
from tkinter import Tk, Entry, Button, INSERT, Label, Text, Scrollbar
root = Tk()

# Ablak fejléce
root.title("OMSZ KOMPOZIT RADARKÉP LETÖLTÉSE")

# Utasítás szöveg megadása
label = Label(root, text='\n Add meg a kezdő- és végdátumot a letöltéshez! \nA kezdő dátum nem lehet 2011.12.30. 12:30-nál korábbi! \nA radarképek minden egész 10 percben érhetők\nel 2014.04.02. 10:00-tól (előtte 15p-ként)! \n')
label.grid(row=1, column=1, columnspan=10)
label.config(foreground='black') 

# Ablak mérete
root.maxsize(430,500)
root.minsize(430,500)

# Input szövegdobozok és feliratok
w_entry=6
justify_entry='right'

label_k = Label(root, text='Kezdő dátum:')
text1 = Label(root, text='Év / Hónap / Nap ')
entry1= Entry(root, width=w_entry, justify=justify_entry)
entry2= Entry(root, width=w_entry, justify=justify_entry)
entry3= Entry(root, width=w_entry, justify=justify_entry)
text2 = Label(root, text='Óra / Perc ')
entry4= Entry(root, width=w_entry, justify=justify_entry)
entry5= Entry(root, width=w_entry, justify=justify_entry)

label_v = Label(root, text='\nVégdátum:')
text3 = Label(root, text='Év / Hónap / Nap ')
entry11= Entry(root, width=w_entry, justify=justify_entry)
entry12= Entry(root, width=w_entry, justify=justify_entry)
entry13= Entry(root, width=w_entry, justify=justify_entry)
text4 = Label(root, text='Óra / Perc ')
entry14= Entry(root, width=w_entry, justify=justify_entry)
entry15= Entry(root, width=w_entry, justify=justify_entry)

# Input szövegdobozok és feliratok elhelyezkedése
label_k.grid(row=2, column=1, columnspan=8)

text1.grid(row=3,column=1)
entry1.grid(row=3, column=2)
entry2.grid(row=3, column=3)
entry3.grid(row=3, column=4)
text2.grid(row=4,column=1)
entry4.grid(row=4, column=2)
entry5.grid(row=4, column=3)

label_v.grid(row=5, column=1, columnspan=8)

text3.grid(row=6,column=1)
entry11.grid(row=6, column=2)
entry12.grid(row=6, column=3)
entry13.grid(row=6, column=4)
text4.grid(row=7,column=1)
entry14.grid(row=7, column=2)
entry15.grid(row=7, column=3)

# Üres sorok
emptyrow1 = Label(root, text='\n', height=1)
emptyrow1.grid(row=8, column=1)
emptyrow2 = Label(root, text='\n', height=1)
emptyrow2.grid(row=10, column=1)

# Input szövegdobozok 'default' értékei
entry1.insert(INSERT, str(cdatetime[0]))
entry2.insert(INSERT, '1')
entry3.insert(INSERT, '1')
entry4.insert(INSERT, str(cdatetime[3]))
entry5.insert(INSERT, str(cdatetime[4]//10*10))

# Inputok ELLENŐRZÉSE
def check():
    global sdatetime
    global edatetime
    global logtxt
    global errorindicator
    errorindicator=0
    try:
        sdatetime = [int(entry1.get()),int(entry2.get()),int(entry3.get()),int(entry4.get()),((int(entry5.get())//10)*10)]
        edatetime = [int(entry11.get()),int(entry12.get()),int(entry13.get()),int(entry14.get()),((int(entry15.get())//10)*10)]
    except (NameError, ValueError, TypeError):
        logtxt = logtxt + '\n> HIBA! A megadott dátum hibás formátumban van!'
        logtxt = logtxt + '\n  Kezdődátum: '+ entry1.get()+'-'+entry2.get()+'-'+entry3.get()+' '+entry4.get()+':'+entry5.get()
        logtxt = logtxt + '\n  Végdátum: '+ entry11.get()+'-'+entry12.get()+'-'+entry13.get()+' '+entry14.get()+':'+entry15.get()
        errorindicator=1
        
    # Inputok változókba helyezése
    dlimit = datetime.datetime(2014,4,2,10,0)
    if errorindicator==0:
        if datetime.datetime(int(entry1.get()),int(entry2.get()),int(entry3.get()),int(entry4.get()),int(entry5.get())) >= dlimit:
            sdatetime = [int(entry1.get()),int(entry2.get()),int(entry3.get()),int(entry4.get()),((int(entry5.get())//10)*10)]
            edatetime = [int(entry11.get()),int(entry12.get()),int(entry13.get()),int(entry14.get()),((int(entry15.get())//10)*10)]
        else:
            sdatetime = [int(entry1.get()),int(entry2.get()),int(entry3.get()),int(entry4.get()),((int(entry5.get())//15)*15)]
            edatetime = [int(entry11.get()),int(entry12.get()),int(entry13.get()),int(entry14.get()),((int(entry15.get())//15)*15)]
    else:
        None
    log()

##############################################################################
# Gombnyomáshoz tartozó utasítás
def buttondownload():
    import urllib.request
    import os
    global logtxt
    check()
    if errorindicator==0:
        logtxt = logtxt + '\nKezdődátum: '+str(datetime.datetime(sdatetime[0],sdatetime[1],sdatetime[2],sdatetime[3],sdatetime[4]))
        logtxt = logtxt + '\nVégdátum: '+str(datetime.datetime(edatetime[0],edatetime[1],edatetime[2],edatetime[3],edatetime[4]))
        logtxt = logtxt + '\nA LETÖLTÉS ELKEZDŐDÖTT!'
    log()
    urllista = []
    fajlnevlista = []
    dt = datetime.datetime(sdatetime[0],sdatetime[1],sdatetime[2],sdatetime[3],sdatetime[4])
    dlimit = datetime.datetime(2014,4,2,10,0)
    while dt <= datetime.datetime(edatetime[0],edatetime[1],edatetime[2],edatetime[3],edatetime[4]):
        urllista.append('http://www.metnet.hu/img/radar/'+str(dt.year)+'/'+str(dt.month).zfill(2)+'/'+str(dt.day).zfill(2)+'/Rccw'+str(dt.year)+str(dt.month).zfill(2)+str(dt.day).zfill(2)+'_'+str(dt.hour).zfill(2)+str(dt.minute).zfill(2)+'.jpg')
        fajlnevlista.append('Rccw'+str(dt.year)+str(dt.month).zfill(2)+str(dt.day).zfill(2)+'_'+str(dt.hour).zfill(2)+str(dt.minute).zfill(2)+'.jpg')
        if dt < dlimit:
            dt += datetime.timedelta(minutes=15)
        else:
            dt += datetime.timedelta(minutes=10)
    # Letöltési mappa létrehozása
    mappanev = 'radar'
    try:
        if not os.path.exists(mappanev):
            os.makedirs(mappanev)
    except OSError:
        print('A mappát nem sikerült létrehozni: '+mappanev)
    # A képek letöltése!!!
    for i in range(0, len(urllista)-1):
        url = str(urllista[i])
        filename = str(mappanev+'/'+fajlnevlista[i])
        if os.path.exists(filename):
            logtxt = logtxt + '\n' + filename + 'már letöltve!'
            log()
            return
        # try:
        #     response = request.urlopen(url)
        #     image_data = response.read()
        # except:
        #     logtxt = logtxt + '\nNem elérhető: '+ urllista[i]
        #     log()
        urllib.request.urlretrieve(url, filename)
    logtxt = logtxt + '\nA LETÖLTÉS KÉSZ!'
    log()
          
def buttoncurrentdate():
    now = datetime.datetime.now()
    cdatetime = [now.year, now.month, now.day, now.hour, now.minute]
    
    entry11.delete(0,'end')
    entry12.delete(0,'end')
    entry13.delete(0,'end')
    entry14.delete(0,'end')
    entry15.delete(0,'end')
        
    entry11.insert(INSERT, str(cdatetime[0]))
    entry12.insert(INSERT, str(cdatetime[1]))
    entry13.insert(INSERT, str(cdatetime[2]))
    entry14.insert(INSERT, str(cdatetime[3]))
    entry15.insert(INSERT, str(cdatetime[4]//10*10))

def buttonexit():
    root.destroy()

# A "Letöltés" gomb
buttonL = Button(root, text='Letöltés', bg='gainsboro', command=buttondownload)
buttonL.grid(row=3, column=9, rowspan=2)
buttonL.config(height = 1, width = 8)

# A "Mai dátum" gomb
buttonD = Button(root, text='Mai dátum', bg='gainsboro', command=buttoncurrentdate)
buttonD.grid(row=6, column=9, rowspan=2)
buttonD.config(height = 1, width = 8)

# Az "EXIT" gomb
buttonX = Button(root, text='Kilépés', bg='gainsboro', command=buttonexit)
buttonX.grid(row=11, column=1, columnspan=9)
buttonX.config(height = 1, width = 9)

#LOG text
def log():
    log=Text(root, width=50, height=10)
    log.insert('end', logtxt)
    scroll = Scrollbar(root)
    scroll.config(command=log.yview)
    log.config(yscrollcommand=scroll.set, state='disabled')
    log.grid(row = 9, column = 1, columnspan = 9)
    scroll.grid(row = 9, column = 10, sticky='NSE')
    log.yview_pickplace('end')
    
logtxt = 'A letöltéshez kattints a [Letöltés] gombra!'

log()
buttoncurrentdate()

#Ablak megjelenítése 
root.mainloop()
