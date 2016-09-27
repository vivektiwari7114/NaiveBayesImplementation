#Basic Program Needs
import sys
import os
import math
from os.path import join, getsize

#Global Variables
spamDict = {}
hamDict = {}

#Function to get recursively search the directory
def getTheListOfFiles(folderName, rootDir):
    nameOfFiles =[]
    for root, dirs, files in os.walk(rootDir):
        getAllFilesNames = root.split('/')
        lastFile = getAllFilesNames[len(getAllFilesNames) - 1].lower()
        if(lastFile == folderName):
            for name in files:
                if name.endswith((".txt")):
                    nameOfFiles.append(os.path.join(root, name))
    return nameOfFiles

#Function to open a file and create dictionary
def openIndividualFile(fileName, tempDict):
    fileContent = open(fileName, "r", encoding="latin1").read()
    listOfWords = fileContent.split()
    for word in listOfWords:
        sWord = word.lower()
        if sWord in tempDict:
                tempDict[sWord] = tempDict.get(sWord) + 1
        else:
            tempDict[sWord] = 1
    return tempDict

def calculateSetDifference(source, destination):
    tempList = source.keys()
    for item in tempList:
        if item not in destination:
            destination[item] = 0
    return destination

def countTheTotalWords(tempDict):
    count =0;
    listOfName = tempDict.keys()
    for lNames in listOfName:
         count = count + tempDict.get(lNames)
    return count

def calculateProbablity(givenClassDict, wordsInGivenClass, distinctCount,newProbDict):
    tempList = givenClassDict.keys()
    for itemD in tempList:
        num = givenClassDict.get(itemD) + 1
        denom = wordsInGivenClass + distinctCount
        prob = math.log(num) - math.log(denom)
        newProbDict[itemD] = prob
    return newProbDict

def writeInFile(key, count, prob):
    contentWrite = key + " "+str(count)+" "+str(prob)+" \n"
    outputfile.write(contentWrite)


#Execution of the Main program
sourceRootDirectory = sys.argv[1]
spamFiles = getTheListOfFiles("spam",sourceRootDirectory)
hamFiles = getTheListOfFiles("ham", sourceRootDirectory)

totalSpamcount = len(spamFiles)  # Total Number of Training data Marked as SPAM
totalHamcount = len(hamFiles)    # Total Number of Training data Marked as HAM
totalFileCount = totalSpamcount +  totalHamcount  # Total Number of Training data

for sName in spamFiles:
    spamDict = openIndividualFile(sName, spamDict)

for hName in hamFiles:
    hamDict = openIndividualFile(hName, hamDict)


#To remove top 100 most frequent words
withoutTopHundredSpamDict =  sorted(spamDict, key = spamDict.get, reverse=True)[:100]
withoutTopHundredHamDict =  sorted(hamDict, key = hamDict.get, reverse=True)[:100]
commonDict = set(withoutTopHundredSpamDict).intersection(withoutTopHundredHamDict)
for wordFound in commonDict:
    if wordFound in  spamDict.keys():
        del spamDict[wordFound]
    if wordFound in  hamDict.keys():
        del hamDict[wordFound]


#Normalization for Set difference
normalizeSpamDict =  spamDict
normalizeHamDict =  hamDict
normalizeSpamDict = calculateSetDifference(hamDict, spamDict)
normalizeHamDict = calculateSetDifference(spamDict, hamDict)

distinctCount = len(normalizeSpamDict) #Distict number of words in both Normalized SPAM and HAM Dictionary

wordsInSpam = countTheTotalWords(normalizeSpamDict) #Total Number of Words in SPAM
wordsInHam = countTheTotalWords(normalizeHamDict)   # Total Number of Words in HAM

probablityForWordsInSpam = {}
probablityForWordsInHam = {}

#Calculate Probablity for Words in SPAM
probablityForWordsInSpam = calculateProbablity(normalizeSpamDict, wordsInSpam, distinctCount,probablityForWordsInSpam)
#Calculate Probablity for Words in HAM
probablityForWordsInHam = calculateProbablity(normalizeHamDict, wordsInHam, distinctCount,probablityForWordsInHam)

#Open the file for write
outputfile = open("nbmodel.txt", 'w')
outputfile.write("SPAMOUTPUT\n")
printSList = normalizeSpamDict.keys()
for itemized in printSList:
     writeInFile(itemized, normalizeSpamDict.get(itemized) , probablityForWordsInSpam.get(itemized))

outputfile.write("HAMOUTPUT\n")
printHList = normalizeHamDict.keys()
for itemized in printHList:
     writeInFile(itemized, normalizeHamDict.get(itemized) , probablityForWordsInHam.get(itemized))
outputfile.write("endOfFile\n")
outputfile.write("totalSpamWords "+str(wordsInSpam) + " \n")
outputfile.write("totalHamWords "+str(wordsInHam) + " \n")
outputfile.write("distinctWords "+str(distinctCount) + " \n")
outputfile.write("totalSpamFIles "+str(totalSpamcount) + " \n")
outputfile.write("totalHamFIles "+str(totalHamcount) + " \n")
