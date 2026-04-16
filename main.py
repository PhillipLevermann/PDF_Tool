import tkinter as tk

from model import PDF_Tool_Model
from view import PDF_Tool_View
from controller import PDF_Tool_Controller



def app():
    root = tk.Tk()

    view  = PDF_Tool_View(root)
    model = PDF_Tool_Model()
    controller = PDF_Tool_Controller(view, model)

    root.mainloop()

if __name__ == '__main__':
    app()