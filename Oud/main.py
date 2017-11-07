# -*- coding: utf-8 -*-
"""
Created on Mon Aug 21 22:13:00 2017

@author: Coen.Smits
"""

"""
Om te converteren: 
    bestanden kopieren naar C:/Python
    cmd prompt openen en naar deze map gaan
    'activate main' typen
    'pyton setup.py py2exe' typen
    includes map en defaults.setup naar dist kopieren
    klaar
"""

from fwdconvert import conversion
from fwdconvert import getDefaults

import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilenames

root = tk.Tk()   

#This is where we lauch the file manager bar.
def OpenFile():
    CROW_factor, last_Location = getDefaults()
    files = askopenfilenames(initialdir = last_Location,
                           filetypes =(("fwd files", "*.fwd"),("All Files","*.*")),
                           title = "Choose a file."
                           )
    fileList = root.tk.splitlist(files)
    print (fileList)
    
    #Using try in case user types in unknown file or closes without choosing a file.
    try:
        for i in range(0,len(fileList)):
            with open(fileList[i],'r'):
                conversion(fileList[i], CROW_factor) 
    except:
        print("No file exists")  
        

CROW_factor, last_Location = getDefaults()

Title = root.title( "Unihorn .fwd to .f25 converter tool")
root.minsize(400,200)
label = ttk.Label(root, text ="CROW Factor: " + str(CROW_factor),foreground="Black",font=("Helvetica", 10))
#label.grid(row=1)
#e1 = ttk.Entry(root)
#e1.grid(row=1, column=1)
#e1.insert(0, CROW_factor)


label.pack()
#e1.pack()


#Menu Bar

menu = tk.Menu(root)
root.config(menu=menu)
root.iconbitmap('includes/Icon1.ico')

file = tk.Menu(menu, tearoff=False)

file.add_command(label = 'Open', command = OpenFile)
#file.add_command(label = 'Exit', command = lambda:exit())

menu.add_cascade(label = 'File', menu = file)

root.mainloop()