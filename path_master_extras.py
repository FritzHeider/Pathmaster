import os
import tkinter as tk
from tkinter import ttk

class DirectoryContentPanel:
    def __init__(self, master):
        self.frame = ttk.Frame(master)
        self.frame.pack(fill=tk.BOTH, expand=True)
        self.tree = ttk.Treeview(self.frame, columns=('Name', 'Size', 'Modified'))
        self.tree.heading('#0', text='Name')
        self.tree.heading('#1', text='Size')
        self.tree.heading('#2', text='Modified')
        self.tree.column('#0', stretch=tk.YES)
        self.tree.column('#1', stretch=tk.YES)
        self.tree.column('#2', stretch=tk.YES)
        self.tree.pack(fill=tk.BOTH, expand=True)
        self.populate_tree('/path/to/start')

    def populate_tree(self, path):
        for entry in os.scandir(path):
            if entry.is_dir():
                node = self.tree.insert('', 'end', text=entry.name, values=('', 'Folder'))
                self.populate_tree_subdir(node, entry.path)
            else:
                self.tree.insert('', 'end', text=entry.name, values=(os.path.getsize(entry.path), 'File'))

    def populate_tree_subdir(self, parent, path):
        try:
            for entry in os.scandir(path):
                if entry.is_dir():
                    node = self.tree.insert(parent, 'end', text=entry.name, values=('', 'Folder'))
                    self.populate_tree_subdir(node, entry.path)
                else:
                    self.tree.insert(parent, 'end', text=entry.name, values=(os.path.getsize(entry.path), 'File'))
        except PermissionError:
            pass  # Handle permissions or add a logging statement here
