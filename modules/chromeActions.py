
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

import json

import logins
from . import twofa
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

#starts chrome instance
#options to clear errors
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
s=Service('modules/chromedriver.exe')

#opens new chrome instance 
driver = webdriver.Chrome(service=s,options=options)
driver.set_window_position(-10,-10)
driver.set_window_size(1024,600)

def login(): # TODO LOGIN TO AT

    login = logins.getLogins()
    userName = login[0]
    pw = login[1]
        #opens autotask login
    driver.get("https://www.autotask.net/Mvc/Framework/Authentication.mvc/Authenticate")

        #Login To Autotask and Wait for 2fa code input. 
        #email Login
    loginEmail= driver.find_element(By.XPATH,"/html/body/div[1]/div/div[2]/div[3]/div[1]/div[1]/div[3]/input").send_keys(userName)
    comfirmEmail = driver.find_element(By.XPATH,"/html/body/div[1]/div/div[2]/div[3]/div[1]/div[1]/div[4]/div[3]/div/div").click()

        #PASS entry TODO protect login info 
    elem=WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[1]/div/div[2]/div[3]/div[2]/div[1]/div[4]/input")))
    loginPass = driver.find_element(By.XPATH,"/html/body/div[1]/div/div[2]/div[3]/div[2]/div[1]/div[4]/input").send_keys(pw)
    confirmPass = driver.find_element(By.XPATH,"/html/body/div[1]/div/div[2]/div[3]/div[2]/div[1]/div[5]/div[4]/div/div").click()

        #2fa login
    generateCode= twofa
    twofaCodeBox=WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[1]/div/div[2]/div[3]/div[5]/div[1]/div[3]/input")))
    recentCode = generateCode.getNewCode()
    entryBox = driver.find_element(By.XPATH,"/html/body/div[1]/div/div[2]/div[3]/div[5]/div[1]/div[3]/input").send_keys(recentCode)
    confirmCode = driver.find_element(By.XPATH,"/html/body/div[1]/div/div[2]/div[3]/div[5]/div[1]/div[5]/div[2]").click()
    
    #Print Current supported models
    getSupportedModels()


#https://ww5.autotask.net/Mvc/ServiceDesk/TicketDetail.mvc?workspace=False&ids%5B0%5D=540748&ticketId=540748
def openTicketURL(ticketID):
    ticketURL='https://ww5.autotask.net/Mvc/ServiceDesk/TicketDetail.mvc?workspace=False&ids%5B0%5D='
    ticketURL = ticketURL + ticketID
    ticketURL = ticketURL + '&ticketId='+ ticketID
    driver.switch_to.new_window('tab')
    driver.get(ticketURL)


def getTicketInfo(ticketNum): # opens new tab and searches for ticket and grabs info. Closes tab. 
    driver.switch_to.window(driver.window_handles[0])
    
    btnCats=[]
    #Search For Ticket
    WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div[1]/div[2]/input")))
    searchBox= driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/div[2]/input")
    searchBox.clear()
    searchBox.send_keys(ticketNum)
    searchBox.send_keys(Keys.RETURN)

    #Switch to iframe contents 
    WebDriverWait(driver, 20).until(EC.frame_to_be_available_and_switch_to_it((By.NAME,"PageContainerFrame")))

    #Open Ticket
    clickTicket=WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[1]/div[2]/div/div[2]/div/table/tbody/tr/td[4]")))
    clickTicket.click()

    #Switch to ticket tab
    driver.switch_to.window(driver.window_handles[1])

    #Output Device name(Title)
    title=WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.XPATH,"/html/body/div[4]/div[2]/div[1]/div[1]/div/div[2]/div[1]")))
    print("Device: ")
    print(title.get_attribute('innerText'))
    deviceName=(title.get_attribute('innerText'))

    #Find parts based on device name
    parts = getPickeableParts(deviceName)
    
    #Gets AT motherboard search name and replaces mb array in parts dict
    moboName=parts['MB'].get(deviceName) # Add try catch in case model is not found in parts.json
    replaceWithMobo = {'MB':moboName}
    parts.update(replaceWithMobo)

    for partCategory in parts:
        if partCategory!='MB':  
            #print(partCategory) #Gets part categories for button text
            btnCats.append(partCategory)
            #print(parts[partCategory]) # Gets AT part names 
        else: 
            btnCats.append('MB')

    #Output Current URL
    ticketURL = str(driver.current_url)
    ticketID = ticketURL.split('=')[-1]
    
    ticketInfo=[ticketID, deviceName, parts, btnCats]
    print(ticketInfo)
    resetWindows()
    return ticketInfo


def pickParts(ticketID,partsToPick): #TODO iterates through partsToPick and calls pickSinglePart for each
    openTicketURL(ticketID)
    
    for part in partsToPick:
        print("Picking: " + part + "...")
        pickSinglePart(part, ticketID)
        print("Picked part : " + part + " on ticket ID:" + ticketID)
    resetWindows()

