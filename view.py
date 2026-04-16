import tkinter as tk
from tkinter import ttk
from model import SPLIT_MARKER

class PDF_Tool_View:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Tool")
        self.root.geometry("500x300")
        self.root.minsize(300, 280) 

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        self._build_tab_merge()
        self._build_tab_split()
        self._build_tab_info()

    def _build_tab_merge(self):
        tab_merge = tk.Frame(self.notebook)
        self.notebook.add(tab_merge, text='Merge')

        #BUTTONS TOP

        frame_top = tk.Frame(tab_merge)
        frame_top.pack(fill=tk.Y)

        self.btn_select_merge = tk.Button(frame_top, text='Select PDF\'s')
        self.btn_select_merge.pack(side=tk.LEFT, padx=1, pady=3)
        self.btn_clear_merge = tk.Button(frame_top, text='Clear')
        self.btn_clear_merge.pack(side=tk.LEFT, padx=1, pady=3)
        self.btn_merge = tk.Button(frame_top, text='Merge')
        self.btn_merge.pack(side=tk.RIGHT, padx=1, pady=3)

        #LISTBOX MID

        frame_mid = tk.Frame(tab_merge)
        frame_mid.pack(fill=tk.BOTH, expand=True)

        self.listbox_merge = tk.Listbox(frame_mid, font=("Consolas", 10))
        self.listbox_merge.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar_listbox = tk.Scrollbar(frame_mid, orient=tk.VERTICAL)
        scrollbar_listbox.pack(side=tk.RIGHT, fill=tk.Y)

        scrollbar_listbox.config(command=self.listbox_merge.yview)
        self.listbox_merge.config(yscrollcommand=scrollbar_listbox.set)

        self.listbox_merge.bind("<Button-1>", self._drag_start)
        self.listbox_merge.bind("<B1-Motion>", self._drag_move)

        #STATUS BOT

        frame_bot = tk.Frame(tab_merge)
        frame_bot.pack(fill=tk.X)

        self.status_merge = tk.Label(frame_bot, text='READY', anchor=tk.CENTER)
        self.status_merge.pack(fill=tk.X, padx=5, pady=5)

    def _build_tab_split(self):
        tab_split = tk.Frame(self.notebook)
        self.notebook.add(tab_split, text='Split')

        #BUTTONS TOP

        frame_top = tk.Frame(tab_split)
        frame_top.pack(fill=tk.Y)

        self.btn_select_split = tk.Button(frame_top, text='Select PDF\'s')
        self.btn_select_split.pack(side=tk.LEFT, padx=1, pady=3)

        self.btn_clear_split = tk.Button(frame_top, text='Clear')
        self.btn_clear_split.pack(side=tk.LEFT, padx=1, pady=3)

        self.btn_add_split = tk.Button(frame_top, text='Add Split')
        self.btn_add_split.pack(side=tk.LEFT, padx=1, pady=3)

        self.btn_remove_split = tk.Button(frame_top, text='Remove')
        self.btn_remove_split.pack(side=tk.LEFT, padx=1, pady=3)

        self.btn_split = tk.Button(frame_top, text='Split')
        self.btn_split.pack(side=tk.RIGHT, padx=1, pady=3)

        #LISTBOX MID

        frame_mid = tk.Frame(tab_split)
        frame_mid.pack(fill=tk.BOTH, expand=True)

        self.listbox_split = tk.Listbox(frame_mid,  font=("Consolas", 10))
        self.listbox_split.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar_listbox = tk.Scrollbar(frame_mid, orient=tk.VERTICAL)
        scrollbar_listbox.pack(side=tk.RIGHT, fill=tk.Y)

        scrollbar_listbox.config(command=self.listbox_split.yview)
        self.listbox_split.config(yscrollcommand=scrollbar_listbox.set)

        self.listbox_split.bind("<Button-1>", self._drag_start)
        self.listbox_split.bind("<B1-Motion>", self._drag_move)

        #STATUS BOT

        frame_bot = tk.Frame(tab_split)
        frame_bot.pack(fill=tk.X)

        self.status_split = tk.Label(frame_bot, text='READY', anchor=tk.CENTER)
        self.status_split.pack(fill=tk.X, padx=5, pady=5)

    def _build_tab_info (self):
        tab_info = tk.Frame(self.notebook)
        self.notebook.add(tab_info, text='Info')

        frame = tk.Frame(tab_info)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        info = tk.Text(frame, wrap=tk.WORD, font=("Segoe UI", 10))
        info.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        info.insert('1.0', self._load_info_text())
        info.config(state=tk.DISABLED)

    def _drag_start (self, event):
        widget = event.widget
        widget.drag_index = widget.nearest(event.y)

    def _drag_move (self, event):
        widget = event.widget

        i = widget.nearest(event.y)
        if i != widget.drag_index:
            entry = widget.get(widget.drag_index)
            widget.delete(widget.drag_index)
            widget.insert(i, entry)
            widget.drag_index = i

    #######################
    #UTIL METHODS
    #######################

    def _get_files(self, listbox):
        return listbox.get(0, tk.END)
    
    def _add_files(self, listbox, file):
        listbox.insert(tk.END, file)

    def _clear_listbox(self, listbox):
        listbox.delete(0, tk.END)

    def _add_split(self, listbox, pos):
        listbox.insert(pos, SPLIT_MARKER)

    def _remove_entry(self, listbox, pos):
        listbox.delete(pos)

    def _get_index(self, listbox):
        return (listbox.curselection())

    def _set_status(self, label, text):
        label.configure(text=text)

    def _load_info_text(self):
        with open('info.txt', 'r', encoding='utf-8') as file:
            return file.read()
        
    #MERGE
    def get_files_merge(self):
        return self._get_files(self.listbox_merge)
    
    def add_files_merge(self, file):
        self._add_files(self.listbox_merge, file)
    
    def clear_listbox_merge(self):
        self._clear_listbox(self.listbox_merge)

    def set_status_merge(self, text):
        self._set_status(self.status_merge, text)
    #SPLIT
    def get_files_split(self):
        return self._get_files(self.listbox_split)
    
    def add_files_split(self, file):
        self._add_files(self.listbox_split, file)

    def clear_listbox_split(self):
        self._clear_listbox(self.listbox_split)

    def add_split(self, pos):
        return self._add_split(self.listbox_split, pos)
    
    def remove_split(self, pos):
        self._remove_entry(self.listbox_split, pos)

    def get_index_split(self):
        return self._get_index(self.listbox_split)

    def set_status_split(self, text):
        self._set_status(self.status_split, text)