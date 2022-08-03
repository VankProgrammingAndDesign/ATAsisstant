import json

modelGroup = "Acer R751T/R751TN"

count=0
allData=[]
f =  open(r"C:\Users\vanke\Documents\Code Applications\ATAssistant\json\rawdata.txt")
for line in f:
    allData.append(line)
    count+=1
    print("Line # " + str(count)+ " : " + line)
    
for data in allData:
    print(data)

totalLines= len(allData)+1

count=1
partCategories = []
partNames = []
for data in allData:
    if ((count % 2) == 0): #even 
        if(count < (totalLines/2)): #even and count is less than allData length/2
            print ("Did not add line: " + str(count) + " to part categories")
        else:    #even and count is > 40
            print ("Did not add line: " + str(count) + " to part names")
    elif((count % 2) == 1):   # odd
        if(count>=totalLines/2): # odd and greater than or equal to  allData length/2       
            partNames.append(data.strip()) # removes new lines and adds to  partNames
        else:    # odd and less than 40 
            partCategories.append(data.strip()[:-1])# removes new lines and ":" and adds to part categories
    else:
        print("This shouldnt trigger")
    count+=1    

for category in partCategories:
    print(category)
print("End of Cateogry List")
for name in partNames:
    print(name)
print("End of Part Name List")

count = 0
elementStr=""
partsInJSON=[]
for category in partCategories:
    elementStr=""
    elementStr=str(category)
    elementStr='"' + elementStr + '"' + ":"
    elementStr= elementStr + '"' + partNames[count] + '"'
    partsInJSON.append(elementStr)
    count+=1

for part in partsInJSON:
    print(part)

Dict={}
count=0
Dict ["models"]={"AutotaskModel 1":""} 
for category in partCategories:
    Dict[category]= partNames[count]
    count+=1
finalDict={}
finalDict[modelGroup]=Dict
print(finalDict)

with open(r"C:\Users\vanke\Documents\Code Applications\ATAssistant\json\processedData.json", "w") as outfile:
    json.dump(finalDict, outfile,indent = 4)