import tkinter as tk
import twofa
import chromeActions
# import tkinter module
from tkinter import * 
from tkinter.ttk import *

from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys

chromeActions.login()





searchButtonHasBeenPressed = FALSE
parts = dict()
def getTicketInfo(ticketNum):
    global searchButtonHasBeenPressed 
    if searchButtonHasBeenPressed:
        deletePartBoxes()

    #ticketInfo=[ticketID, deviceName, parts, btnCats]
    info = chromeActions.getTicketInfo(ticketNum)
    ticketID = info[0]
    deviceName = info[1]
    parts = info[2]
    btnCats = info[3]
    print("Before make boxes:" + str(btnCats))

    makePartBoxes(btnCats) # Makes checkboxes from part categories

    l2.configure(text = "Searched: " + ticketNum)
    l3.configure(text = "Device: " + deviceName)
    l4.configure(text = "Ticket ID: " + ticketID)
    searchButtonHasBeenPressed = TRUE

def makePartBoxes(btnCats):
    global checkboxVars
    checkboxVars = dict()
    checkboxVars.clear()
    
    for category in btnCats:
        checkboxVars[category] = tk.StringVar()
        btn = Checkbutton(btnFrame,text=str(category), variable= checkboxVars[category], onvalue=str(category), offvalue = None)
        btn.pack(side=TOP, anchor=W)

def makePartsToPickList():
    #Finds parts to pick from checkbox vars 
    catsToPick = []
    for pick in checkboxVars:
        if pick !=None:
            catsToPick.append(str(pick))
            print("Added category to pick list: "+ str(pick))

    global partsToPick
    partsToPick = []
    for cat in catsToPick:
        partToPick = parts[cat]
        partsToPick.append(partToPick)
        print("Added part to pick list: " + [partToPick])
    print("Parts to Pick : ")
    print(partsToPick)

def pickParts():
    makePartsToPickList()
# Display Parts Chosen
# Change Button Text and Actions to Confirm Parts 
# 

def deletePartBoxes():
    print("Need to delete part boxes")
    for widget in btnFrame.winfo_children():
        widget.destroy()

#Loop Run/ Window creation
window = tk.Tk()
window.geometry("275x640+1005+0")

#class gui:
#    __init__(self,master):
#        myFrame= Frame(master)

window.columnconfigure(1,minsize=200, weight = 0)

#Pulls info from ticket entry
def getTicketNum():
    ticketNum = str(e1.get())
    l2.configure(text = "Result: " + ticketNum)

#labels in window
l1 = Label(window, text = "Ticket#:")
l2 = Label(window)
l3 = Label(window)
l4 = Label(window)
l5 = Label(window)
l1.grid(row = 0, column = 0, sticky = W, pady = 2)
l2.grid(row = 2, column = 0, columnspan = 3, pady = 2, sticky=W)
l3.grid(row = 3, column = 0, columnspan = 3, pady = 2, sticky=W)
l4.grid(row = 4, column = 0, columnspan = 3, pady = 2, sticky=W)
l5.grid(row = 5, column = 0, columnspan = 3, pady = 2, sticky=W)

btnFrame = Frame(window, width = 255, height= 440,)
btnFrame.grid(row = 6, columnspan = 3,sticky=W, pady=5, padx=5)

# entry widgets
e1 = Entry(window)

e1.grid(row = 0, column = 1,sticky = W, pady = 2)

#Search button
button_search = Button(window, text="LOOKUP", command=lambda:getTicketInfo(str(e1.get()))).grid(row = 1, column = 1, pady = 2)
button_pickParts = Button(window, text="PICK PARTS", command=pickParts).grid(row = 7, column = 1, pady = 2)

#End loop run
tk.mainloop()