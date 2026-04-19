from pathlib import Path
from pypdf import PdfReader, PdfWriter

class PDF_Tool_Model:

    def get_pdf_info(self, path):
        reader = PdfReader(path)

        return {
            'name': Path(path).name,
            'path': path,
            'pages': len(reader.pages)
        }

    def merge_pdfs(self, list_pdf, savepath): 
        merger = PdfWriter()

        for pdf in list_pdf:
            print(pdf['path'])
            merger.append(pdf['path'])
            
        merger.write(savepath)

    def split_pdfs(self, dict_pdf, savepath):      
        save_path = Path(savepath).parent
        save_name = Path(savepath).stem

        splitted_list = []
        splitted_fragment = []

        for pdf in dict_pdf:
            if pdf['type'] == 'page':
                splitted_fragment.append(pdf)
            elif splitted_fragment:
                splitted_list.append(splitted_fragment)
                splitted_fragment = []
        if splitted_fragment:
            splitted_list.append(splitted_fragment)
    
        cache_reader = {}

        i = 1
        for fragment in splitted_list:
                      
            writer = PdfWriter()

            for pdf in fragment:
                page = pdf['page']
                name = pdf['name']
                path = pdf['path']

                if path not in cache_reader:
                    cache_reader[path] = PdfReader(path)
                
                writer.add_page(cache_reader[path].pages[int(page)-1])

            output_file = save_path / f"{save_name}({i}).pdf"
            writer.write(str(output_file))

            i += 1