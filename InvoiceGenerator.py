# Borb imports
from borb.pdf.document.document import Document
from borb.pdf.page.page import Page
from borb.pdf.canvas.layout.page_layout.multi_column_layout import SingleColumnLayout
from decimal import Decimal
from borb.pdf.canvas.layout.image.image import Image
from borb.pdf.pdf import PDF
from borb.pdf.canvas.layout.table.fixed_column_width_table import FixedColumnWidthTable as Table
from borb.pdf.canvas.layout.text.paragraph import Paragraph
from borb.pdf.canvas.layout.layout_element import Alignment
from borb.pdf.canvas.color.color import HexColor, X11Color

# General imports
from datetime import datetime


# Settings related imports
from confuse import Configuration
from argparse import ArgumentParser

# local module imports
from client import Client

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

    # Appends a table to the document.
    def add_table(self, table: Table):
        self.layout.add(table)

    # Appends a blank line to the document
    def add_blank_line(self):
        self.layout.add(Paragraph(" "))

    # Generates the file at the given file name/path
    def generate(self, file_name:str):
        with open(file_name, "wb") as pdf_file_handle:
            PDF.dumps(pdf_file_handle, self.doc)

    # Builds a table with the header information. Does not modify the document.
    def build_header(self) -> Table:

        header = Table(number_of_rows=5, number_of_columns=3)
	
        header.add(Paragraph("[Street Address]"))    
        header.add(Paragraph("Date:        ", font="Helvetica-Bold",respect_spaces_in_text=True,  horizontal_alignment=Alignment.RIGHT))    
        now = datetime.now()    
        header.add(Paragraph("%d/%d/%d" % (now.day, now.month, now.year)))
        
        header.add(Paragraph("[City, State, ZIP Code]"))    
        header.add(Paragraph("Invoice #:", font="Helvetica-Bold", horizontal_alignment=Alignment.RIGHT))
        header.add(Paragraph("%d" % 1))   
        
        header.add(Paragraph("[Phone]"))    
        header.add(Paragraph("Due Date:", font="Helvetica-Bold", horizontal_alignment=Alignment.RIGHT))
        header.add(Paragraph("%d/%d/%d" % (now.day, now.month, now.year))) 
        
        header.add(Paragraph("[Email Address]"))    
        header.add(Paragraph(" "))
        header.add(Paragraph(" "))

        header.add(Paragraph("[Company Website]"))
        header.add(Paragraph(" "))
        header.add(Paragraph(" "))

        header.set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2), Decimal(2))    		
        header.no_borders()
        return header

    def build_billing_shipping(self):
        info = Table(number_of_rows=6, number_of_columns=2)  
        info.add(  
            Paragraph(  
                "BILL TO",  
                background_color=HexColor("263238"),  
                font_color=X11Color("White"), 
                padding_bottom=Decimal(4) 
            )  
        )  
        info.add(  
            Paragraph(  
                "SHIP TO",  
                background_color=HexColor("263238"),  
                font_color=X11Color("White"),  
                padding_bottom=Decimal(4)
            )  
        )  
        info.add(Paragraph("[Recipient Name]"))        # BILLING  
        info.add(Paragraph("[Recipient Name]"))        # SHIPPING  
        info.add(Paragraph("[Company Name]"))          # BILLING  
        info.add(Paragraph("[Company Name]"))          # SHIPPING  
        info.add(Paragraph("[Street Address]"))        # BILLING  
        info.add(Paragraph("[Street Address]"))        # SHIPPING  
        info.add(Paragraph("[City, State, ZIP Code]")) # BILLING  
        info.add(Paragraph("[City, State, ZIP Code]")) # SHIPPING  
        info.add(Paragraph("[Phone]"))                 # BILLING  
        info.add(Paragraph("[Phone]"))                 # SHIPPING  
        info.set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2), Decimal(2))  
        info.no_borders()  
        return info

    def build_items(self):







# Helper to laod in the arguments from the command line
def _load_arguments() -> ArgumentParser:
    parser = ArgumentParser(prog=__name__, description="Generates a PDF Invoice")

    # Possible arguments
    parser.add_argument('-c', '--client') 
    parser.add_argument('-h', '--hours') 
    parser.add_argument('-s', '--start') 
    parser.add_argument('-e', '--end') 




if __name__ == "__main__":


    document = InvoiceGenerator()

    document.add_image("https://picsum.photos/128/128")

    document.add_table(document.build_header())
    document.add_blank_line()
    document.add_table(document.build_billing_shipping())

    document.generate("output.pdf")





    