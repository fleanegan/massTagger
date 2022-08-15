import unittest

from batchTag.src.readTags import listFilesInDir
from batchTag.src.readTags import collectPresentTags
from batchTag.src.readTags import deleteTags
from batchTag.src.readTags import addTags
from batchTag.src.readTags import findFiles
import os

def createFile(fileName, content):
    f = open(fileName, "w")
    f.write(content)
    f.close()

testDirectory = "batchTag/test/assets/dummyDir/"

class TestGetTags(unittest.TestCase):
    def test_getFileNames(self):
        result = listFilesInDir(testDirectory)
        self.assertEqual(len(result), 5)
    def test_getPresentTags(self):
        files = listFilesInDir(testDirectory)
        result = collectPresentTags(files)
        self.assertEqual(len(result), 3)

class TestDeleteTags(unittest.TestCase):
    def test_DeleteTagInMiddleOfLine(self):
        testFileName = testDirectory + "containsTag.md"
        createFile(testFileName, "this is #a tag");
        tagsToBeDeleted = ["#a", "#b"]
        deleteTags(testFileName, tagsToBeDeleted)
        with open(testFileName, "r") as file:
            self.assertEqual(file.read(), "this is tag")
        os.remove(os.path.abspath(testFileName)) 
            
    def test_lineOnlyTag(self):
        testFileName = testDirectory + "containsTag.md"
        createFile(testFileName, "#a");
        tagsToBeDeleted = ["#a", "#b"]
        deleteTags(testFileName, tagsToBeDeleted)
        with open(testFileName, "r") as file:
            self.assertEqual(file.read(), "")
        os.remove(os.path.abspath(testFileName)) 
        
    def test_lineWithTagAndSpace(self):
        testFileName = testDirectory + "containsTag.md"
        createFile(testFileName, " #a  ");
        tagsToBeDeleted = ["#a", "#b"]
        deleteTags(testFileName, tagsToBeDeleted)
        with open(testFileName, "r") as file:
            self.assertEqual(file.read(), "")
        os.remove(os.path.abspath(testFileName)) 
            
    def test_lineWithTagAndWithoutSpace(self):
        testFileName = testDirectory + "containsTag.md"
        createFile(testFileName, " test#a  ");
        tagsToBeDeleted = ["#a", "#b"]
        deleteTags(testFileName, tagsToBeDeleted)
        with open(testFileName, "r") as file:
            self.assertEqual(file.read(), " test ")
        os.remove(os.path.abspath(testFileName))
            
class TestAddTags(unittest.TestCase):
    def test_AddTagToEmptyFile(self):
        testFileName = testDirectory + "doesNotContainTagOnCreation.md"
        createFile(testFileName, "")
        tagsToAdd = ["#This", "#is"]
        addTags(testFileName, tagsToAdd)
        with open(testFileName, "r") as file:
            self.assertEqual(file.read(), "#This\n#is\n")
        file.close()
        os.remove(os.path.abspath(testFileName)) 
    def test_AddOnlyNewTagToFile(self):
        testFileName = testDirectory + "doesNotContainTagOnCreation.md"
        tagsToAdd = ["#This", "#is"]
        createFile(testFileName, tagsToAdd[0])
        addTags(testFileName, tagsToAdd)
        with open(testFileName, "r") as file:
            self.assertEqual(file.read(), "#is\n#This")
        file.close()
        os.remove(os.path.abspath(testFileName)) 
    def test_AddTagToFileDoesNotDeleteText(self):
        testFileName = testDirectory + "doesNotContainTagOnCreation.md"
        tagsToAdd = ["#This", "#is"]
        createFile(testFileName, "this is banana")
        addTags(testFileName, tagsToAdd)
        with open(testFileName, "r") as file:
            self.assertEqual(file.read(), "#This\n#is\nthis is banana")
        file.close()
        os.remove(os.path.abspath(testFileName)) 
        
def getStringsContainingSub(inList, searchString):
    return [s for s in inList if searchString in s]
        
class FindFiles(unittest.TestCase):
    def test_FileBySearchingFileName(self):
        searchString = "ByNa"
        presentFiles = listFilesInDir(testDirectory)
        foundFiles = findFiles(presentFiles, searchString)
        self.assertEqual(len(foundFiles), 1)
        self.assertEqual(os.path.basename(foundFiles[0]), "ByName.md")
    def test_FileBySearchingFileContent(self):
        searchString = "is"
        presentFiles = listFilesInDir(testDirectory)
        foundFiles = findFiles(presentFiles, searchString)
        self.assertEqual(len(foundFiles), 2)
        self.assertEqual(len(getStringsContainingSub(foundFiles, "a.md")), 1)
        self.assertEqual(len(getStringsContainingSub(foundFiles, "find.md")), 1)
    def test_DoNotSearchInFilePath(self):
        searchString = "assets"
        presentFiles = listFilesInDir(testDirectory)
        foundFiles = findFiles(presentFiles, searchString)
        self.assertEqual(len(foundFiles), 0)

if __name__ == '__main__':
    unittest.main()

