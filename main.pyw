from launcher import openrblx #.\launcher.py
from config import config #.\config.py
from astraparse import parse #.\astraparse.py
from PIL import ImageTk, Image
from pathlib import Path
from tkinter import messagebox
from customtkinter import set_appearance_mode
import customtkinter as tk
import subprocess
import threading
import sys

# ---Create Window--- #

main = tk.CTk()
main.geometry('400x150')
main.resizable(False,False)
main.title('Astra')

base = Path(getattr(sys,'_MEIPASS',Path(__file__).parent))

# ---Handle Theme and Version--- #

data = parse(base / '.astra')
theme = data['theme']
version = data['version']

if theme == "Dark":
    logo = Image.open(str(base / 'astra-dark.png'))
    main.iconbitmap(str(base / 'astra-dark.ico'))
    set_appearance_mode('dark')
else:
    logo = Image.open(str(base / 'logo.png'))
    main.iconbitmap(str(base / 'logo.ico'))
    
themes = {
    'Dark': {
        'fg_color': '#404040',
        'ui_color': '#ffffff',
        'btn_color': '#828282',
        'btn_text': '#ffffff',
        'logo': 'astra-dark.ico'
    },
    'Light': {
        'fg_color': '#ffffff',
        'ui_color': '#000000',
        'btn_color': '#4a4a4a',
        'btn_text': '#ffffff',
        'logo': 'logo.ico'
    }
}

theme_config = themes.get(theme, themes['Light'])
main.configure(fg_color=theme_config['fg_color'])

logo_tk = tk.CTkImage(light_image=logo,dark_image=logo,size=(80,80))
logo_label = tk.CTkLabel(main, image = logo_tk,text='')
logo_label.place(x=250,y=35)

logo_text = tk.CTkLabel(main,text='Astra',text_color=theme_config['ui_color'],font=("Segoe UI", 15))
ver_text = tk.CTkLabel(main,text=version,text_color=theme_config['ui_color'],font=("Segoe UI", 15))
logo_text.place(x=345,y=50)
ver_text.place(x=345,y=75)

questionlabel = tk.CTkLabel(main,text='What would you like to do?',text_color=theme_config['ui_color'],font=("Segoe UI", 17))
questionlabel.pack(anchor='nw', padx=5)

def startlauncher():
    main.withdraw()
    openrblx()

def startconfig():
    main.withdraw()
    config()

openroblox = tk.CTkButton(main, text='Open Roblox', width=16, fg_color=theme_config['btn_color'],text_color=theme_config['btn_text'],font=("Segoe UI", 13),corner_radius=16,command=startlauncher)
openroblox.pack(anchor='nw', padx=10, pady=10)

configbutton = tk.CTkButton(main, text='Configure Roblox', width=16, fg_color=theme_config['btn_color'],text_color=theme_config['btn_text'],font=("Segoe UI", 13),corner_radius=16,command=startconfig)
configbutton.pack(anchor='nw', padx=10, pady=10)

main.mainloop()
