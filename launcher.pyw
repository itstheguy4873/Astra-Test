from pathlib import Path
from PIL import Image
from datetime import datetime
from roots import extractroots #.\roots.py
from astraparse import parse
import customtkinter as tk
import threading
import os
import psutil
import subprocess
import requests
import zipfile
import sys
import winreg as reg

def openrblx():
    
    localappdata = os.environ.get('LOCALAPPDATA')
    rblxpath = Path(localappdata) / 'Roblox'

    base = Path(getattr(sys,'_MEIPASS',Path(__file__).parent))

    data = parse(base / '.astra')
    theme = data['theme']
    launcherver = data['launcher_version']
    
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
        
    if Path(rblxpath).exists():

        # ---Kill Roblox---
            
        for process in psutil.process_iter():
            if 'Roblox' in process.name():
                process.kill()
            
        def status(label, text):
            label.after(0, lambda: label.configure(text=text))

        response = requests.get('https://clientsettingscdn.roblox.com/v2/client-version/WindowsPlayer')

        if response.status_code == 200:
            data = response.json()

            version = data.get('clientVersionUpload', 'No version found')
            verpath = Path(rblxpath / 'Versions' / version)

            print(verpath)

            # ---Create Window---

            theme_config = themes.get(theme, themes['Light'])
               
            openapp = tk.CTkToplevel()
            openapp.title(f'Astra Launcher {launcherver}')
            openapp.geometry('350x200')
            openapp.resizable(False, False)
            openapp.configure(fg_color=theme_config['fg_color'])
            openapp.iconbitmap(str(base / 'logo.ico'))

            if theme == "Dark":
                logo = Image.open(str(base / 'astra-dark.png'))
                openapp.iconbitmap(str(base / 'astra-dark.ico'))
                openapp.configure(fg_color=theme_config['fg_color'])
            else:
                logo = Image.open(str(base / 'logo.png'))
                openapp.iconbitmap(str(base / 'logo.ico'))
            
            logotk = tk.CTkImage(light_image=logo, dark_image=logo, size=(80, 80))
            logolabel = tk.CTkLabel(openapp, image=logotk, text='')
            logolabel.pack(anchor='center', expand=True)

            statuslabel = tk.CTkLabel(openapp, text_color=theme_config['ui_color'], font=("Arial", 15), text='The window has just started')
            statuslabel.pack(anchor='center', expand=True)

            progress = tk.CTkProgressBar(openapp, width=300, height=20, mode='determinate')
            progress.pack(anchor='center', expand=True)
            progress.set(0)
                
            status(statuslabel, 'Establishing Toplevel')
            openapp.update()

            if not Path(verpath).exists():
                status(statuslabel, 'Creating Version Directory')
                openapp.update()
                verpath.mkdir(exist_ok=True)

            print('window created')

            def update():

                baseurl = f'https://setup.rbxcdn.com/{version}'

                for file, extractpath in extractroots.items():

                    url = f'{baseurl}-{file}'
                    print(url)
                    openapp.update()

                    status(statuslabel, f'Downloading {file}')
                    openapp.update()
                    response = requests.get(url)
                    print(response.status_code)
                    response.raise_for_status()

                    # ---Write---
                        
                    if response.status_code == 200:
                        zippath = Path(verpath) / file
                        with open(zippath, 'wb') as f:
                            f.write(response.content)

                        if file.endswith('.exe'):
                            print(f'{file} is .exe file, will not extract')

                        elif file.endswith('.zip'):
                            extractdir = Path(verpath) / extractpath

                            extractdir.mkdir(parents=True, exist_ok=True)
                            print(extractdir)

                            # ---Extract---
                                
                            with zipfile.ZipFile(zippath, 'r') as zip_file:
                                status(statuslabel, f'Extracting {zippath.name}')
                                openapp.update()
                                zip_file.extractall(extractdir)

                            progress.after(0, lambda: progress.step())

                            zippath.unlink()

                    progress.after(0, lambda: progress.step())

                status(statuslabel, 'Configuring Registry')
                openapp.update()

                # ---Configure Registry---
                    
                clientexe = reg.CreateKey(reg.HKEY_CURRENT_USER, r'SOFTWARE\ROBLOX Corporation\Environments\roblox-player')
                reg.SetValueEx(clientexe, 'clientExe', 0, reg.REG_SZ, str(verpath / 'RobloxPlayerBeta.exe'))

                verkey = reg.CreateKey(reg.HKEY_CURRENT_USER, r'SOFTWARE\ROBLOX Corporation\Environments\roblox-player')
                reg.SetValueEx(verkey, 'version', 0, reg.REG_SZ, version)

                defkey = reg.CreateKey(reg.HKEY_CURRENT_USER, r'SOFTWARE\ROBLOX Corporation\Environments\roblox-player')
                reg.SetValueEx(defkey, None, 0, reg.REG_SZ, str(verpath / 'RobloxPlayerInstaller.exe'))

                lockey = reg.CreateKey(reg.HKEY_CURRENT_USER, r'SOFTWARE\ROBLOX Corporation')
                reg.SetValueEx(lockey, 'InstallLocation', 0, reg.REG_SZ, str(verpath))

                timekey = reg.CreateKey(reg.HKEY_CURRENT_USER, r'SOFTWARE\Roblox\Retention')
                reg.SetValueEx(timekey, 'LastRunDate', 0, reg.REG_SZ, datetime.now().strftime("%Y%m%d"))

                icokey = reg.CreateKey(reg.HKEY_CURRENT_USER, r'SOFTWARE\ROBLOX Corporation\Environments\roblox-player\Capabilities')
                reg.SetValueEx(icokey, 'ApplicationIcon', 0, reg.REG_EXPAND_SZ, f'"{verpath / "RobloxPlayerInstaller.exe"}",0')

                urikey = reg.OpenKeyEx(reg.HKEY_CURRENT_USER, r'SOFTWARE\Classes\roblox-player\shell\open\command', 0, reg.KEY_SET_VALUE)
                reg.SetValueEx(urikey, '', 0, reg.REG_SZ, f'"{sys.argv[0]}" %1')

                status(statuslabel, 'Starting Roblox')
                progress.after(0, lambda: progress.set(100))

                if len(sys.argv) > 1:
                    subprocess.Popen([str(verpath / 'RobloxPlayerBeta.exe')] + sys.argv[1:])
                    print(sys.argv[1])
                    
                else:
                    subprocess.Popen([str(verpath / 'RobloxPlayerBeta.exe')])

                openapp.after(0, openapp.destroy)

                print('defined update')
            threading.Thread(target=update, daemon=True).start()
