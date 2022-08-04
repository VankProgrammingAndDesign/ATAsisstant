import tkinter as tk
from typing import Dict
import chromeActions
# import tkinter module
from tkinter import * 
from tkinter.ttk import *


chromeActions.login()


#T20220202.0237
#T20220202.0267


#Loop Run/ Window creation
window = tk.Tk()
window.geometry("275x640+1005+0")
window.columnconfigure(1,minsize=200, weight = 0)

class gui:
    def __init__(self,master):
        self.master=master
        #labels in window
        self.l1 = Label(master, text = "Ticket#:")
        self.l2 = Label(master)
        self.l3 = Label(master)
        self.l4 = Label(master)
        self.l5 = Label(master)
        self.l1.grid(row = 0, column = 0, sticky = W, pady = 2)
        self.l2.grid(row = 2, column = 0, columnspan = 3, pady = 2, sticky=W)
        self.l3.grid(row = 3, column = 0, columnspan = 3, pady = 2, sticky=W)
        self.l4.grid(row = 4, column = 0, columnspan = 3, pady = 2, sticky=W)
        self.l5.grid(row = 5, column = 0, columnspan = 3, pady = 2, sticky=W)
        # entry widgets
        self.e1 = Entry(master)
        self.e1.grid(row = 0, column = 1,sticky = W, pady = 2)

        #Search button
        self.button_search = Button(master, text="LOOKUP", command=lambda:self.getTicketInfo(str(self.e1.get())))
        self.button_search.grid(row = 1, column = 1, pady = 2, sticky=W)
        master.bind('<Return>',(lambda event: self.getTicketInfo(str(self.e1.get()))))
        

        self.button_pickParts = Button(master, text="PICK PARTS",command=self.pickParts)
        self.button_pickParts.grid(row = 7, column = 1, pady = 2, sticky=W)
        self.btnFrame = Frame(master, width = 255, height= 440,)
        self.btnFrame.grid(row = 6, columnspan = 3,sticky=W, pady=5, padx=5)
        self.searchButtonHasBeenPressed = FALSE

    #Pulls info from ticket entry

    def getTicketInfo(self,ticketNum): 
        if self.searchButtonHasBeenPressed:
            self.reset_windows()

        #ticketInfo=[ticketID, deviceName, parts, btnCats]
        info = chromeActions.getTicketInfo(ticketNum)
        self.ticketID = info[0]
        self.deviceName = info[1]
        self.parts = info[2]
        self.btnCats = info[3]
        print("Before make boxes:" + str(self.btnCats))
        self.makePartBoxes() # Makes checkboxes from part categories
        self.l2.configure(text = "Searched: " + ticketNum)
        self.l3.configure(text = "Device: " + self.deviceName)
        self.l4.configure(text = "Ticket ID: " + self.ticketID)
        self.searchButtonHasBeenPressed = TRUE


    def reset_windows(self):
        self.deletePartBoxes()
        self.deleteBtnFrameContents()
        self.button_pickParts.configure(text= "PICK", command=self.pickParts)


    def pickParts(self):
        self.makePartsToPickList()
        # Display Parts Chosen
        self.showPickInfo()
        # Change Button Text and Actions to Confirm Parts # 
    
    def confirmPick(self):
        chromeActions.pickParts(self.ticketID,self.partsToPick)

    def deletePartBoxes(self):
        print("Need to delete part boxes")
        for widget in self.btnFrame.winfo_children():
            widget.destroy()

    def deleteBtnFrameContents(self):
        #Clear Button frame
        for widgets in self.btnFrame.winfo_children():
            widgets.destroy()


    def showPickInfo(self):
        #Clear Button frame
        self.deleteBtnFrameContents()

        #Show Picked Choices:
        for part in self.partsToPick:
            lab = Label(self.btnFrame, text= part)
            lab.pack(side=TOP, anchor=W)
        
        #Change buttons
        self.button_pickParts.configure(text= "CONFIRM", command=self.confirmPick)

    def makePartBoxes(self):
        self.checkboxVars=[]
        for category in self.btnCats:
            svar=tk.StringVar()
            self.checkboxVars.append(svar)
            btn = Checkbutton(self.btnFrame, text=str(category), variable= svar, onvalue=str(category), offvalue = '')
            btn.pack(side=TOP, anchor=W)


    #TODO issue, picks all parts, change dict to list?
    def makePartsToPickList(self):
    #Finds parts to pick from checkbox vars 
        self.catsToPick = []
        for choice in self.checkboxVars:
            if choice.get() !='':
                if choice.get != 0:
                    self.catsToPick.append(choice.get())
                    print("Added category to pick list: "+ choice.get())

        self.partsToPick = []
        for cat in self.catsToPick:
            partToPick = self.parts[cat]
            self.partsToPick.append(partToPick)
            print("Added part to pick list: " + partToPick)
        print("Parts to Pick : ")
        print(self.partsToPick)

searchGui = gui(window)

#End loop run
tk.mainloop()