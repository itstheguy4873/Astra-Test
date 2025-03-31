from PIL import ImageTk, Image
from pathlib import Path
from tkinter import messagebox
from datetime import datetime
import customtkinter as tk
import winreg as reg
import json
import requests
import os
import subprocess
import sys
import psutil
import time
import threading
import zipfile

#Create window

main = tk.CTk()
main.geometry('400x150')
main.resizable(False,False)
main.iconbitmap('logo.ico')
main.title('Astra')

#Set theme and get version

with open('.astra','r') as f:
    data = json.load(f)
    theme = data['theme']
    version = data['version']
    launcherver = data['launcher_version']
if theme == "black":
    main.configure(fg_color='#1c1c1c')
    
else:
    main.configure(fg_color='#ffffff')

#Create UI

if theme == 'black':
    uitheme = 'white'
    btntheme = '#828282'
    btntxttheme = 'white'
    foregroundclr = '#1c1c1c'
else:
    uitheme = 'black'
    btntheme = '#4a4a4a'
    btntxttheme = 'white'
    foregroundclr = '#ffffff'

logo = Image.open('logo.png')
logotk = tk.CTkImage(light_image=logo,dark_image=logo,size=(80,80))
logolabel = tk.CTkLabel(main, image = logotk,text='')
logolabel.place(x=250,y=35)

logotext = tk.CTkLabel(main,text='Astra',text_color=uitheme,font=("Arial", 15))
vertext = tk.CTkLabel(main,text=version,text_color=uitheme,font=("Arial", 15))
logotext.place(x=345,y=50)
vertext.place(x=345,y=75)

questionlabel = tk.CTkLabel(main,text='What would you like to do?',text_color=uitheme,font=("Arial", 17))
questionlabel.pack(anchor='nw', padx=5)

def openrblx():
    main.quit()
    main.destroy()
    
    localappdata = os.environ.get('LOCALAPPDATA')
    userpath = os.environ.get('USERPROFILE')
    rblxpath = Path(localappdata) / 'Roblox'
    
    
    if Path(rblxpath).exists():

        for process in psutil.process_iter():
            if 'Roblox' in process.name():
                process.kill()
        
        def status(label,text):
            label.after(0, lambda: label.configure(text=text))

        response = requests.get('https://clientsettingscdn.roblox.com/v2/client-version/WindowsPlayer')

        if response.status_code == 200:
            data = response.json()

            version = data.get('clientVersionUpload', 'No version found')
            verpath = Path(rblxpath / 'Versions' / version)
            
            print(verpath)
            
            openapp = tk.CTk()
            openapp.title(f'Astra Launcher {launcherver}')
            openapp.geometry('350x200')
            openapp.resizable(False,False)
            openapp.configure(fg_color=foregroundclr)
            openapp.iconbitmap('logo.ico')

            logo = Image.open('logo.png')
            logotk = tk.CTkImage(light_image=logo,dark_image=logo,size=(80,80))
            logolabel = tk.CTkLabel(openapp, image = logotk,text='')
            logolabel.pack(anchor='center',expand=True)

            statuslabel = tk.CTkLabel(openapp,text_color=uitheme,font=("Arial",15),text='the window has just started')
            statuslabel.pack(anchor='center',expand=True)

            progress = tk.CTkProgressBar(openapp, width = 300, height = 20,mode='determinate')
            progress.pack(anchor='center',expand=True)
            progress.set(0)

            if not Path(verpath).exists():
                status(statuslabel,'Creating Version Directory')
                verpath.mkdir(exist_ok=True)
            
            print('window created')
            
            def update():
                
                baseurl = f'https://setup.rbxcdn.com/{version}'

                extractroots = { #Thanks to Latte Softworks: https://github.com/latte-soft/rdd/
                    "RobloxApp.zip": "",
                    "RobloxPlayerInstaller.exe": "", #Needed so Roblox actually launches
                    "RobloxPlayerLauncher.exe": "", #Ditto
                    "redist.zip": "",
                    "shaders.zip": "shaders/",
                    "ssl.zip": "ssl/",

                    "WebView2.zip": "",
                    "WebView2RuntimeInstaller.zip": "WebView2RuntimeInstaller/",

                    "content-avatar.zip": "content/avatar/",
                    "content-configs.zip": "content/configs/",
                    "content-fonts.zip": "content/fonts/",
                    "content-sky.zip": "content/sky/",
                    "content-sounds.zip": "content/sounds/",
                    "content-textures2.zip": "content/textures/",
                    "content-models.zip": "content/models/",

                    "content-platform-fonts.zip": "PlatformContent/pc/fonts/",
                    "content-platform-dictionaries.zip": "PlatformContent/pc/shared_compression_dictionaries/",
                    "content-terrain.zip": "PlatformContent/pc/terrain/",
                    "content-textures3.zip": "PlatformContent/pc/textures/",

                    "extracontent-luapackages.zip": "ExtraContent/LuaPackages/",
                    "extracontent-translations.zip": "ExtraContent/translations/",
                    "extracontent-models.zip": "ExtraContent/models/",
                    "extracontent-textures.zip": "ExtraContent/textures/",
                    "extracontent-places.zip": "ExtraContent/places/"
                }

                for file, extractpath in extractroots.items():
                    url = f'{baseurl}-{file}'
                    print(url)

                    status(statuslabel, f'Downloading {file}')
                    response = requests.get(url)
                    print(response.status_code)
                    response.raise_for_status()
                    
                    if response.status_code == 200:
                        zippath = Path(verpath) / file
                        with open(zippath, 'wb') as f:
                            f.write(response.content)

                        if file.endswith('.exe'):
                            print(f'{file} is .exe file, will not extract')

                        elif file.endswith('.zip'):
                            extractdir = Path(verpath) / extractpath

                            extractdir.mkdir(parents=True,exist_ok=True)
                            print(extractdir)

                            with zipfile.ZipFile(zippath, 'r') as zip_file:
                                status(statuslabel,f'Extracting {zippath.name}')
                                zip_file.extractall(extractdir)
                                    
                            progress.step()

                            zippath.unlink()

                    progress.step()

                status(statuslabel,'Configuring Registry')

                clientexe = reg.CreateKey(reg.HKEY_CURRENT_USER,r'SOFTWARE\ROBLOX Corporation\Environments\roblox-player')
                reg.SetValueEx(clientexe,'clientExe',0,reg.REG_SZ,str(verpath / 'RobloxPlayerBeta.exe'))

                verkey = reg.CreateKey(reg.HKEY_CURRENT_USER,r'SOFTWARE\ROBLOX Corporation\Environments\roblox-player')
                reg.SetValueEx(verkey,'version',0,reg.REG_SZ,version)

                defkey = reg.CreateKey(reg.HKEY_CURRENT_USER,r'SOFTWARE\ROBLOX Corporation\Environments\roblox-player')
                reg.SetValueEx(defkey,None,0,reg.REG_SZ,str(verpath / 'RobloxPlayerInstaller.exe'))

                lockey = reg.CreateKey(reg.HKEY_CURRENT_USER,r'SOFTWARE\ROBLOX Corporation')
                reg.SetValueEx(lockey,'InstallLocation',0,reg.REG_SZ,str(verpath))

                timekey = reg.CreateKey(reg.HKEY_CURRENT_USER,r'SOFTWARE\Roblox\Retention')
                reg.SetValueEx(timekey,'LastRunDate',0,reg.REG_SZ,datetime.now().strftime("%Y%m%d"))

                icokey = reg.CreateKey(reg.HKEY_CURRENT_USER,r'SOFTWARE\ROBLOX Corporation\Environments\roblox-player\Capabilities')
                reg.SetValueEx(icokey,'ApplicationIcon',0,reg.REG_EXPAND_SZ,f'"{verpath / "RobloxPlayerInstaller.exe"}",0')
                
                status(statuslabel, 'Starting Roblox')
                progress.set(100)
                rblxapp = Path(verpath) / 'RobloxPlayerBeta.exe'
                subprocess.Popen([str(rblxapp),'roblox-player:1+launchmode:app'])
                
            print('defined update')
            
            def startupd():
                thread = threading.Thread(target=update)
                thread.daemon = True
                thread.start()

            if not verpath.exists():
                startupd()
                print('starting function')
            startupd()
            openapp.mainloop()

