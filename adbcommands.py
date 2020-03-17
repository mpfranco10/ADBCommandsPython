# -*- coding: utf-8 -*-
import os
import time
# path for the adb which come with NOX emulator.
path = "C:\\Users\\mapau\\AppData\\Local\\Android\\Sdk\\platform-tools"
apkpath = "D:\\Moviles\\ADB\\talkingtom.apk"
pathcomandos = "D:\\Moviles\\ADB\\commandList.txt"
rutabase = "D:\\Moviles\\ADB\\"

#numero de eventos en los que se va a saltar
X = 8
N = 10 #numero de eventos que se van a hacer

def takeScreenshoot(name: str) -> str:
    os.popen("adb shell screencap -p /sdcard/" + name + '.png').read()
    os.popen("adb pull /sdcard/"+name+".png "+rutabase+"tmp\\"+name+".png").read()
    os.popen("adb shell rm /sdcard/" + name + '.png').read()
    return rutabase + "tmp\\"+name+".png"

def itemHtml(descr:str, comandos, imgs) -> str:
    imgscontainer = ""
    for img in imgs:
        imgscontainer += """ <div class="col-sm">  <img width="290px" height="600px" src='"""+ img+ """' alt="command"> </div> """
    comscon = ""
    for c in comandos:
        comscon += "<p>"+c+"</p>"
    html = """
        <h1>Description: """+ descr+ """</h2>
       """+ comscon+ """ <hr> <div class="row">
        """+imgscontainer+"""
        </div>
        """
    return html

# Change the directory to it.
os.chdir(path)
html = ""
# checking for connected devices
device = os.popen("adb devices").read().split('\n', 1)[1].split("device")[0].strip()
# connect to the selected device 172.0.0.1:62001
print("Waiting for connection ...")
connect = os.popen("adb connect " + device ).read()

#Instalar app
print("Se instalara la app")
os.system("adb install " + apkpath)
time.sleep(5)
print("Abriendo talking tom")
os.popen("adb shell monkey -p com.outfit7.mytalkingtomfree -v 500").read()
html += itemHtml("Abrir talking Tom", ["adb shell monkey -p com.outfit7.mytalkingtomfree -v 500"], [takeScreenshoot("tom")])
time.sleep(7)
print("Inicio de comandos")

numevento = 0
# Strips the newline character 
while numevento <= N:
    
    file1 = open(pathcomandos, 'r') 
    Lines = file1.readlines() 
    i = 0
    currentimgs = []
    currentdes = ""
    currentcmds = []

    
    for line in Lines: 
        if 'D:' in line:
            if i!=0:
                html += itemHtml(currentdes, currentcmds, currentimgs)
                currentcmds = []
                currentimgs = []
            des  = line.split(':')
            currentdes = des[1] 
            numevento += 1 #ya termine 1 evento
            if numevento % X == 0: #hacemos back cada X eventos :)
                os.popen("adb shell input keyevent 4").read()
            if numevento > N:
                break
        else:
            print("Comando a ejecutar" + line)
            time.sleep(2)
            rta = os.popen(line).read()
            ruta = takeScreenshoot(str(i))
            currentimgs.append(ruta)
            if "battery" in line:
                line += "- Respuesta: "+ rta
            currentcmds.append(line)
            i+=1 #para poder tomar pantallazo
        
initial_html = open(rutabase + "template.txt", "r").read()
ending =  open(rutabase + "endtemplate.txt", "r").read()
total = initial_html + html + ending
    
#Desinstalar la app
os.system("adb uninstall com.outfit7.mytalkingtomfree")

Html_file= open(rutabase + "prueba.html","w")
Html_file.write(total)
Html_file.close()