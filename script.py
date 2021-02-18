##############################################################################
"""-------------------------------------------------------------------------""
    Az OMSZ honlapjáról történő kompozit radarképek letöltése.
    A script bekéri a kezdő- és végidőpontot és letölti az
    elérhető radarképeket.
""-------------------------------------------------------------------------"""
##############################################################################

import datetime
import time
import os
import urllib.request
import sys

###############################################################################
global sdatetime
global edatetime
global datumkezdes
global datumvaltas

# Kezdődátum és intervallum bekérése


def script():

    sdatetime = [0,0,0,0,0]
    edatetime = [0,0,0,0,0]
    
    def inputok():

        try:
            sdatetime[0] = input('Letöltés kezdődátumának éve:     >>> ')
            sdatetime[1] = input('Letöltés kezdődátumának hónapja: >>> ')
            sdatetime[2] = input('Letöltés kezdődátumának napja:   >>> ')
            sdatetime[3] = input('Letöltés kezdődátumának órája:   >>> ')
            sdatetime[4] = input('Letöltés kezdődátumának perce:   >>> ')
            intervallum = input('Letöltési intervallum [nap] beállítása: (pl. "5" = 5 nap)   >>> ')
            c = int(intervallum)
            datetime.datetime(int(sdatetime[0]),int(sdatetime[1]),int(sdatetime[2]),int(sdatetime[3]),int(sdatetime[4]))
        except:
            (NameError, ValueError, TypeError)
            print('HIBA! A megadott dátum hibás!\n')
            inputok()
        starttime = datetime.datetime(int(sdatetime[0]),int(sdatetime[1]),int(sdatetime[2]),int(sdatetime[3]),int(sdatetime[4]))
        endtime = starttime + datetime.timedelta(days=c)  
        edatetime[0] = endtime.year
        edatetime[1] = endtime.month
        edatetime[2] = endtime.day
        edatetime[3] = endtime.hour
        edatetime[4] = endtime.minute

        sdatetime[0] = starttime.year
        sdatetime[1] = starttime.month
        sdatetime[2] = starttime.day
        sdatetime[3] = starttime.hour
        sdatetime[4] = starttime.minute

    datumkezdes = datetime.datetime(2011,12,30,12,30)
    datumvaltas = datetime.datetime(2014,4,2,10,0)

    def check():
        try:
            datetime.datetime(int(sdatetime[0]),int(sdatetime[1]),int(sdatetime[2]),int(sdatetime[3]),int(sdatetime[4]))
            datetime.datetime(int(edatetime[0]),int(edatetime[1]),int(edatetime[2]),int(edatetime[3]),int(edatetime[4]))
        except:
            (NameError, ValueError, TypeError)
            print('HIBA! A megadott dátum hibás!\n')
            inputok()
        if datetime.datetime(int(sdatetime[0]),int(sdatetime[1]),int(sdatetime[2]),int(sdatetime[3]),int(sdatetime[4])) < datumkezdes:
            sdatetime[0] = 2011
            sdatetime[1] = 12
            sdatetime[2] = 30
            sdatetime[3] = 12
            sdatetime[4] = 30
            print('A kezdődátum beállítva: 2011-12-30 12:30')
        if datetime.datetime(int(sdatetime[0]),int(sdatetime[1]),int(sdatetime[2]),int(sdatetime[3]),int(sdatetime[4])) > datetime.datetime.now():
            inputok()
        if datetime.datetime(int(edatetime[0]),int(edatetime[1]),int(edatetime[2]),int(edatetime[3]),int(edatetime[4])) > datetime.datetime.now():
            edatetime[0] = datetime.datetime.now().year
            edatetime[1] = datetime.datetime.now().month
            edatetime[2] = datetime.datetime.now().day
            edatetime[3] = datetime.datetime.now().hour
            edatetime[4] = datetime.datetime.now().minute
            print('A végdátum beállítva: {}-{}-{} {}:{}'.format(edatetime[0],str(edatetime[1]).zfill(2),str(edatetime[2]).zfill(2),str(edatetime[3]).zfill(2),str(edatetime[4]//10*10).zfill(2)))
        if datetime.datetime(int(sdatetime[0]),int(sdatetime[1]),int(sdatetime[2]),int(sdatetime[3]),int(sdatetime[4])) < datumvaltas:
            sdatetime[4] = sdatetime[4]//15*15
        else:
            sdatetime[4] = sdatetime[4]//10*10
        if datetime.datetime(int(edatetime[0]),int(edatetime[1]),int(edatetime[2]),int(edatetime[3]),int(edatetime[4])) < datumvaltas:
            edatetime[4] = edatetime[4]//15*15
        else:
            edatetime[4] = edatetime[4]//10*10

    def download():
        print('\nKezdődátum: {}-{}-{} {}:{}'.format(str(sdatetime[0]),str(sdatetime[1]).zfill(2),str(sdatetime[2]).zfill(2),str(sdatetime[3]).zfill(2),str(sdatetime[4]).zfill(2)))
        print('Végdátum: {}-{}-{} {}:{}'.format(str(edatetime[0]),str(edatetime[1]).zfill(2),str(edatetime[2]).zfill(2),str(edatetime[3]).zfill(2),str(edatetime[4]).zfill(2)))
        
        urllista = []
        fajlnevlista = []
        dt = datetime.datetime(sdatetime[0],sdatetime[1],sdatetime[2],sdatetime[3],sdatetime[4])
        while dt <= datetime.datetime(edatetime[0],edatetime[1],edatetime[2],edatetime[3],edatetime[4]):
            urllista.append('http://www.metnet.hu/img/radar/'+str(dt.year)+'/'+str(dt.month).zfill(2)+'/'+str(dt.day).zfill(2)+'/Rccw'+str(dt.year)+str(dt.month).zfill(2)+str(dt.day).zfill(2)+'_'+str(dt.hour).zfill(2)+str(dt.minute).zfill(2)+'.jpg')
            fajlnevlista.append('Rccw'+str(dt.year)+str(dt.month).zfill(2)+str(dt.day).zfill(2)+'_'+str(dt.hour).zfill(2)+str(dt.minute).zfill(2)+'.jpg')
            if dt < datumvaltas:
                dt += datetime.timedelta(minutes=15)
            else:
                dt += datetime.timedelta(minutes=10)
        # Letöltési mappa létrehozása
        mappanev = 'radar'
        try:
            if not os.path.exists(mappanev):
                os.makedirs(mappanev)
        except:
            OSError
            print('A mappát nem sikerült létrehozni: '+mappanev)
    
        print('{} db kép kerül letöltésre.\n'.format(len(urllista)))
        print('>>> A letöltés elkezdődött...\n')

        # A képek letöltése!!!
        szazalek = []
        log = []
        nonlog = []
        time = []
        szamlalo = 0
        time.append(datetime.datetime.now())
        for i in range(0, len(urllista)-1):
            url = str(urllista[i])
            brokenurl = 0
            filename = str(mappanev+'/'+fajlnevlista[i])
            if os.path.exists(filename):
                log.append(fajlnevlista[i])
                brokenurl = 1
                if (round(i/len(urllista)*100))%5 == 0:
                    szazalek.append(round(i/len(urllista)*100))
                    szamlalo += 1
                    if len(szazalek)>1 and szazalek[szamlalo-1] != szazalek[szamlalo-2]:
                        time.append(datetime.datetime.now())
                        t = (time[len(time)-1]-time[0]) * ((len(urllista)-i)/i)
                        tnow = str(datetime.datetime.now().hour).zfill(2)+':'+str(datetime.datetime.now().minute).zfill(2)+':'+str(datetime.datetime.now().second).zfill(2)
                        print('> {}% letöltve...   > {} > Becsült hátralevő idő: {}'.format(round(i/len(urllista)*100),tnow,t))
            try:
                response = urllib.request.urlopen(url)
                image_data = response.read()
            except:
                brokenurl = 1
                if (round(i/len(urllista)*100))%5 == 0:
                    szazalek.append(round(i/len(urllista)*100))
                    szamlalo += 1
                    if len(szazalek)>1 and szazalek[szamlalo-1] != szazalek[szamlalo-2]:
                        time.append(datetime.datetime.now())
                        t = (time[len(time)-1]-time[0]) * ((len(urllista)-i)/i)
                        tnow = str(datetime.datetime.now().hour).zfill(2)+':'+str(datetime.datetime.now().minute).zfill(2)+':'+str(datetime.datetime.now().second).zfill(2)
                        print('> {}% letöltve...   > {} > Becsült hátralevő idő: {}'.format(round(i/len(urllista)*100),tnow,t))
            if brokenurl == 0:
                urllib.request.urlretrieve(url, filename)
                if (round(i/len(urllista)*100))%5 == 0:
                    szazalek.append(round(i/len(urllista)*100))
                    szamlalo += 1
                    if len(szazalek)>1 and szazalek[szamlalo-1] != szazalek[szamlalo-2]:
                        time.append(datetime.datetime.now())
                        t = (time[len(time)-1]-time[0]) * ((len(urllista)-i)/i)
                        tnow = str(datetime.datetime.now().hour).zfill(2)+':'+str(datetime.datetime.now().minute).zfill(2)+':'+str(datetime.datetime.now().second).zfill(2)
                        print('> {}% letöltve...   > {} > Becsült hátralevő idő: {}'.format(round(i/len(urllista)*100),tnow,t))
        print('>   100% letöltve!')
        print('\n>>> A letöltés befejeződött!\n')
        print('\nKorábban letöltött fájlok:')
        print(*log, sep='\n')
        print('\nNem elérhető fájlok:')
        print(*nonlog, sep='\n')
        script()

    inputok()
    check()
    download()
script()
