from msilib.schema import CheckBox
import sys
import os

# IMPORT / GUI AND MODULES AND WIDGETS
# ///////////////////////////////////////////////////////////////
from modules import *
from chromeActions import *
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
        description = "Automating the boring stuff"
        # APPLY TEXTS
        self.setWindowTitle(title)
        widgets.titleRightInfo.setText(description)

        # TOGGLE MENU
        # ///////////////////////////////////////////////////////////////
        widgets.toggleButton.clicked.connect(lambda: UIFunctions.toggleMenu(self, False))

        # SET UI DEFINITIONS
        # ///////////////////////////////////////////////////////////////
        UIFunctions.uiDefinitions(self)
        
        # LOGIN
        login()
        
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

        # Dropdowns
        primaryDrops=["Vankerkvoorde, Ryan"]
        statusDrops=["Repaired", "In Progress", "Waiting Parts","Battery Swap Required", "Waiting Repair"]
        damageDrops=["Yes", "No"]
        warrantyDrops=["In warranty accidental damage", "No Part Need Out of Warranty", "Parts Replaced in Warranty" ]
        
        widgets.comboBox_primaryResource_pick.addItems(primaryDrops)
        widgets.comboBox_status_pick.addItems(statusDrops)
        widgets.comboBox_damage_pick.addItems(damageDrops)
        widgets.comboBox_warranty_pick.addItems(warrantyDrops)
        
        
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
        
        #btn execution functions
        def ticketSearchPick(self):
            searchEntry = widgets.entry_ticketnum_pick.text()
            print("Searching for ticket: " + searchEntry)
            #ticketInfo=[ticketID, deviceName, schoolName, sn, traWarrantyExp, mfgWarrantyExp, parts, btnCats]
            info = getTicketInfo(searchEntry)   
            self.ticketNum = searchEntry        #ticketNum
            self.ticketID = info[0]             #ticektID
            self.deviceName = info[1]           #deviceName
            self.school = info[2]               #schoolName
            self.sn = info[3]                   #S/N
            self.traExp = info[4]               #traWarrantyExp
            self.mfgExp = info[5]               #mfgWarrantyExp
            self.parts = info[6]                #parts
            self.btnCats = info[7]              #btnCcats
            showPickeableParts(self)
        
        def ticketSearchVerify(self):
            searchEntry = widgets.entry_ticketnum_verify.text()
            print("Searching for ticket: " + searchEntry)
            #ticketInfo=[ticketID, deviceName, parts, btnCats]
            info = getTicketInfo(searchEntry)
            self.ticketID = info[0]
            self.deviceName = info[1]
            self.parts = info[2]
            self.btnCats = info[3]
        
        def showTicketInfoPick(self):
            widgets.table_ticketinfo_pick.setItem( 0 , 0 , QTableWidgetItem(self.ticketNum)) # Ticket Number
            widgets.table_ticketinfo_pick.setItem( 0 , 1 , QTableWidgetItem(self.deviceName)) # Device Type
            widgets.table_ticketinfo_pick.setItem( 0 , 2 , QTableWidgetItem(self.mfgExp)) # MFG Exp
            widgets.table_ticketinfo_pick.setItem( 0 , 3 , QTableWidgetItem(self.traExp)) # TRA Exp
            widgets.table_ticketinfo_pick.setItem( 0 , 4 , QTableWidgetItem(self.school)) # School
        
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
        
        
        def pickPartsExecute(self):
            checkForPartsToPick(self)
            pickParts(self.ticketID,self.partsToPick)
            
        def forward(self):
            forward_info= dict()
            
            if(widgets.checkBox_primaryResource_pick.isChecked):
                currentSelection=widgets.comboBox_primaryResource_pick.currentText()
                forward_info.update({"Primary":currentSelection})
            
            if(widgets.checkBox_status_pick.isChecked):
                currentSelection=widgets.comboBox_status_pick.currentText()
                forward_info.update({"Status":currentSelection})
                
            if(widgets.checkBox_damage_pick.isChecked):
                currentSelection=widgets.comboBox_damage_pick.currentText()
                forward_info.update({"AccidentalDamage":currentSelection})
                
            if(widgets.checkBox_warranty_pick.isChecked):
                currentSelection=widgets.comboBox_warranty_pick.currentText()
                forward_info.update({"WarrantyClaim":currentSelection})
            
            forwardTicket(self.ticketID,forward_info)

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
   
        if btnName == "btn_ticketSearch_pick":
            ticketSearchPick(self)
            showTicketInfoPick(self)
            
        if btnName == "btn_ticketSearch_verify":
            ticketSearchVerify(self)

        if btnName == "btn_pickParts":
            pickPartsExecute(self)
            
        if btnName =="btn_forward_pick":
            forward(self)
            
            
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
