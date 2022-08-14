import tkinter as tk
from tkinter import ttk
import re # regular expression library 
from tkinter import END
from batchTag.src.readTags import listFilesInDir
from batchTag.src.readTags import collectPresentTags
from batchTag.src.readTags import deleteTags
from batchTag.src.readTags import addTags
from tkinter import filedialog


class TagSearchBox:
    def __init__(self, window):
        self.inputContentTracker = tk.StringVar()
        self.textEntry = ttk.Entry(window, textvariable=self.inputContentTracker)
    def setPosition(self, row, column):
        self.textEntry.grid(row=row, column=column,sticky='NSEW')
    def bind(self, pattern, function):
        self.textEntry.bind(pattern, function)
    def setTrace(self, function):
        self.inputContentTracker.trace_add("write", function)
    def focus(self):
        self.textEntry.focus()
    def setText(self, text):
        self.inputContentTracker.set(text)
    def get(self):
        return self.textEntry.get()
    def set(self, string):
        return self.inputContentTracker.set(string)
    
class ButtonBox:
    def __init__(self, window):
        self.frame = ttk.Frame(window)
        self.button1 = ttk.Button(self.frame, text="Reset Tag Selection", command=lambda: print("noe"))
        self.button2 = ttk.Button(self.frame, text="Reset File Selection", command=lambda: print("noe"))
        self.button3 = ttk.Button(self.frame, text="ADD Tag Selection", command=lambda: print("noe"))
        self.button4 = ttk.Button(self.frame, text="REMOVE Tag Selection", command=lambda: print("noe"))
        self.button1.pack(side=tk.BOTTOM, expand=True, fill=tk.BOTH)
        self.button2.pack(side=tk.BOTTOM, expand=True, fill=tk.BOTH)
        self.button3.pack(side=tk.BOTTOM, expand=True, fill=tk.BOTH)
        self.button4.pack(side=tk.BOTTOM, expand=True, fill=tk.BOTH)
    def setPosition(self, row, column):
        self.frame.grid(row=row, column=column,sticky='NSEW')
    def bind(self, pattern, function):
        self.frame.bind(pattern, function)
        
class TagListView:
    def __init__(self, window):
        self.listView = tk.Listbox(window, height = 6, relief='flat')
    def setPosition(self, row, column):
        self.listView.grid(row=row, column=column,sticky='NSEW')
    def clear(self):
        self.listView.delete(0, END)    
    def deleteSelectedElement(self, event=None):
        if self.listView.size():
            if len(self.listView.curselection()) == 0:
                self.listView.select_set(0)
            cur_item = self.listView.curselection()[0]
            self.listView.delete(cur_item)
    def focus(self):
        self.listView.focus()
    def selectFirstOption(self):
        self.listView.selection_set(0)
    def bind(self, pattern, function):
        self.listView.bind(pattern, function)
    def populate(self, elements): 
        self.clear()
        for element in elements:
            self.listView.insert(tk.END,element)
    def toList(self):
        return self.listView.get(0, END)
    def inList(self, element):
        if element in self.toList():
            return True
        else:
            return False
         
class FileView:   
    def __init__(self, window):
        self.tree = ttk.Treeview(window,show="tree", selectmode="none")
        self.tree.bind("<ButtonRelease-1>", self.select)
        self.tree.bind("<Down>", self.noHanderPlease)
        self.tree.bind("<Up>", self.noHanderPlease)
        self.tree.bind("<KeyRelease-Down>", self.moveFocusDown)
        self.tree.bind("<KeyRelease-Up>", self.moveFocusUp)
        self.tree.bind("<Return>", lambda e: self.select()) 
        self.tree.bind("<space>", lambda e: self.select()) 
        self.tree.tag_configure('red', background="red")        
        style = ttk.Style(window)
        style.configure("Treeview")
        self.tree.configure(style="Treeview")
    def setFocusOnFirstChild(self):
        self.tree.focus_set()
        children = self.tree.get_children()
        if children:
            self.tree.focus(children[0])
        else:
            print("no children found")
    def setPosition(self, row, column):
        self.tree.grid(row=row, column=column,sticky='NSEW')
    def select(self, event=None):
        self.tree.selection_toggle(self.tree.focus())
        print (self.tree.selection())
    def moveFocus(self, view, fetchingFunction):
        cur_item = view.focus()
        print("move focus")
        cur_item_index = view.index(cur_item)
        next_item = fetchingFunction(cur_item)
        item_count = len(view.get_children())
        if (fetchingFunction == view.next and cur_item_index == item_count - 1):
            return 'break';
        if (fetchingFunction == view.prev and cur_item_index == 0):
            return 'break';
        view.item(cur_item, tags="noColor")
        view.item(next_item, tags="red")
        view.focus(next_item)
        view.yview_moveto(view.index(next_item) / item_count)
        return 'break'
    def moveFocusDown(self, event=None):
        view = event.widget
        self.moveFocus(view, view.next)
        return 'break'  
    def moveFocusUp(self, event=None):
        view = event.widget
        self.moveFocus(view, view.prev)
        return 'break'  
    def noHanderPlease(seilf, event=None):
        return 'break'
    def insert(self, fileName):
        self.tree.insert("", tk.END, text=fileName)
    def clearSelection(self):
        for item in self.tree.selection():
            self.tree.selection_remove(item)
    def selectionToList(self):
        result = []
        for iid in self.tree.selection():
            result.append(self.tree.item(iid)["text"])
        return result
    
