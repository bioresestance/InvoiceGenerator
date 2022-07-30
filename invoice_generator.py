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
from borb.pdf.canvas.layout.table.table import TableCell

# General imports
from datetime import datetime
from dataclasses import dataclass
from typing import List

# Settings related imports
from confuse import Configuration
from argparse import ArgumentParser

# local module imports
from billable_item import BillableItem
from client import Client
from company import Company




TOP_ROW_TABLE_COLOR = HexColor("263238")
ODD_ROW_TABLE_COLOR = HexColor("BBBBBB") 
EVEN_ROW_TABLE_COLOR = HexColor("FFFFFF") 



'''
Class that generates a PDF invoice from provided data.
'''
class InvoiceGenerator():

    def __init__(self, company:Company, client:Client):

        self.company = company
        self.client = client

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
	
        header.add(Paragraph(f"{self.company.name}"))    
        header.add(Paragraph("Date:        ", font="Helvetica-Bold",respect_spaces_in_text=True,  horizontal_alignment=Alignment.RIGHT))    
        now = datetime.now()    
        header.add(Paragraph("%d/%d/%d" % (now.day, now.month, now.year)))
        
        header.add(Paragraph(f"{self.company.address}"))    
        header.add(Paragraph("Invoice #:", font="Helvetica-Bold", horizontal_alignment=Alignment.RIGHT))
        header.add(Paragraph("%d" % 1))   
        
        header.add(Paragraph(f"{self.company.phone}"))    
        header.add(Paragraph("Due Date:", font="Helvetica-Bold", horizontal_alignment=Alignment.RIGHT))
        header.add(Paragraph("%d/%d/%d" % (now.day, now.month, now.year))) 
        
        header.add(Paragraph(f"{self.company.email}"))    
        header.add(Paragraph(" "))
        header.add(Paragraph(" "))

        header.add(Paragraph(f"{self.company.website}"))
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

    # Builds the table of billable items.
    def build_items(self, items_to_bill: List[BillableItem]):
        
        sub_total = 0
        item_table = Table(number_of_rows=14, number_of_columns=4)  
        
        # Builds the Table header. Dark Background with white text.
        for heading in ["DESCRIPTION", "QTY", "UNIT PRICE", "AMOUNT"]:
            item_table.add( TableCell( Paragraph(heading, font_color=X11Color("White")), background_color=TOP_ROW_TABLE_COLOR))     
                

        # Build the items content. 
        for i in range(0, 10):

            # Odd and even rows will alternate background.
            row_color = EVEN_ROW_TABLE_COLOR if (i % 2) else ODD_ROW_TABLE_COLOR

            if i < len(items_to_bill):
                # Item Description
                item_table.add(TableCell(Paragraph(items_to_bill[i].item_description), background_color=row_color))
                # Item Quantity
                item_table.add(TableCell(Paragraph(str(items_to_bill[i].item_quantity)), background_color=row_color))
                # Unit Price
                item_table.add(TableCell(Paragraph(f"${items_to_bill[i].item_unit_price:.2f}"), background_color=row_color))

                # Total Amount
                item_amount = items_to_bill[i].item_quantity * items_to_bill[i].item_unit_price
                sub_total += item_amount
                item_table.add(TableCell(Paragraph(f"${item_amount}"), background_color=row_color))
            else:
                # No more items, fill in the rest of the rows
                for _ in range(0, 4):
                    item_table.add(TableCell(Paragraph(" "), background_color=row_color))

        # Build the final total section

        # Sub-total
        item_table.add(TableCell(Paragraph("Sub-Total", horizontal_alignment=Alignment.RIGHT),  col_span=3))
        item_table.add(TableCell(Paragraph(f"${sub_total:.2f}", horizontal_alignment=Alignment.RIGHT),  col_span=1))

        # Taxes
        item_table.add(TableCell(Paragraph("GST (5%)", horizontal_alignment=Alignment.RIGHT),  col_span=3))
        item_table.add(TableCell(Paragraph(f"${(sub_total * 0.05):.2f}", horizontal_alignment=Alignment.RIGHT),  col_span=1))

        # Total
        item_table.add(TableCell(Paragraph("Total", horizontal_alignment=Alignment.RIGHT),  col_span=3))
        item_table.add(TableCell(Paragraph(f"${ ((sub_total * 0.05) + sub_total):.2f}", horizontal_alignment=Alignment.RIGHT),  col_span=1))


        item_table.set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(4), Decimal(2))  
        item_table.no_borders() 

        return item_table






# Helper to laod in the arguments from the command line
def _load_arguments() -> ArgumentParser:
    parser = ArgumentParser(prog=__name__, description="Generates a PDF Invoice")

    # Possible arguments
    parser.add_argument('-c', '--client') 
    parser.add_argument('-h', '--hours') 
    parser.add_argument('-s', '--start') 
    parser.add_argument('-e', '--end') 




if __name__ == "__main__":

    # Test data to fill into the invoice.
    test_items = [BillableItem("Engineering Hours", 40, 60), BillableItem("Consulting fees", 12,120)]
    test_company = Company("XYZ Inc.", "123 Main St, Victoria, BC, Canada", "1-234-567-8910", "billing@xyz.ca", "www.xyz.ca")
    test_client = Client("ABC Inc.", "321 Secondary St, Victoria, BC, Canada", "1-234-567-8911", "billing@abc.ca", "www.abc.ca")

    document = InvoiceGenerator(test_company, test_client)

    document.add_image("https://www.ajb-tech.ca/assets/photos/AJB-Tech-Logo-borders-transparent.png")

    document.add_table(document.build_header())
    document.add_blank_line()
    document.add_table(document.build_billing_shipping())
    document.add_blank_line()
    document.add_table(document.build_items(test_items))

    document.generate("output.pdf")





    