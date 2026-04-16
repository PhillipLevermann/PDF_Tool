from pathlib import Path
from pypdf import PdfReader, PdfWriter

SPLIT_MARKER = "────────── SPLIT ──────────"

class PDF_Tool_Model:
    def pdf_loader_pages(self, list_pdf):

        list = []
        pdf_splitted = []

        for pdf in list_pdf:
            reader = PdfReader(pdf)
            for i in range(len(reader.pages)):
                i += 1
                pdf_splitted.append(f'{pdf}::{i}')
            list.append(pdf_splitted)
            pdf_splitted = []

        return list

    def merge_pdfs(self, list_pdf, outputpath): 
        try:
            merger = PdfWriter()
            for pdf in list_pdf:
                merger.append(pdf)
            merger.write(outputpath)
            return True
        except Exception as e:
            print(e)
            return False

    def split_pdfs(self, list_pdf, savepath):      
        save_path = Path(savepath).parent
        save_name = Path(savepath).stem

        splitted_list = []
        splitted_fragment = []

        for pdf in list_pdf:
            if pdf != SPLIT_MARKER:
                splitted_fragment.append(pdf)
            elif splitted_fragment:
                splitted_list.append(splitted_fragment)
                splitted_fragment = []

        if splitted_fragment:
            if splitted_fragment[0] != SPLIT_MARKER:
                splitted_list.append(splitted_fragment)
    
        cache_reader = {}

        i = 1
        for fragment in splitted_list:
                      
            writer = PdfWriter()

            for pdf in fragment:
                path, page = pdf.rsplit("::", 1)

                if path not in cache_reader:
                    cache_reader[path] = PdfReader(path)
                
                writer.add_page(cache_reader[path].pages[int(page)-1])

            output_file = save_path / f"{save_name}({i}).pdf"
            writer.write(str(output_file))

            i += 1