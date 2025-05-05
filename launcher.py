from pathlib import Path
from PIL import Image
from datetime import datetime
from roots import extractroots #.\roots.py
from astraparse import parse
import customtkinter as tk
import os
import psutil
import subprocess
import requests
import zipfile
import winreg as reg

def openrblx():
    localappdata = os.environ.get('LOCALAPPDATA')
    rblxpath = Path(localappdata) / 'Roblox'

    data = parse('.astra')
    theme = data['theme']
    launcherver = data['launcher_version']

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
    
    if Path(rblxpath).exists():

        # Kill Roblox
        for process in psutil.process_iter():
            if 'Roblox' in process.name():
                process.kill()
        
        def status(label, text):
            label.configure(text=text)

        response = requests.get('https://clientsettingscdn.roblox.com/v2/client-version/WindowsPlayer')

        if response.status_code == 200:
            data = response.json()

            version = data.get('clientVersionUpload', 'No version found')
            verpath = Path(rblxpath / 'Versions' / version)

            print(verpath)

            # Create window
            openapp = tk.CTkToplevel()
            openapp.title(f'Astra Launcher {launcherver}')
            openapp.geometry('350x200')
            openapp.resizable(False, False)
            openapp.configure(fg_color=foregroundclr)
            openapp.iconbitmap('logo.ico')

            logo = Image.open('logo.png')
            logotk = tk.CTkImage(light_image=logo, dark_image=logo, size=(80, 80))
            logolabel = tk.CTkLabel(openapp, image=logotk, text='')
            logolabel.pack(anchor='center', expand=True)

            statuslabel = tk.CTkLabel(openapp, text_color=uitheme, font=("Arial", 15), text='the window has just started')
            statuslabel.pack(anchor='center', expand=True)

            progress = tk.CTkProgressBar(openapp, width=300, height=20, mode='determinate')
            progress.pack(anchor='center', expand=True)
            progress.set(0)

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

                    status(statuslabel, f'Downloading {file}')
                    openapp.update()
                    response = requests.get(url)
                    print(response.status_code)
                    response.raise_for_status()

                    # Write
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

                            # Extract
                            with zipfile.ZipFile(zippath, 'r') as zip_file:
                                status(statuslabel, f'Extracting {zippath.name}')
                                openapp.update()
                                zip_file.extractall(extractdir)

                            progress.step()

                            zippath.unlink()

                    progress.step()

                status(statuslabel, 'Configuring Registry')
                openapp.update()

                # Configure registry
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

                status(statuslabel, 'Starting Roblox')
                progress.set(100)
                rblxapp = Path(verpath) / 'RobloxPlayerBeta.exe'
                subprocess.Popen([str(rblxapp), 'roblox-player:1+launchmode:app'])

                print('defined update')
            update()

            openapp.destroy()
