#Basic Program Needs
import sys
import os
import math

countSpam={}
countHam={}
probSpam={}
probHam ={}
def getTheListOfFiles(rootDir):
    nameOfFiles = ""
    for root, dirs, files in os.walk(rootDir):
            for name in files:
                if name.endswith(("nbmodel.txt")):
                    nameOfFiles = os.path.join(root, name)
    print(nameOfFiles)
    return nameOfFiles

def getTheListOfDevFiles(rootDir):
    nameOfFiles =[]
    for root, dirs, files in os.walk(rootDir):
            for name in files:
                if name.endswith((".txt")):
                    nameOfFiles.append(os.path.join(root, name))
    return nameOfFiles

def getTheFileContent(getModelFileName):
    file = open(getModelFileName, "r")
    query = file.read()
    queryContent = query.split('\n')
    return queryContent

def returnContent(index, content):
    currentItem = content[index].strip()
    itemList = currentItem.split()
    value = int(itemList[1])
    return value

def returnTheListOfWords(fileName):
    fileContent = open(fileName, "r", encoding="latin1").read()
    listOfWords = fileContent.split()
    return listOfWords

def calculateProbablity(listOfTokens,dict):
    probTotal = 0
    for word in listOfTokens:
        if word in dict:
            probTotal = probTotal + dict.get(word)
    return  probTotal

def writeFinalOutput(label, fileName):
    fContent = label + " " + fileName+ " \n"
    finalFile.write(fContent)


#Execution of the Main Program

inputDirectory = sys.argv[1]
getContent = getTheFileContent("nbmodel.txt")

#To Make dictionary and set up of variable using nbmodel.txt
for num in range(1, len(getContent)):
    currentItem  = getContent[num].strip()
    if currentItem == "HAMOUTPUT":
        break;
    else:
        itemList = currentItem.split()
        countSpam[itemList[0]] = int(itemList[1])
        probSpam[itemList[0]] = float(itemList[2])

for num in range(num+1, len(getContent)):
    currentItem = getContent[num].strip()
    if currentItem == "endOfFile":
        break;
    else:
        itemList = currentItem.split()
        countHam[itemList[0]] = int(itemList[1])
        probHam[itemList[0]] = float(itemList[2])

num = num +1
totalSpamWords = returnContent(num, getContent)
num = num +1
totalHamWords = returnContent(num, getContent)
num = num +1
distinctWords = returnContent(num, getContent)
num = num +1
totalSpamFIles = returnContent(num, getContent)
num = num +1
totalHamFIles = returnContent(num, getContent)

totalFiles = totalSpamFIles + totalHamFIles;
sProb = math.log(totalSpamFIles)  -  math.log(totalFiles)
hProb = math.log(totalHamFIles)  -  math.log(totalFiles)

# TO READ THE DEV DATA AND TO CLASSIFY THE FILES
finalFile = open("nboutput.txt", 'w')
nameOfDevFiles =  getTheListOfDevFiles(inputDirectory)


recalltotalSpamCount= 0
recallTotalHamCount = 0
expectedSpamCount =0
expectedHamCount =0
preTSpamcount=0
preTHamcount =0

for devFiles in nameOfDevFiles:

     getFileType = devFiles.split('/')
     typeOfFile = getFileType[len(getFileType) - 2]
     if (typeOfFile == "spam"):
         recalltotalSpamCount = recalltotalSpamCount + 1
     else:
         recallTotalHamCount = recallTotalHamCount + 1
     listOfTokens = returnTheListOfWords(devFiles)
     spamPro = sProb + calculateProbablity (listOfTokens, probSpam)
     hamPro =  hProb +calculateProbablity(listOfTokens, probHam)
     if spamPro > hamPro:
         label = "spam"
         preTSpamcount = preTSpamcount + 1
     elif hamPro > spamPro:
         label = "ham"
         preTHamcount = preTHamcount + 1
     else:
         label = "Cannot Decide"

     if typeOfFile == "spam" and label == "spam":
         expectedSpamCount = expectedSpamCount + 1
     if typeOfFile == "ham" and label == "ham":
         expectedHamCount = expectedHamCount + 1

     writeFinalOutput(label, devFiles)


precisionForSpam =  expectedSpamCount/preTSpamcount
precisionForHam =   expectedHamCount/ preTHamcount

recallForSpam = expectedSpamCount/recalltotalSpamCount
recallForHam =  expectedHamCount/ recallTotalHamCount

fscoreForSpam = (2 * precisionForSpam * recallForSpam)/(precisionForSpam +  recallForSpam)
fscoreForHam =  (2 * precisionForHam * recallForHam)/(precisionForHam +  recallForHam)

'''
print(precisionForSpam)
print(recallForSpam)
print(fscoreForSpam)
print(precisionForHam)
print(recallForHam)
print(fscoreForHam)
'''