class Gui:
    def __init__(self):
        self.window = tk.Tk()
        self.window.geometry("1200x800")
        self.window.grid_columnconfigure(1,weight=1)
        self.window.grid_rowconfigure(1,weight=1)
        self.window.grid_rowconfigure(2,weight=2)
        self.tagSearchBox = TagSearchBox(self.window)
        self.availableTagView = TagListView(self.window)
        self.selectedTagView= TagListView(self.window)
        self.fileView = FileView(self.window)      
        self.fileView.tree.focus_set()
        self.tagSearchBox.setPosition(0, 1)
        self.selectedTagView.setPosition(2, 2)
        self.availableTagView.setPosition(1, 1)
        self.fileView.setPosition(2, 1)
        self.buttonBox = ButtonBox(self.window)
        self.buttonBox.setPosition(1, 2)
        self.window.config(highlightbackground = "red", highlightcolor= "red")
    def initFocus(self):
        self.fileView.setFocusOnFirstChild()
        self.tagSearchBox.focus()
        
class GuiPresenter:
    def __init__(self):
        self.gui = Gui()
        self.filesInCurrentWorkingDirectory = listFilesInDir(workingDir)
        self.bindings()
        self.populateFileView()
        self.clearTagSelection()
        self.gui.initFocus()
        self.gui.window.mainloop()
    def selectTag(self, activeWidget):
        my_w = activeWidget.widget
        if len(my_w.curselection()) == 0:
            self.gui.tagSearchBox.focus()
        index = int(my_w.curselection()[0])
        value = my_w.get(index) 
        self.gui.tagSearchBox.set("")
        self.gui.selectedTagView.listView.insert(0, value)
        self.gui.availableTagView.clear()
        self.gui.tagSearchBox.focus()
    def enterNewTag(self, event=None):
        value = self.gui.tagSearchBox.get()
        if value[1] != '#':
            value = '#' + value
        self.gui.selectedTagView.listView.insert(0, value)
        self.gui.tagSearchBox.set("")
    def moveTagSelectionDown(self, activeWidget):
        self.gui.availableTagView.focus()
        self.gui.availableTagView.selectFirstOption()
    def moveTagSelectionUp(self, activeWidget):
        self.gui.tagSearchBox.focus()
        self.gui.availableTagView.clear()
    def unselectTag(self, activeWidget):
        self.gui.selectedTagView.deleteElement()
    def clearFileSelection(self):
        self.gui.fileView.clearSelection()
    def clearTagSelection(self):
        self.gui.selectedTagView.clear()
        self.populateTagList()
    def addSelectedTagsToFiles(self):
        fileList = self.gui.fileView.selectionToList()
        newTags = self.gui.selectedTagView.toList()
        for file in fileList:
            print("adding to file " + file)
            addTags(file, newTags)
    def removeSelectedTagsFromFiles(self):
        fileList = self.gui.fileView.selectionToList()
        newTags = self.gui.selectedTagView.toList()
        for file in fileList:
            print("removing from file " + file)
            deleteTags(file, newTags)
    def populateTagList(self, *args):
        elementCandidats = collectPresentTags(self.filesInCurrentWorkingDirectory)
        elements = []
        searchString = self.gui.tagSearchBox.get()
        self.gui.availableTagView.clear()
        for element in elementCandidats:
            if(re.findall(searchString,element,re.IGNORECASE) and not self.gui.selectedTagView.inList(element)):
                elements.append(element)
        self.gui.availableTagView.populate(elements)
    def populateFileView(self):
        for file in self.filesInCurrentWorkingDirectory:
            self.gui.fileView.insert(file)
    def bindings(self):
        self.gui.availableTagView.bind('<Escape>', self.moveTagSelectionUp)
        self.gui.availableTagView.bind('<Return>', self.selectTag)
        self.gui.tagSearchBox.bind('<Return>', self.enterNewTag)
        self.gui.tagSearchBox.bind('<Down>', self.moveTagSelectionDown)
        self.gui.selectedTagView.bind('<BackSpace>', self.gui.selectedTagView.deleteSelectedElement)
        self.gui.tagSearchBox.setTrace(self.populateTagList)
        self.gui.buttonBox.button1.configure(command=self.clearTagSelection)
        self.gui.buttonBox.button2.configure(command=self.clearFileSelection)
        self.gui.buttonBox.button3.configure(command=self.addSelectedTagsToFiles)
        self.gui.buttonBox.button4.configure(command=self.removeSelectedTagsFromFiles)
        self.gui.window.bind("<Escape>", lambda x: self.gui.window.destroy())    
        
   
workingDir = "./"
if __name__ == "__main__":
    workingDir = filedialog.askdirectory()
    GuiPresenter()