from borb.pdf.document.document import Document
from borb.pdf.page.page import Page
from borb.pdf.canvas.layout.page_layout.multi_column_layout import SingleColumnLayout
from decimal import Decimal
from borb.pdf.canvas.layout.image.image import Image
from borb.pdf.pdf import PDF

from confuse import Configuration
from argparse import ArgumentParser



'''
 Main Class to handle creating the Invoice
'''
class InvoiceGenerator():

    def __init__(self):
        # Base Document 
        self.doc = Document()

        # Only need a single page at the moment. New pages created automatically.
        self.page = Page()
        self.doc.add_page(self.page)

        # Fit all content into a single column
        self.layout = SingleColumnLayout(self.page, vertical_margin = (self.page.get_page_info().get_height() * Decimal(0.02)) )

    # Appends an image to the document.
    def add_image(self, image_path:str, width=Decimal(128), height=Decimal(128)):
        self.layout.add(Image( image_path, width=width, height=height))

    # Generates the file at the given file name/path
    def generate(self, file_name:str):
        with open(file_name, "wb") as pdf_file_handle:
            PDF.dumps(pdf_file_handle, self.doc)




# Helper to laod in the arguments from the command line
def _load_arguments() -> ArgumentParser:
    parser = ArgumentParser(prog=__name__, description="Generates a PDF Invoice")

    parser.add_argument('-c', '--client') 



if __name__ == "__main__":


    document = InvoiceGenerator()

    document.add_image("https://picsum.photos/128/128")

    document.generate("output.pdf")



    