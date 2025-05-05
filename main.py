from launcher import openrblx #.\launcher.py
from config import config #.\config.py
from astraparse import parse #.\astraparse.py
from PIL import ImageTk, Image
from tkinter import messagebox
import customtkinter as tk
import threading

# ---Create Window---

main = tk.CTk()
main.geometry('400x150')
main.resizable(False,False)
main.iconbitmap('logo.ico')
main.title('Astra')

# ---Handle Theme and Version---

data = parse('.astra')
theme = data['theme']
version = data['version']

if theme == "Black":
    main.configure(fg_color='#1c1c1c')
    
themes = {
    'Black': {
        'fg_color': '#1c1c1c',
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
main.configure(fg_color=theme_config['fg_color'])

logo = Image.open('logo.png')
logo_tk = tk.CTkImage(light_image=logo,dark_image=logo,size=(80,80))
logo_label = tk.CTkLabel(main, image = logo_tk,text='')
logo_label.place(x=250,y=35)

logo_text = tk.CTkLabel(main,text='Astra',text_color=theme_config['ui_color'],font=("Arial", 15))
ver_text = tk.CTkLabel(main,text=version,text_color=theme_config['ui_color'],font=("Arial", 15))
logo_text.place(x=345,y=50)
ver_text.place(x=345,y=75)

questionlabel = tk.CTkLabel(main,text='What would you like to do?',text_color=theme_config['ui_color'],font=("Arial", 17))
questionlabel.pack(anchor='nw', padx=5)

def startlauncher():
    main.withdraw()
    openrblx()

def startconfig():
    main.withdraw()
    config()

openroblox = tk.CTkButton(main, text='Open Roblox', width=16, fg_color=theme_config['btn_color'],text_color=theme_config['btn_text'],command=startlauncher)
openroblox.pack(anchor='nw', padx=10, pady=10)

configbutton = tk.CTkButton(main, text='Configure Roblox', width=16, fg_color=theme_config['btn_color'],text_color=theme_config['btn_text'],command=startconfig)
configbutton.pack(anchor='nw', padx=10, pady=10)

main.mainloop()
