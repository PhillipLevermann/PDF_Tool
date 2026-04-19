from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from view import PDF_Tool_View
    from model import PDF_Tool_Model

from tkinter import filedialog, messagebox

class PDF_Tool_Controller:
    def __init__(self, view: PDF_Tool_View, model: PDF_Tool_Model):
        self.view = view
        self.model = model

        self._bind_events()

    def _bind_events(self):
        self.view.btn_select_merge.config(command=self.select_merge)
        self.view.btn_clear_merge.config(command=self.view.clear_tree_merge)
        self.view.btn_merge.config(command=self.merge_files)

        self.view.btn_select_split.config(command=self.select_split)
        self.view.btn_clear_split.config(command=self.view.clear_tree_split)
        self.view.btn_add_split.config(command=self.add_split)
        self.view.btn_remove_split.config(command=self.view.remove_sel_split)
        self.view.btn_split.config(command=self.split_files)

    # MERGE 

    def select_merge(self):
        selected_pdf = self.view.ask_open_pdf_files()

        if not selected_pdf:
            return

        entries = []

        for pdf in selected_pdf:
            pdf_info = self.model.get_pdf_info(pdf)

            pages = pdf_info['pages']
            name = pdf_info['name']
            path = pdf_info['path']

            
            entries.append((pages, name, path))

        self.view.add_files_merge(entries)
        
    def merge_files(self):
        pdf_files = self.view.get_files_merge()
        if pdf_files:
            savepath = self.view.ask_save_pdf_path()
            if not savepath:
                return

            self.model.merge_pdfs(pdf_files, savepath)

    # SPLIT

    def _is_split_marker(self, item):
        return "split_marker" in self.view.get_item_tags_split(item)

    def _remove_unnecessary_splits(self):
        items = self.view.get_item_ids_split()

        if not items:
            return

        to_delete = []
        last_was_split = False

        for item in items:
            is_split = self._is_split_marker(item)

            if is_split and last_was_split:
                to_delete.append(item)

            last_was_split = is_split

        if items and self._is_split_marker(items[0]):
            to_delete.append(items[0])

        if items and self._is_split_marker(items[-1]):
            to_delete.append(items[-1])

        self.view.remove_items_split(set(to_delete))

    def select_split(self):
        selected_pdf = self.view.ask_open_pdf_files()

        if not selected_pdf:
            return

        entries = []

        for pdf in selected_pdf:
            pdf_info = self.model.get_pdf_info(pdf)

            pages = pdf_info['pages']
            name = pdf_info['name']
            path = pdf_info['path']

            for i in range(1, pages + 1):
                entries.append((i, name, path))

        self.view.add_files_split(entries)

    def add_split(self):
        pos = self.view.get_sel_index_split()
        if pos is not None:
            insert = pos + 1
            self.view.add_split(insert)
        else:
            self.view.add_split(0)
        self._remove_unnecessary_splits()

    def split_files(self):
        self._remove_unnecessary_splits()

        pdf_files = self.view.get_files_split()

        if pdf_files:
            savepath = self.view.ask_save_pdf_path()

            self.model.split_pdfs(pdf_files, savepath)

        else:
            self.view.set_status_split('NO FILES SELECTED')