def pickSinglePart(partNameAT, ticketID): #TODO opens new page and goes through pick parts process
    
    #Waits for title to load and opens new part charge
    #/html/body/div[3]/div[4] - new charge button

    newChargeButton=WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[3]/div[4]")))
    newChargeButton.click()

    #switch to new charge page
    driver.switch_to.window(driver.window_handles[2])

    #item search box
    #/html/body/form/div[1]/div/div[2]/div[2]/div/table/tbody/tr[2]/td[1]/table/tbody/tr[1]/td/div/nobr/span/input
    partSearchBox=WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,"/html/body/form/div[1]/div/div[2]/div[2]/div/table/tbody/tr[2]/td[1]/table/tbody/tr[1]/td/div/nobr/span/input")))
    partSearchBox.send_keys(partNameAT)

    #iframe id for autocomplete.
    autoCompleteBox=WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.CLASS_NAME,"autocomplete")))
    partSearchBox.send_keys(Keys.RETURN)

    #pick hyperlink
    #/html/body/form/div[1]/div/div[2]/div[2]/div[2]/div[2]/table/tbody/tr/td/span/div/div/table/tbody/tr[2]/td[5]/a
    time.sleep(2)

    pickLink=WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,"/html/body/form/div[1]/div/div[2]/div[2]/div[2]/div[2]/table/tbody/tr/td/span/div/div/table/tbody/tr[2]/td[5]/a"))) 
    pickLink.send_keys(Keys.PAGE_DOWN)
    pickLink.click()

    #alert box OK button
    try:
        WebDriverWait(driver, 3).until(EC.alert_is_present(),
                                       'Timed out waiting for pick ' +
                                       'confirmation popup to appear.')

        alert = driver.switch_to.alert
        alert.accept()
    except TimeoutException():
        print("no alert")

    #TODO pick confirmation popup - okay button
    #/html/body/form/div/table/tbody/tr/td[1]/atbutton/span/a/table
    #/html/body/form/div[1]/div/atwindowpanel/div[3]/table/tbody/tr[2]/td/div[1]/iframe

    

    try:
        WebDriverWait(driver, 20).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH,"/html/body/form/div[1]/div/atwindowpanel/div[3]/table/tbody/tr[2]/td/div[1]/iframe")))
    except:
        WebDriverWait(driver, 20).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH,"/html/body/form/div[1]/div/atwindowpanel/div[3]/table/tbody/tr[2]/td/div[1]/iframe")))
    
    

    try:
        confirmPick=WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,"/html/body/form/div/table/tbody/tr/td[1]/atbutton/span")))
    except:
        confirmPick=WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,"/html/body/form/div/table/tbody/tr/td[1]/atbutton/span")))


    confirmPick=WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,"/html/body/form/div/table/tbody/tr/td[1]/atbutton/span")))
    confirmPick.click()

    # check for price changed alert. 
    try:
        WebDriverWait(driver, 3).until(EC.alert_is_present(),
                                       'Timed out waiting for pick ' +
                                       'confirmation popup to appear.')

        alert = driver.switch_to.alert
        alert.accept()
    except:
        print("no price alert")

    #Save and Close button
    #/html/body/form/div[1]/div/div[1]/table/tbody/tr/td/table/tbody/tr/td[1]/atbutton/span
    saveClose=WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,"/html/body/form/div[1]/div/div[1]/table/tbody/tr/td/table/tbody/tr/td[1]/atbutton/span")))
    saveClose.click()
    driver.switch_to.window(driver.window_handles[1])

