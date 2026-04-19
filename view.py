import tkinter as tk
from tkinter import ttk, filedialog

SPLIT_MARKER = "───── SPLIT ─────"

class PDF_Tool_View:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Tool")
        self.root.geometry("500x320")
        self.root.minsize(300, 320) 

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

        #TREEVIEW MID

        frame_mid = tk.Frame(tab_merge)
        frame_mid.pack(fill=tk.BOTH, expand=True)

        self.treeview_merge = ttk.Treeview(frame_mid,
                                    columns=('page', 'filename', 'path'), 
                                    show='headings')
        self.treeview_merge.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.treeview_merge.heading('page', text='Pages')
        self.treeview_merge.heading('filename', text='Filename')
        self.treeview_merge.heading('path', text='Path')

        self.treeview_merge.column('page', width=50, minwidth=50, stretch=False)
        self.treeview_merge.column('filename', width=200, minwidth=100, stretch=False)
        self.treeview_merge.column('path', width=250, minwidth=100, stretch=True)

        self.treeview_merge.tag_configure('split_marker', 
                                          font=('Arial', 10, 'bold'), 
                                          background="#AAAAAA")

        scrollbar_treeview = tk.Scrollbar(frame_mid, orient=tk.VERTICAL)
        scrollbar_treeview.pack(side=tk.RIGHT, fill=tk.Y)

        scrollbar_treeview.config(command=self.treeview_merge.yview)
        self.treeview_merge.config(yscrollcommand=scrollbar_treeview.set)

        self.treeview_merge.bind('<Button-1>', self._drag_start)
        self.treeview_merge.bind('<B1-Motion>', self._drag_move)
        self.treeview_merge.bind('<ButtonRelease-1>', self.stop_drag)
        self.treeview_merge.bind('<Delete>', self._remove_bind)

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

        #TREEVIEW MID

        frame_mid = tk.Frame(tab_split)
        frame_mid.pack(fill=tk.BOTH, expand=True)

        self.treeview_split = ttk.Treeview(frame_mid,
                                           columns=('page', 'filename', 'path'), 
                                           show='headings')
        self.treeview_split.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.treeview_split.heading('page', text='Page #')
        self.treeview_split.heading('filename', text='Filename')
        self.treeview_split.heading('path', text='Path')

        self.treeview_split.column('page', width=50, minwidth=50, stretch=False)
        self.treeview_split.column('filename', width=200, minwidth=100, stretch=False)
        self.treeview_split.column('path', width=250, minwidth=100, stretch=True)

        self.treeview_split.tag_configure('split_marker', 
                                          font=('Arial', 10, 'bold'),
                                          foreground="#FFFFFF", 
                                          background="#5C5C5C")

        scrollbar_treeview = tk.Scrollbar(frame_mid, orient=tk.VERTICAL)
        scrollbar_treeview.pack(side=tk.RIGHT, fill=tk.Y)

        scrollbar_treeview.config(command=self.treeview_split.yview)
        self.treeview_split.config(yscrollcommand=scrollbar_treeview.set)

        self.treeview_split.bind('<Button-1>', self._drag_start)
        self.treeview_split.bind('<B1-Motion>', self._drag_move)
        self.treeview_split.bind('<ButtonRelease-1>', self.stop_drag)
        self.treeview_split.bind('<Delete>', self._remove_bind)
        
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
        item = event.widget.identify_row(event.y)
        if item:
            self.drag_item = item

    def _drag_move (self, event):
        widget = event.widget

        if not self.drag_item:
            return

        target_item = widget.identify_row(event.y)

        if target_item and target_item != self.drag_item:
            target_index = widget.index(target_item)
            widget.move(self.drag_item, "", target_index)

    def stop_drag(self, event):
        self.drag_item = None

    #######################
    #UTIL METHODS
    #######################

    # INTERNAL

    def _get_files(self, tree):
        list_dict = []

        for id in tree.get_children():
            item = tree.item(id)
            values = item['values']
            tags = item['tags']

            if 'split_marker' in tags:
                list_dict.append({'type': 'split'})
            else:
                list_dict.append({
                    'type': 'page',
                    'page': values[0],
                    'name': values[1],
                    'path': values[2]
                })  

        return list_dict
    
    def _get_item_tags(self, tree, item):
        try:
            return tree.item(item, "tags")
        except Exception:
            return ()

    def _get_item_ids(self, tree):
        return tree.get_children()
    
    def _add_files(self, tree, list):
        for file in list:
            tree.insert('', tk.END, values=(file[0], file[1], file[2]))

    def _clear_tree(self, tree):
        for item in tree.get_children():
            tree.delete(item)

    def _add_split(self, tree, pos):
        tree.insert('', pos, values=('', SPLIT_MARKER, ''), tags=('split_marker'))

    def _remove_sel(self, tree):
        for item in tree.selection():
            tree.delete(item)
    
    def _remove_bind(self, event):
        self._remove_sel(event.widget)

    def _get_sel_index(self, tree):
        selection = tree.selection()
        return tree.index(selection[0]) if selection else None

    def _set_status(self, label, text):
        label.configure(text=text)

    def _load_info_text(self):
        with open('info.txt', 'r', encoding='utf-8') as file:
            return file.read()
        
    #GENERIC

    def ask_open_pdf_files(self):
        selected_pdf = filedialog.askopenfilenames(
            title='Choose PDF files',
            filetypes=[('PDF files', '.pdf')]
        )
        return selected_pdf

    def ask_save_pdf_path(self):
        savepath = filedialog.asksaveasfilename(
                title='Save as..',
                filetypes=[('PDF files', '*.pdf')],
                defaultextension=('.pdf')
            )
        return savepath

    #MERGE

    def get_files_merge(self):
        return self._get_files(self.treeview_merge)
    
    def add_files_merge(self, list):
        self._add_files(self.treeview_merge, list)
    
    def clear_tree_merge(self):
        self._clear_tree(self.treeview_merge)

    def set_status_merge(self, text):
        self._set_status(self.status_merge, text)

    #SPLIT

    def get_item_tags_split(self, item):
        return self._get_item_tags(self.treeview_split, item)

    def get_item_ids_split(self):
        return self._get_item_ids(self.treeview_split)

    def get_files_split(self):
        return self._get_files(self.treeview_split)
    
    def add_files_split(self, list):
        self._add_files(self.treeview_split, list)

    def clear_tree_split(self):
        self._clear_tree(self.treeview_split)

    def add_split(self, pos):
        self._add_split(self.treeview_split, pos)
    
    def remove_sel_split(self):
        self._remove_sel(self.treeview_split)

    def remove_items_split(self, items):
        if items:
            self.treeview_split.delete(*items)

    def get_sel_index_split(self):
        return self._get_sel_index(self.treeview_split)
        
    def set_status_split(self, text):
        self._set_status(self.status_split, text)
