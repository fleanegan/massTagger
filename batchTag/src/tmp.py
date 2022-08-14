from tkinter import ttk
import tkinter as tk
         
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
        self.tree.grid(row = 1, column = 1)
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


#tree.config(columns=("col1"))
#style = ttk.Style(root)
#style.configure("Treeview")
#tree.configure(style="Treeview")

root = tk.Tk()
tree = FileView(root)

#sub tree using item attribute to achieve that
tree.insert("FRED")
tree.insert("MAVIS")
tree.insert("BRIGHT")
tree.insert("SOME")
tree.insert("NODES")
tree.insert("1HERE")
tree.insert("2HERE")
tree.insert("3HERE")
tree.insert("4HERE")
tree.insert("5HERE")
tree.insert("6HERE")
tree.insert("7HERE")
tree.insert("8HERE")
tree.insert("9HERE")
tree.insert("10HERE")
tree.insert("11HERE")
tree.insert("12HERE")
tree.insert("13HERE")

root.mainloop()


