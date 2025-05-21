from pathlib import Path
from astraparse import parse
from astraparse import write
from PIL import Image
from tkinter import messagebox
import customtkinter as tk
import os
import sys
import requests
import psutil

def config():
    localappdata = os.environ.get('LOCALAPPDATA')
    rblxpath = Path(localappdata) / 'Roblox'
    base = Path(getattr(sys,'_MEIPASS',Path(__file__).parent))
    
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
                
            # ---Create config UI--- #
                
            configapp = tk.CTkToplevel()
            configapp.geometry('600x400')
            configapp.iconbitmap('logo.ico')
            configapp.title('Astra Configuration')

            themes = {
            'Dark': {
                'fg_color': '#404040',
                'ui_color': '#ffffff',
                'btn_color': '#828282',
                'btn_text': '#ffffff'
            },
            'Light': {
                'fg_color': '#ffffff',
                'ui_color': '#000000',
                'btn_color': '#4a4a4a',
                'btn_text': '#ffffff'
                }
            }

            theme_config = themes.get(theme, themes['Light'])
            
            if theme == "Dark":
                logo = Image.open(str(base / 'astra-dark.png'))
                configapp.iconbitmap(str(base / 'astra-dark.ico'))
                configapp.configure(fg_color=theme_config['fg_color'])
            else:
                logo = Image.open(str(base / 'logo.png'))
                configapp.iconbitmap(str(base / 'logo.ico'))

            if "RobloxPlayerBeta.exe" in (i.name() for i in psutil.process_iter()):
                if not messagebox.askyesno('Warning', 'Roblox must be closed to edit settings.\nClose Roblox?',icon='error'):
                    sys.exit()
                else:
                    pass

            for process in psutil.process_iter():
                if 'Roblox' in process.name():
                    process.kill()

            # ---Tabview--- #
            
            tabview = tk.CTkTabview(configapp,fg_color=theme_config['fg_color'])
            tabview.pack(anchor='n')

            general = tabview.add('General')
            integrations = tabview.add('Integrations')
            fastflags = tabview.add('FastFlags')
            appearance = tabview.add('Appearance')
            mods = tabview.add('Mods')
            advanced = tabview.add('Advanced')

            def unsaved(callback):
                notification = tk.CTkFrame(configapp,corner_radius=16)
                notiftext = tk.CTkLabel(notification,text='Changes not saved',text_color='orange')
                notiftext.pack(side='left',padx=20)
                def savefunc():
                    callback()
                    notification.destroy()
                    
                savebutton = tk.CTkButton(notification,text='Save',command=savefunc)
                savebutton.pack(side='left',padx=20)
                notification.pack(side='bottom',fill='x',pady=5)

            fastflagview = tk.CTkScrollableFrame(fastflags,height=500)
            fastflagview.pack(side='right',fill='x')

            def addfastflagfunc():
                ff = tk.CTkFrame(fastflagview)
                ff.pack(side='left')
            
            addfastflag = tk.CTkButton(fastflags,text='Add FastFlag')
            addfastflag.place(y=20)

            removefastflag = tk.CTkButton(fastflags,text='Remove FastFlag')
            removefastflag.place(y=100)

            editfastflag = tk.CTkButton(fastflags,text='Edit FastFlag')
            editfastflag.place(y=180)

            # ---Appearance/Theme--- #

            appearanceview = tk.CTkScrollableFrame
            
            themeboxtext = tk.CTkLabel(appearance,text='App Theme',text_color=theme_config['ui_color'],font=("Segoe UI", 15))
            themeboxtext.pack()
            
            themebox = tk.CTkComboBox(appearance, values=['Light','Dark'],corner_radius=16,command=lambda: unsaved(addfastflagfunc))
            themebox.set(theme)
            themebox.pack()

            

            settings: {
                'theme': themebox,
                'fastflags': fastflagview
            }
            
            configapp.mainloop()
            
        else:
            messagebox.showwarning('Error','Could not configure Roblox: Could not get latest version')
