import tkinter as tk
from tkinter import ttk, filedialog

SPLIT_MARKER = "──── ✂ ────"

class PDF_Tool_View:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Tool")
        self.root.geometry("800x500")
        self.root.minsize(800, 500) 

        self.drag_item = None
        
        #COLORS
        self.colors = {
            "bg_main": "#FFFFFF",
            "bg_off": "#FFFFFF",
            "button_bg": "#E9E9E9",
            "button_fg": "#000000",
            "button_active_bg": "#6DA2DB",
            "button_active_fg": "#FFFFFF"
        }
        self.root["bg"] = self.colors['bg_off']

        #GRID CONFIG
        self.root.grid_rowconfigure(0, minsize=35)  # Tab Buttons
        self.root.grid_rowconfigure(1, weight=1)  # Tabs
        self.root.grid_columnconfigure(0, weight=1)

        #STYLES
        self.root.option_add("*Font", ("Segoe UI", 10))
        style = ttk.Style()
        style.configure(".", font=("Segoe UI", 10))
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))

        #FRAME HANDLING
        self._build_frame_tab_select()
        self._build_frame_content()
        self._build_tab_merge()
        self._build_tab_split()
        self._build_tab_info()

        self.switch_tab("merge")

    #FRAME BUILDERS
    def _build_frame_tab_select(self):
        frame_tab = tk.Frame(self.root, bg=self.colors['bg_off'])
        frame_tab.grid(row=0, column=0, sticky="ew", padx=5)

        self.btn_tab_merge = self._create_tab_button(frame_tab, 'Merge')
        self.btn_tab_merge.pack(side=tk.LEFT, padx=3)

        self.btn_tab_split = self._create_tab_button(frame_tab, 'Split')
        self.btn_tab_split.pack(side=tk.LEFT, padx=3)

        self.btn_tab_info = self._create_tab_button(frame_tab, 'Info')
        self.btn_tab_info.pack(side=tk.RIGHT, padx=3)

    def _build_frame_content(self):
        self.frame_content = tk.Frame(self.root, bg=self.colors['bg_main'])
        self.frame_content.grid(row=1, column=0, sticky="nsew")

        self.frame_content.grid_rowconfigure(0, weight=1)
        self.frame_content.grid_columnconfigure(0, weight=1)

    def _build_tab_merge(self):
        self.frame_tab_merge = tk.Frame(self.frame_content, bg=self.colors['bg_main'])
        self.frame_tab_merge.grid(row=0, column=0, sticky="nsew")

        self.frame_tab_merge.grid_rowconfigure(0, minsize=50)  # Title
        self.frame_tab_merge.grid_rowconfigure(1, weight=1)  # Tree + Sidebar
        self.frame_tab_merge.grid_rowconfigure(2, weight=0)  # Bottom
        self.frame_tab_merge.grid_rowconfigure(3, weight=0)  # Main

        self.frame_tab_merge.grid_columnconfigure(0, weight=1)  # Tree
        self.frame_tab_merge.grid_columnconfigure(1, weight=0)  # Sidebar

        # TITLE
        frame_title = tk.Frame(self.frame_tab_merge, bg=self.colors['bg_main'])
        frame_title.grid(row=0, column=0, columnspan=2, sticky="ew", padx=5)

        title = tk.Label(
            frame_title,
            text="Merge PDF files",
            bg=self.colors['bg_main'],
            fg="black",
            font=("Segoe UI", 14, "bold")
        )
        title.pack(anchor=tk.W)

        # TREE
        frame_tree = tk.Frame(self.frame_tab_merge, bg=self.colors['bg_main'])
        frame_tree.grid(row=1, column=0, sticky=tk.NSEW, padx=(5, 0))

        frame_tree.grid_rowconfigure(0, weight=1)
        frame_tree.grid_columnconfigure(0, weight=1)

        # SIDEBAR
        frame_sidebar = tk.Frame(self.frame_tab_merge, bg=self.colors['bg_main'])
        frame_sidebar.grid(row=1, column=1, sticky="ns", padx=5)

        self.btn_merge_move_up = self._create_sidebar_button(frame_sidebar, "↑")
        self.btn_merge_move_up.pack(fill="x", pady=2)

        self.btn_merge_remove = self._create_sidebar_button(frame_sidebar, "×")
        self.btn_merge_remove.pack(fill="x", pady=2)

        self.btn_merge_move_dn = self._create_sidebar_button(frame_sidebar, "↓")
        self.btn_merge_move_dn.pack(fill="x", pady=2)
  
        # BOTTOM
        frame_bottom = tk.Frame(self.frame_tab_merge, bg=self.colors['bg_main'])
        frame_bottom.grid(row=2, column=0, columnspan=2, sticky="ew", padx=5, pady=(5, 2))

        self.btn_merge_select = self._create_bot_button(frame_bottom, 'Select PDF(s)')
        self.btn_merge_select.pack(side=tk.LEFT, padx=1, pady=3)

        self.btn_merge_clear = self._create_bot_button(frame_bottom, 'Clear all')
        self.btn_merge_clear.pack(side=tk.LEFT, padx=1, pady=3)

        # MAIN
        frame_main = tk.Frame(self.frame_tab_merge, bg=self.colors['bg_main'])
        frame_main.grid(row=3, column=0, columnspan=2, sticky="ew", padx=5, pady=(2, 5))

        self.btn_merge = self._create_main_button(frame_main, 'Merge')
        self.btn_merge.pack(padx=1, pady=3)

        #TREEVIEW

        self.treeview_merge = ttk.Treeview(frame_tree,
                                           columns=('page', 'filename', 'path'),
                                           show='headings')
        self.treeview_merge.grid(row=0, column=0, sticky="nsew")

        self.treeview_merge.heading('page', text='Pages')
        self.treeview_merge.heading('filename', text='Filename')
        self.treeview_merge.heading('path', text='Path')

        self.treeview_merge.column('page', width=50, minwidth=50, stretch=False)
        self.treeview_merge.column('filename', width=200, minwidth=100, stretch=False)
        self.treeview_merge.column('path', width=250, minwidth=100, stretch=True)

        self.treeview_merge.tag_configure('split_marker', 
                                          font=('Segoe UI', 10, 'bold'), 
                                          background="#AAAAAA")

        scrollbar_treeview = tk.Scrollbar(frame_tree, orient=tk.VERTICAL)
        scrollbar_treeview.grid(row=0, column=1, sticky="ns")

        scrollbar_treeview.config(command=self.treeview_merge.yview)
        self.treeview_merge.config(yscrollcommand=scrollbar_treeview.set)

        self.treeview_merge.bind('<Button-1>', self._drag_start)
        self.treeview_merge.bind('<B1-Motion>', self._drag_move)
        self.treeview_merge.bind('<ButtonRelease-1>', self._stop_drag)
        self.treeview_merge.bind('<Delete>', self._remove_bind)

    def _build_tab_split(self): 
        self.frame_tab_split = tk.Frame(self.frame_content, bg=self.colors['bg_main'])
        self.frame_tab_split.grid(row=0, column=0, sticky="nsew")

        self.frame_tab_split.grid_rowconfigure(0, minsize=50)  # Title
        self.frame_tab_split.grid_rowconfigure(1, weight=1)  # Tree + Sidebar
        self.frame_tab_split.grid_rowconfigure(2, weight=0)  # Bottom
        self.frame_tab_split.grid_rowconfigure(3, weight=0)  # Main

        self.frame_tab_split.grid_columnconfigure(0, weight=1)  # Tree
        self.frame_tab_split.grid_columnconfigure(1, weight=0)  # Sidebar

        # TITLE
        frame_title = tk.Frame(self.frame_tab_split, bg=self.colors['bg_main'])
        frame_title.grid(row=0, column=0, columnspan=2, sticky="ew", padx=5)

        title = tk.Label(
            frame_title,
            text="Split PDF files",
            bg=self.colors['bg_main'],
            fg="black",
            font=("Segoe UI", 14, "bold")
        )
        title.pack(anchor=tk.W)

        # TREE
        frame_tree = tk.Frame(self.frame_tab_split, bg=self.colors['bg_main'])
        frame_tree.grid(row=1, column=0, sticky=tk.NSEW, padx=(5, 0))

        frame_tree.grid_rowconfigure(0, weight=1)
        frame_tree.grid_columnconfigure(0, weight=1)

        # SIDEBAR
        frame_sidebar = tk.Frame(self.frame_tab_split, bg=self.colors['bg_main'])
        frame_sidebar.grid(row=1, column=1, sticky="ns", padx=5)

        self.btn_split_move_up = self._create_sidebar_button(frame_sidebar, "↑")
        self.btn_split_move_up.pack(fill="x", pady=2)

        self.btn_split_remove = self._create_sidebar_button(frame_sidebar, "×")
        self.btn_split_remove.pack(fill="x", pady=2)

        self.btn_split_move_dn = self._create_sidebar_button(frame_sidebar, "↓")
        self.btn_split_move_dn.pack(fill="x", pady=2)
  
        # BOTTOM
        frame_bottom = tk.Frame(self.frame_tab_split, bg=self.colors['bg_main'])
        frame_bottom.grid(row=2, column=0, columnspan=2, sticky="ew", padx=5, pady=(5, 2))

        self.btn_split_select = self._create_bot_button(frame_bottom, 'Select PDF(s)')
        self.btn_split_select.pack(side=tk.LEFT, padx=1, pady=3)

        self.btn_split_clear = self._create_bot_button(frame_bottom, 'Clear all')
        self.btn_split_clear.pack(side=tk.LEFT, padx=1, pady=3)

        self.btn_add_split = self._create_bot_button(frame_bottom, 'Add Split')
        self.btn_add_split.pack(side=tk.RIGHT, padx=(1, 36), pady=3)

        # MAIN
        frame_main = tk.Frame(self.frame_tab_split, bg=self.colors['bg_main'])
        frame_main.grid(row=3, column=0, columnspan=2, sticky="ew", padx=5, pady=(2, 5))

        self.btn_split = self._create_main_button(frame_main, 'Split')
        self.btn_split.pack(padx=1, pady=3)

        #TREEVIEW

        self.treeview_split = ttk.Treeview(frame_tree,
                                           columns=('page', 'filename', 'path'),
                                           show='headings')
        self.treeview_split.grid(row=0, column=0, sticky="nsew")

        self.treeview_split.heading('page', text='Page #')
        self.treeview_split.heading('filename', text='Filename')
        self.treeview_split.heading('path', text='Path')

        self.treeview_split.column('page', width=50, minwidth=50, stretch=False)
        self.treeview_split.column('filename', width=200, minwidth=100, stretch=False)
        self.treeview_split.column('path', width=250, minwidth=100, stretch=True)

        self.treeview_split.tag_configure('split_marker', 
                                          font=('Segoe UI', 10), 
                                          background="#C8D4E0",
                                          foreground='#666666',
                                          )

        scrollbar_treeview = tk.Scrollbar(frame_tree, orient=tk.VERTICAL)
        scrollbar_treeview.grid(row=0, column=1, sticky="ns")

        scrollbar_treeview.config(command=self.treeview_split.yview)
        self.treeview_split.config(yscrollcommand=scrollbar_treeview.set)

        self.treeview_split.bind('<Button-1>', self._drag_start)
        self.treeview_split.bind('<B1-Motion>', self._drag_move)
        self.treeview_split.bind('<ButtonRelease-1>', self._stop_drag)
        self.treeview_split.bind('<Delete>', self._remove_bind)

    def _build_tab_info(self):
        self.frame_tab_info = tk.Frame(self.frame_content, bg=self.colors['bg_main'])
        self.frame_tab_info.grid(row=0, column=0, sticky=tk.NSEW, padx=5, pady=5)

        info = tk.Text(
            self.frame_tab_info,
            bg=self.colors['bg_main'],
            fg="black",
            bd=0,
            relief="flat",
            highlightthickness=0,
            insertbackground="black",  # Cursor sichtbar machen
            padx=10,
            pady=10,
            wrap="word"
        )
        info.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        info.insert('1.0', self._load_info_text())
        info.config(state=tk.DISABLED)

    #BUTTON BUILDERS
    def _create_tab_button(self, parent, text):
        return tk.Button(
            parent,
            text=text,
            width=12,
            font=("Segoe UI", 12),
            bg=self.colors['button_bg'],
            fg=self.colors['button_fg'],
            activebackground=self.colors['button_active_bg'],
            activeforeground=self.colors['button_active_fg'],
            relief="flat",
            bd=0,
            highlightthickness=0,
            cursor="hand2",
        )
    
    def _create_sidebar_button(self, parent, text):
        return tk.Button(
            parent,
            text=text,
            width=3,
            font=("Segoe UI", 11, "bold"),
            bg=self.colors['button_bg'],
            fg=self.colors['button_fg'],
            activebackground=self.colors['button_active_bg'],
            activeforeground=self.colors['button_active_fg'],
            relief="flat",
            bd=0,
            highlightthickness=0,
            cursor="hand2",
            pady=6
        )
    
    def _create_bot_button(self, parent, text):
        return tk.Button(
            parent,
            text=text,
            width=12,
            font=("Segoe UI", 12),
            bg=self.colors['button_bg'],
            fg=self.colors['button_fg'],
            activebackground=self.colors['button_active_bg'],
            activeforeground=self.colors['button_active_fg'],
            relief="flat",
            bd=0,
            highlightthickness=0,
            cursor="hand2",
        )
        
    def _create_main_button(self, parent, text):
        return tk.Button(
            parent,
            text=text,
            width=12,
            font=("Segoe UI", 12, 'bold'),
            bg='#6DA2DB',
            fg='#FFFFFF',
            activebackground='#5487BE',
            activeforeground='#FFFFFF',
            relief="flat",
            bd=0,
            highlightthickness=0,
            cursor="hand2",
        )
    
    #NAVIGATION
    def switch_tab(self, tab_name):
        tabs = {
            "merge": self.frame_tab_merge,
            "split": self.frame_tab_split,
            "info": self.frame_tab_info
        }

        buttons = {
            "merge": self.btn_tab_merge,
            "split": self.btn_tab_split,
            "info": self.btn_tab_info
        }

        tabs[tab_name].tkraise()

        for name, button in buttons.items():
            if name == tab_name:
                button.config(
                    bg=self.colors["button_active_bg"],
                    fg=self.colors["button_active_fg"]
                )
            else:
                button.config(
                    bg=self.colors["button_bg"],
                    fg=self.colors["button_fg"]
                )

    #EVENT HANDLERS
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

    def _stop_drag(self, event):
        self.drag_item = None

    def _remove_bind(self, event):
        self._remove_sel(event.widget)

    #TREE HELPERS
    def _collect_tree_data(self, tree):
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
    
    def _get_sel_index(self, tree):
        selection = tree.selection()
        return tree.index(selection[0]) if selection else None

    def _move_selected_up(self, tree):
        items = tree.selection()

        if not items:
            return

        for item in items:
            index = tree.index(item)
            if index > 0:
                tree.move(item, '', index - 1)

        tree.selection_set(items)

    def _move_selected_down(self, tree):
        items = tree.selection()

        if not items:
            return

        for item in reversed(items):
            index = tree.index(item)
            if index < len(tree.get_children()) - 1:
                tree.move(item, '', index + 1)

        tree.selection_set(items)

    #OTHER HELPERS
    def _load_info_text(self):
        with open('info.txt', 'r', encoding='utf-8') as file:
            return file.read()
    
    #DIALOGS
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

    #PUBLIC METHODS
    #MERGE
    def get_files_merge(self):
        return self._collect_tree_data(self.treeview_merge)
    
    def add_files_merge(self, list):
        self._add_files(self.treeview_merge, list)
    
    def clear_tree_merge(self):
        self._clear_tree(self.treeview_merge)

    def remove_sel_merge(self):
        self._remove_sel(self.treeview_merge)

    def move_selected_up_merge(self):
        self._move_selected_up(self.treeview_merge)

    def move_selected_down_merge(self):
        self._move_selected_down(self.treeview_merge)

    #SPLIT
    def get_item_tags_split(self, item):
        return self._get_item_tags(self.treeview_split, item)

    def get_item_ids_split(self):
        return self._get_item_ids(self.treeview_split)

    def get_files_split(self):
        return self._collect_tree_data(self.treeview_split)
    
    def add_files_split(self, list):
        self._add_files(self.treeview_split, list)

    def clear_tree_split(self):
        self._clear_tree(self.treeview_split)

    def add_split_marker_split(self, pos):
        self._add_split(self.treeview_split, pos)
    
    def remove_selection_split(self):
        self._remove_sel(self.treeview_split)

    def remove_items_split(self, items):
        if items:
            self.treeview_split.delete(*items)

    def get_sel_index_split(self):
        return self._get_sel_index(self.treeview_split)
    
    def move_selected_up_split(self):
        self._move_selected_up(self.treeview_split)

    def move_selected_down_split(self):
        self._move_selected_down(self.treeview_split)













                
  