def config():
    localappdata = os.environ.get('LOCALAPPDATA')
    rblxpath = Path(localappdata) / 'Roblox'
    
    if Path(rblxpath).exists():
        response = requests.get('https://clientsettingscdn.roblox.com/v2/client-version/WindowsPlayer')

        if response.status_code == 200:
            data = response.json()

            version = data.get('clientVersionUpload', 'No version found')
            verpath = Path(rblxpath / 'Versions' / version)
            print(verpath)

            if Path(verpath).exists():
                
                #Create config UI
                
                configapp = tk.CTk()
                configapp.geometry('600x400')
                configapp.title('Astra Configuration')
                if theme == "black":
                    configapp.configure(fg_color='#1c1c1c')
    
                else:
                    configapp.configure(fg_color='#ffffff')

                if "RobloxPlayerBeta.exe" in (i.name() for i in psutil.process_iter()):
                    if not messagebox.askyesno('Warning', 'Roblox must be closed to edit settings.\nClose Roblox?',icon='error'):
                        sys.exit()
                    else:
                        pass

                for process in psutil.process_iter():
                    if 'Roblox' in process.name():
                        process.kill()
                
                tabview = tk.CTkTabview(configapp,fg_color=foregroundclr)
                tabview.pack(side='left', anchor='nw', fill='y', padx=10, pady=10)

                general = tabview.add('General')
                integrations = tabview.add('Integrations')
                appearance = tabview.add('Appearance')
                mods = tabview.add('Mods')
                advanced = tabview.add('Advanced')

                configapp.after(5,configapp.mainloop)
                    
            else:
                messagebox.showwarning('Error','Could not configure Roblox: Could not find Roblox installation')
            
        else:
            messagebox.showwarning('Error','Could not configure Roblox: Could not get latest version')

openroblox = tk.CTkButton(main, text='Open Roblox', width=16, fg_color=btntheme,text_color=btntxttheme, command=openrblx)
openroblox.pack(anchor='nw', padx=10, pady=10)

configbutton = tk.CTkButton(main, text='Configure Roblox', width=16, fg_color=btntheme,text_color=btntxttheme,command=config)
configbutton.pack(anchor='nw', padx=10, pady=10)

main.mainloop()
