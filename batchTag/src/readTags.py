import glob
import os.path
import os
import re
from os.path import exists

def listFilesInDir(directory):
    result = []
    for root, dirs, files in os.walk(directory):
        if files:
            for file in files:
                if os.path.splitext(file)[1] == '.md':
                    result.append(os.path.abspath(directory) + '/' + file)
    return result

def collectPresentTags(files):
    result = []
    for textFile in files:
        if exists(textFile):
            with open(textFile,'r') as file:
                for line in file:
                    for word in line.split():
                        if (line[0] == '#'):
                            result.append(word)
    result = list(set(result)) # removing douplicates
    return result

def deleteTags(fileName, listOfTags):
    result = []
    with open(fileName,'r') as file:
        lines = file.readlines()
    for line in lines:
        for tag in listOfTags:
            if line.strip() == tag:
                line = ""
                break ;
            line = re.sub(tag + "[\s\n]", "", line)
        result.append(line)
    with open(fileName, 'w') as file:
        file.writelines(result)

def addTags(fileName, listOfTags):    
    if exists(fileName):
        with open(fileName, 'r') as original: data = original.read()
        with open(fileName, 'w') as modified: 
            for tag in listOfTags:
                if tag not in data:
                    modified.write(tag + "\n")
            modified.write(data)
        
def findFiles(presentFiles, searchString):
    results = []
    for file in presentFiles:
        fileBaseName = os.path.basename(file)
        if (fileBaseName.find(searchString) != -1):
            results.append(file)
        else:
            if exists(file):
                with open(file, 'r') as candidate: 
                    fileContent = candidate.read()
                    if (fileContent.find(searchString) != -1):
                        results.append(file)
    return results