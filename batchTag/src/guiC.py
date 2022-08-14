import tkinter as tk
from tkinter import ttk
import re # regular expression library 
from tkinter import END

dummyList = ['abcde', 'sbcde', 'tomate', 'topate', 'tolpat']
dummyWr

class TagSearchBox:
    def __init__(self, window):
        self.inputContentTracker = tk.StringVar()
        self.textEntry = ttk.Entry(window, textvariable=self.inputContentTracker)
        self.textEntry.grid(row=0, column=1)
        self.focus()
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
        
class TagListView:
    def __init__(self, window):
        self.listView = tk.Listbox(window, height = 6, relief='flat')
        self.listView.grid(row = 1, column = 1)
    def clear(self):
        self.listView.delete(0, END)    
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
        self.tree.grid(row = 2, column = 1)
    def select(self, event=None):
        self.tree.selection_toggle(self.tree.focus())
        print (self.tree.selection())
    def moveFocus(self, view, fetchingFunction):
        cur_item = view.focus()
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
        
class Gui:
    def __init__(self):
        self.window = tk.Tk()
        self.TagSearchBox = TagSearchBox(self.window)
        self.TagListView = TagListView(self.window)
        self.FileView = FileView(self.window)
        self.bindings()
        self.window.mainloop()
    def onReturnPress(self, activeWidget):
        my_w = activeWidget.widget
        if len(my_w.curselection()) == 0:
            self.TagSearchBox.focus()
        index = int(my_w.curselection()[0]) # position of selection
        value = my_w.get(index) # selected value 
        self.TagSearchBox.set(value) # set value for string variable of Entry 
        self.TagListView.clear()
        self.TagSearchBox.focus()
    def onDownPress(self, activeWidget):
        self.TagListView.focus()
        self.TagListView.selectFirstOption()
    def onUpPress(self, activeWidget):
        self.TagSearchBox.focus()
        self.TagListView.clear()
    def populateTagList(self, *args):
        elementCandidats = dummyList
        elements = []
        searchString = self.TagSearchBox.get()
        self.TagListView.clear()
        for element in elementCandidats:
            if(re.findall(searchString,element,re.IGNORECASE)):
                elements.append(element)
        self.TagListView.populate(elements)
    def populateFileView(self):
        filesInCurrentWorkingDirectory = lstFilesInDir()
    def bindings(self):
        self.TagListView.bind('<Up>', self.onUpPress)
        self.TagListView.bind('<Return>', self.onReturnPress)
        self.TagSearchBox.bind('<Down>', self.onDownPress)
        self.TagSearchBox.setTrace(self.populateTagList)
        self.window.bind("<Escape>", lambda x: self.window.destroy())
        
#class GuiPresenter:
Gui()