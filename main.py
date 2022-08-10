# ///////////////////////////////////////////////////////////////
#
# BY: WANDERSON M.PIMENTA
# PROJECT MADE WITH: Qt Designer and PySide6
# V: 1.0.0
#
# This project can be used freely for all uses, as long as they maintain the
# respective credits only in the Python scripts, any information in the visual
# interface (GUI) can be modified without any implication.
#
# There are limitations on Qt licenses if you want to use your products
# commercially, I recommend reading them on the official website:
# https://doc.qt.io/qtforpython/licenses.html
#
# ///////////////////////////////////////////////////////////////

from msilib.schema import CheckBox
import sys
import os
import platform

# IMPORT / GUI AND MODULES AND WIDGETS
# ///////////////////////////////////////////////////////////////
from modules import *
from modules import chromeActions


from widgets import *
os.environ["QT_FONT_DPI"] = "96" # FIX Problem for High DPI and Scale above 100%


#IMPORT / DICT
from typing import Dict


# SET AS GLOBAL WIDGETS
# ///////////////////////////////////////////////////////////////
widgets = None

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        # SET AS GLOBAL WIDGETS
        # ///////////////////////////////////////////////////////////////
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        global widgets
        widgets = self.ui

        # USE CUSTOM TITLE BAR | USE AS "False" FOR MAC OR LINUX
        # ///////////////////////////////////////////////////////////////
        Settings.ENABLE_CUSTOM_TITLE_BAR = True

        # APP NAME
        # ///////////////////////////////////////////////////////////////
        title = "AT Assistant"
        description = "Making ticket completion easier to make your job easier"
        # APPLY TEXTS
        self.setWindowTitle(title)
        widgets.titleRightInfo.setText(description)

        # TOGGLE MENU
        # ///////////////////////////////////////////////////////////////
        widgets.toggleButton.clicked.connect(lambda: UIFunctions.toggleMenu(self, True))

        # SET UI DEFINITIONS
        # ///////////////////////////////////////////////////////////////
        UIFunctions.uiDefinitions(self)
        
        # LOGIN
        chromeActions.login()
        
        # QTableWidget PARAMETERS
        # ///////////////////////////////////////////////////////////////
        widgets.table_pickeableParts.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        widgets.table_ticketinfo_pick.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        widgets.table_ticketinfo_verify.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        widgets.table_verifyinfo.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # BUTTONS CLICK
        # Add for each clickable button
        # ///////////////////////////////////////////////////////////////
        widgets.btn_ticketSearch_pick.clicked.connect(self.buttonClick)
        widgets.btn_ticketSearch_verify.clicked.connect(self.buttonClick)
        widgets.btn_forward_pick.clicked.connect(self.buttonClick)
        widgets.btn_forward_verify.clicked.connect(self.buttonClick)
        widgets.btn_pickParts.clicked.connect(self.buttonClick)
        widgets.btn_verify.clicked.connect(self.buttonClick)
        
        
        
        
        
        # LEFT MENUS
        widgets.btn_home.clicked.connect(self.buttonClick)
        widgets.btn_widgets.clicked.connect(self.buttonClick)
        widgets.btn_new.clicked.connect(self.buttonClick)
        widgets.btn_save.clicked.connect(self.buttonClick)

        # EXTRA LEFT BOX
        def openCloseLeftBox():
            UIFunctions.toggleLeftBox(self, True)
        widgets.toggleLeftBox.clicked.connect(openCloseLeftBox)
        widgets.extraCloseColumnBtn.clicked.connect(openCloseLeftBox)

        # EXTRA RIGHT BOX
        def openCloseRightBox():
            UIFunctions.toggleRightBox(self, True)
        #widgets.settingsTopBtn.clicked.connect(openCloseRightBox)

        # SHOW APP
        # ///////////////////////////////////////////////////////////////
        self.show()

        # SET CUSTOM THEME
        # ///////////////////////////////////////////////////////////////
        useCustomTheme = False
        themeFile = "themes\py_dracula_light.qss"

        # SET THEME AND HACKS
        if useCustomTheme:
            # LOAD AND APPLY STYLE
            UIFunctions.theme(self, themeFile, True)

            # SET HACKS
            AppFunctions.setThemeHack(self)

        # SET HOME PAGE AND SELECT MENU
        # ///////////////////////////////////////////////////////////////
        widgets.stackedWidget.setCurrentWidget(widgets.home)
        widgets.btn_home.setStyleSheet(UIFunctions.selectMenu(widgets.btn_home.styleSheet()))
    
    
    # BUTTONS CLICK
    # Post here your functions for clicked buttons
    # ///////////////////////////////////////////////////////////////
    def buttonClick(self):
        #T20220602.0687
        
        #btn execution functions
        def ticketSearchPick(self):
            searchEntry = widgets.entry_ticketnum_pick.text()
            print("Searching for ticket: " + searchEntry)
            #ticketInfo=[ticketID, deviceName, parts, btnCats]
            info = chromeActions.getTicketInfo(searchEntry)
            self.ticketNum = searchEntry
            self.ticketID = info[0]
            self.deviceName = info[1]
            self.parts = info[2]
            self.btnCats = info[3]
            showPickeableParts(self)
        
        def ticketSearchVerify(self):
            searchEntry = widgets.entry_ticketnum_verify.text()
            print("Searching for ticket: " + searchEntry)
            #ticketInfo=[ticketID, deviceName, parts, btnCats]
            info = chromeActions.getTicketInfo(searchEntry)
            self.ticketID = info[0]
            self.deviceName = info[1]
            self.parts = info[2]
            self.btnCats = info[3]
        
        def showTicketInfoPick(self):
            widgets.table_ticketinfo_pick.setItem( 0 , 0 , QTableWidgetItem(self.ticketNum)) # Ticket Number
            widgets.table_ticketinfo_pick.setItem( 0 , 1 , QTableWidgetItem(self.deviceName)) # Device Type
        
        def showPickeableParts(self):
            
            self.checkBoxes = []
            widgets.table_pickeableParts.setRowCount(len(self.parts)) #sets total rows to length of self.parts
            for index, cat in enumerate(self.parts): # Fills category column
                widgets.table_pickeableParts.setItem( index , 1 , QTableWidgetItem(cat)) 
                
            
            for index, part in enumerate(self.parts.values()): 
                # fills autotask ID column
                widgets.table_pickeableParts.setItem( index , 2 , QTableWidgetItem(part))
                
                # fills checkbox column
                checkBox = QCheckBox(widgets.table_pickeableParts)
                self.checkBoxes.append(checkBox)
                widgets.table_pickeableParts.setCellWidget(index , 0, checkBox)
                checkBox.setStyleSheet("margin-left:80%; margin-right:20%;")
                
                
        def checkForPartsToPick(self):
            self.partsToPick = []
            partList = list(self.parts.values())
            for index, cbox in enumerate(self.checkBoxes):
                if cbox.isChecked():
                    self.partsToPick.append(partList[index])
            print(self.partsToPick)
        
        
        def pickParts(self):
            checkForPartsToPick(self)
            chromeActions.pickParts(self.ticketID,self.partsToPick)

        # GET BUTTON CLICKED
        btn = self.sender()
        btnName = btn.objectName()

        # SHOW HOME PAGE
        if btnName == "btn_home":
            widgets.stackedWidget.setCurrentWidget(widgets.home)
            UIFunctions.resetStyle(self, btnName)
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))

        # SHOW WIDGETS PAGE
        if btnName == "btn_widgets":
            widgets.stackedWidget.setCurrentWidget(widgets.widgets)
            UIFunctions.resetStyle(self, btnName)
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))

        # SHOW NEW PAGE
        if btnName == "btn_new":
            widgets.stackedWidget.setCurrentWidget(widgets.new_page) # SET PAGE
            UIFunctions.resetStyle(self, btnName) # RESET ANOTHERS BUTTONS SELECTED
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet())) # SELECT MENU

        if btnName == "btn_save":
            print("Save BTN clicked!")
            
        if btnName == "btn_ticketSearch_pick":
            ticketSearchPick(self)
            showTicketInfoPick(self)
            
        if btnName == "btn_ticketSearch_verify":
            ticketSearchVerify(self)

        if btnName == "btn_pickParts":
            pickParts(self)
            
        if btnName =="btn_forward_pick":
            chromeActions.forwardTicket(self.ticketID,{"Primary":"Ryan Vankerkvoorde"})
            
        # PRINT BTN NAME
        print(f'Button "{btnName}" pressed!')
        


    # RESIZE EVENTS
    # ///////////////////////////////////////////////////////////////
    def resizeEvent(self, event):
        # Update Size Grips
        UIFunctions.resize_grips(self)

    # MOUSE CLICK EVENTS
    # ///////////////////////////////////////////////////////////////
    def mousePressEvent(self, event):
        # SET DRAG POS WINDOW
        self.dragPos = event.globalPos()

        # PRINT MOUSE EVENTS
        if event.buttons() == Qt.LeftButton:
            print('Mouse click: LEFT CLICK')
        if event.buttons() == Qt.RightButton:
            print('Mouse click: RIGHT CLICK')

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("icon.ico"))
    window = MainWindow()
    sys.exit(app.exec())
