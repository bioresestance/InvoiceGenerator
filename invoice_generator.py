# Borb imports
from xmlrpc.client import DateTime
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
from datetime import datetime, timedelta
from dataclasses import dataclass
from typing import List

# Settings related imports
from confuse import Configuration
from argparse import ArgumentParser

# local module imports
from billable_item import BillableItem
from client import Client, ClientInfo
from company import Company




TOP_ROW_TABLE_COLOR = HexColor("263238")
ODD_ROW_TABLE_COLOR = HexColor("BBBBBB") 
EVEN_ROW_TABLE_COLOR = HexColor("FFFFFF") 



'''
Class that generates a PDF invoice from provided data.
'''
class InvoiceGenerator():

    def __init__(self, 
        company:Company, 
        client:Client, 
        invoice_number:int = 1, 
        invoice_date:DateTime = datetime.now(), 
        invoice_due_period=7, 
        tax_rate_percent=5
    ):

        # Save parameters
        self.company = company
        self.client = client
        self.invoice_number = invoice_number
        self.invoice_date = invoice_date
        self.invoice_due_date:datetime = self.invoice_date + timedelta(days=invoice_due_period)
        self.tax_rate = tax_rate_percent

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
        header.add(Paragraph(f"{self.invoice_date:%d-%m-%Y}"))
        
        header.add(Paragraph(f"{self.company.address}"))    
        header.add(Paragraph("Invoice #:", font="Helvetica-Bold", horizontal_alignment=Alignment.RIGHT))
        header.add(Paragraph(f"{self.invoice_number}"))   
        
        header.add(Paragraph(f"{self.company.phone}"))    
        header.add(Paragraph("Due Date:", font="Helvetica-Bold", horizontal_alignment=Alignment.RIGHT))
        header.add(Paragraph(f"{self.invoice_due_date:%d-%m-%Y}")) 
        
        header.add(Paragraph(f"{self.company.email}"))    
        header.add(Paragraph(" "))
        header.add(Paragraph(" "))

        header.add(Paragraph(f"{self.company.website}"))
        header.add(Paragraph(" "))
        header.add(Paragraph(" "))

        header.set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2), Decimal(2))    		
        header.no_borders()
        return header



    # Builds the table containing the client shipping and billing information
    def build_billing_shipping(self):
        info = Table(number_of_rows=6, number_of_columns=2)  
        # Headers
        info.add( Paragraph( "BILL TO", background_color=TOP_ROW_TABLE_COLOR, font_color=X11Color("White")))    
        info.add( Paragraph( "SHIP TO", background_color=TOP_ROW_TABLE_COLOR, font_color=X11Color("White")))  

        # Recipient Name
        info.add(Paragraph(f"{self.client.billing_info.recipient}"))              # BILLING  
        info.add(Paragraph(f"{self.client.shipping_info.recipient}"))             # SHIPPING 

        # Company Name 
        info.add(Paragraph(f"{self.client.billing_info.company_name}"))           # BILLING  
        info.add(Paragraph(f"{self.client.shipping_info.company_name}"))          # SHIPPING  

        # Street Address
        info.add(Paragraph(f"{self.client.billing_info.street_address}"))         # BILLING  
        info.add(Paragraph(f"{self.client.shipping_info.street_address}"))        # SHIPPING  

        # Rest of the adress
        info.add(Paragraph(f"{self.client.billing_info.city_province_areacode}")) # BILLING  
        info.add(Paragraph(f"{self.client.shipping_info.city_province_areacode}"))# SHIPPING 

        # Phone number 
        info.add(Paragraph(f"{self.client.billing_info.phone}"))                  # BILLING  
        info.add(Paragraph(f"{self.client.shipping_info.phone}"))                 # SHIPPING  

        # Formating
        info.set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(4), Decimal(2))  
        info.no_borders()  
        return info



    # Builds the table of billable items.
    def build_items(self, items_to_bill: List[BillableItem]):
        
        sub_total = 0.0
        tax_amount = 0.0
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
        tax_amount = (sub_total * (self.tax_rate / 100))
        item_table.add(TableCell(Paragraph(f"GST ({self.tax_rate}%)", horizontal_alignment=Alignment.RIGHT),  col_span=3))
        item_table.add(TableCell(Paragraph(f"${(tax_amount):.2f}", horizontal_alignment=Alignment.RIGHT),  col_span=1))

        # Total
        item_table.add(TableCell(Paragraph("Total", horizontal_alignment=Alignment.RIGHT),  col_span=3))
        item_table.add(TableCell(Paragraph(f"${ (tax_amount + sub_total):.2f}", horizontal_alignment=Alignment.RIGHT),  col_span=1))


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
    test_client_info = ClientInfo("Bob Smith", "ABC Inc.", "321 Secondary St", "Victoria, BC, V4G 3D6, Canada", "1-234-567-8911")


    document = InvoiceGenerator(test_company, Client(test_client_info, test_client_info), tax_rate_percent=12)

    document.add_image("https://www.ajb-tech.ca/assets/photos/AJB-Tech-Logo-borders-transparent.png")

    document.add_table(document.build_header())
    document.add_blank_line()
    document.add_table(document.build_billing_shipping())
    document.add_blank_line()
    document.add_table(document.build_items(test_items))

    document.generate("output.pdf")





    