def forwardTicket(ticketID, forwardInfo): #TODO forwards ticket to specific name and status
    
    def changePrimary(newPrimary):
        print("Changing primary to:..." + newPrimary)
        
        #Primary Resource Drop
        #/html/body/form/div/div[5]/table/tbody/tr[2]/td/div/div[2]/table/tbody/tr/td[3]/table/tbody/tr[2]/td/table/tbody/tr/td[1]/select
        WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,"/html/body/form/div/div[5]/table/tbody/tr[2]/td/div/div[2]/table/tbody/tr/td[3]/table/tbody/tr[2]/td/table/tbody/tr/td[1]/select")))
        selectrPrimaryDrop= Select(driver.find_element(By.XPATH,"/html/body/form/div/div[5]/table/tbody/tr[2]/td/div/div[2]/table/tbody/tr/td[3]/table/tbody/tr[2]/td/table/tbody/tr/td[1]/select"))
        selectrPrimaryDrop.select_by_visible_text(newPrimary + " (Client Service Engineer L1)")
        
    def changeStatus(newStatus):
        print("Changing Status to:..." + newStatus)
        
        #Status Drop
        #/html/body/form/div/div[5]/table/tbody/tr[3]/td/div/div[2]/table/tbody/tr[8]/td[1]/select
        WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,"/html/body/form/div/div[5]/table/tbody/tr[3]/td/div/div[2]/table/tbody/tr[8]/td[1]/select")))
        selectrStatusDrop= Select(driver.find_element(By.XPATH,"/html/body/form/div/div[5]/table/tbody/tr[3]/td/div/div[2]/table/tbody/tr[8]/td[1]/select"))
        selectrStatusDrop.select_by_visible_text(newStatus)
        
        
        
    #TODO
    #def changeSubIssType(newSIType):
    
    def changeAccDmg(newAccDmg):
        print("Changing Accidental Damage to:..." + newAccDmg)
        
        #Damage Drop
        #/html/body/form/div/div[5]/table/tbody/tr[4]/td/div/div[2]/table/tbody/tr/td/table/tbody/tr[1]/td[1]/div/span/select
        WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,"/html/body/form/div/div[5]/table/tbody/tr[4]/td/div/div[2]/table/tbody/tr/td/table/tbody/tr[1]/td[1]/div/span/select")))
        selectrDamageDrop= Select(driver.find_element(By.XPATH,"/html/body/form/div/div[5]/table/tbody/tr[4]/td/div/div[2]/table/tbody/tr/td/table/tbody/tr[1]/td[1]/div/span/select"))
        selectrDamageDrop.select_by_visible_text(newAccDmg)
        
    def changeWarrClaim(newWarrClaim):
        print("Changing Accidental Damage to:..." + newWarrClaim)
        
        #Warr Claim Drop
        #/html/body/form/div/div[5]/table/tbody/tr[4]/td/div/div[2]/table/tbody/tr/td/table/tbody/tr[8]/td[1]/div/span/select
        WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,"/html/body/form/div/div[5]/table/tbody/tr[4]/td/div/div[2]/table/tbody/tr/td/table/tbody/tr[8]/td[1]/div/span/select")))
        selectrWarrantyDrop= Select(driver.find_element(By.XPATH,"/html/body/form/div/div[5]/table/tbody/tr[4]/td/div/div[2]/table/tbody/tr/td/table/tbody/tr[8]/td[1]/div/span/select"))
        selectrWarrantyDrop.select_by_visible_text(newWarrClaim)
    
    confirmedForward = False
    
    primaryDrops=["Ryan Vankerkvoorde"]
    statusDrops=["Repaired", "In Progress", "Waiting Parts","Battery Swap Required", "Waiting Repair"]
    damageDrops=["Yes", "No"]
    warrantyDrops=["In warranty accidental damage", "No Part Need Out of Warranty", "Parts Replaced in Warranty" ]
    
    forwardInfoTest = {
        "Primary": "Vankerkvoorde, Ryan",
        "Status": "In Progress",
        "AccidentalDamage": "Yes",
        "WarrantyClaim": "No Part Need Out of Warranty"
        }
    
    #"SubIssueType": "",
    
    #"Secondary": "",
    #"QAResource": "",
    #"ReworkResource": "",
    #"OriginalTechnician": "",
    #"QualityControl": ""
    
    #Open Ticket Page
    openTicketURL(ticketID)
    
    #Open Forward Page
    
    #Forward Button
    #/html/body/div[1]/div[4]/div[3]
    forwardButton=WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[1]/div[4]/div[3]")))
    forwardButton.click()
    #switch to forward tab
    driver.switch_to.window(driver.window_handles[2])
    
    #Go through passed dict and perform page changes for each one
    for option in forwardInfoTest:
            if(option == "Primary"):
                changePrimary(forwardInfoTest[option])
            if(option == "Status"):
                changeStatus(forwardInfoTest[option])
            
            #if(option == "SubIssueType"):
            
            
            
            #Need to add try and click + on "User Defined Fields" on failure
            #if(option == "AccidentalDamage"):
                changeAccDmg(forwardInfoTest[option])
            
            #if(option == "WarrantyClaim"):
                changeWarrClaim(forwardInfoTest[option])
            
            #if(option == "Secondary"):
            #if(option == "QAResource"):
            #if(option == "ReworkResource"):
            #if(option == "OriginalTechnician"):
            #if(option == "QualityControl"):
        
    #Save and Close
    
    #/html/body/form/div/div[2]/ul/li[1]/a
    saveCloseButton=WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,"/html/body/form/div/div[2]/ul/li[1]/a")))      
    #saveCloseButton.click()


#def createNotesEntry #TODO open notes, add notes based on parts picked

def getPickeableParts(deviceName):
    with open(r"json\parts.json", "r") as outfile:
        data = json.load(outfile)
    
    pickeableParts = dict()
    for modelCategory in data:   
        models=data[modelCategory].get('models')
        if deviceName in models:
            print("Found parts for model group: " + modelCategory)
    
            modelDict= data[modelCategory].copy()
            modelDict.pop('models')
            pickeableParts = modelDict.copy()
            #print(pickeableParts)
            return pickeableParts   #returns just parts and no model info 

        
def resetWindows():
    x=0
    for handle in driver.window_handles:
        if x!=0:
            driver.switch_to.window(handle)
            driver.close()
        x=x+1
    driver.switch_to.window(driver.window_handles[0])
#elem=WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,"")))




def getSupportedModels():
    with open(r"json\parts.json", "r") as outfile:
        data = json.load(outfile)
    
    pickeableParts = dict()
    for modelCategory in data:   
        models=data[modelCategory].get('models')
        for deviceName in models:
            print("Supported model:  " + deviceName)