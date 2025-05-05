from pathlib import Path
from astraparse import parse
from tkinter import messagebox
import customtkinter as tk
import os
import sys
import requests
import psutil

def config():
    localappdata = os.environ.get('LOCALAPPDATA')
    rblxpath = Path(localappdata) / 'Roblox'

    data = parse('.astra')
    theme = data['theme']
    version = data['version']
    
    if Path(rblxpath).exists():
        response = requests.get('https://clientsettingscdn.roblox.com/v2/client-version/WindowsPlayer')

        if response.status_code == 200:
            data = response.json()

            version = data.get('clientVersionUpload', 'No version found')
            verpath = Path(rblxpath / 'Versions' / version)
            print(verpath)

            if Path(verpath).exists():
                
                #Create config UI
                
                configapp = tk.CTkToplevel()
                configapp.geometry('600x400')
                configapp.iconbitmap('logo.ico')
                configapp.title('Astra Configuration')

                if theme == 'Black':
                    print('dark')
                    uitheme = '#ffffff'
                    btntheme = '#828282'
                    btntxttheme = '#ffffff'
                    foregroundclr = '#1c1c1c'
                else:
                    print('light')
                    uitheme = '#000000'
                    btntheme = '#4a4a4a'
                    btntxttheme = '#ffffff'
                    foregroundclr = '#ffffff'

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
                fastflags = tabview.add('FastFlags')
                appearance = tabview.add('Appearance')
                mods = tabview.add('Mods')
                advanced = tabview.add('Advanced')

                addfastflag = tk.CTkButton(fastflags,text='Add FastFlag')
                addfastflag.place(y=20)

                removefastflag = tk.CTkButton(fastflags,text='Remove FastFlag')
                removefastflag.place(y=100)

                editfastflag = tk.CTkButton(fastflags,text='Edit FastFlag')
                editfastflag.place(y=180)

                fastflagview = tk.CTkScrollableFrame(fastflags,width=400,height=500)
                fastflagview.place(x=200,y=20)

                configapp.after(5,configapp.mainloop)
                    
            else:
                messagebox.showwarning('Error','Could not configure Roblox: Could not find Roblox installation')
            
        else:
            messagebox.showwarning('Error','Could not configure Roblox: Could not get latest version')
