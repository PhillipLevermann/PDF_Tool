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
        self.view.btn_clear_merge.config(command=self.view.clear_listbox_merge)
        self.view.btn_merge.config(command=self.merge_files)

        self.view.btn_select_split.config(command=self.select_split_pages)
        self.view.btn_clear_split.config(command=self.view.clear_listbox_split)
        self.view.btn_add_split.config(command=self.add_split)
        self.view.btn_remove_split.config(command=self.remove_split)
        self.view.btn_split.config(command=self.split_files)

    # MERGE 

    def select_merge(self):
        selected_pdf = filedialog.askopenfilenames(
            title='Choose PDF files',
            filetypes=[('PDF files', '*.pdf')]
        )

        for file in selected_pdf:
            self.view.add_files_merge(file)

        self.view.set_status_merge('DRAG&DROP TO CHANGE ORDER')
        
    def merge_files(self):
        pdf_files = self.view.get_files_merge()
        if pdf_files:
            savepath = filedialog.asksaveasfilename(
                title='Save as..',
                filetypes=[('PDF files', '*.pdf')],
                defaultextension=('*.pdf')
            )

            if not savepath:
                return

            success = self.model.merge_pdfs(pdf_files, savepath)

            if success:
                self.view.set_status_merge('MERGE SUCCESSFUL')
                self.view.clear_listbox_merge()
            else:
                messagebox.showwarning('Error!', 'Merge failed!')    
        else:
            self.view.set_status_merge('NO FILES SELECTED')

    # SPLIT

    def select_split_pages(self):
        selected_pdf = filedialog.askopenfilenames(
            title='Choose PDF files',
            filetypes=[('PDF files', '*.pdf')]
        )

        catalog = self.model.pdf_loader_pages(selected_pdf)

        for pdf in catalog:
            for page in pdf:
                self.view.add_files_split(page)

    def select_split(self):
        selected_pdf = filedialog.askopenfilenames(
            title='Choose PDF files',
            filetypes=[('PDF files', '*.pdf')]
        )

        self.view.clear_listbox_split()

        for file in selected_pdf:
            self.view.add_files_split(file)

        self.view.set_status_split('DRAG&DROP TO CHANGE ORDER')

    def add_split(self):
        pos = self.view.get_index_split()
        if pos:
            insert = pos[0] + 1
            self.view.add_split(insert)
        else:
            self.view.add_split(0)

    def remove_split(self):
        pos = self.view.get_index_split()
        if pos:
            self.view.remove_split(pos[0])

    def split_files(self):
        pdf_files = self.view.get_files_split()
        if pdf_files:
            savepath = filedialog.asksaveasfilename(
                title='Save as..',
                filetypes=[('PDF files', '*.pdf')],
                defaultextension=('*.pdf')
            )

            self.model.split_pdfs(pdf_files, savepath)

        else:
            self.view.set_status_split('NO FILES SELECTED')