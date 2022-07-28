from borb.pdf.document.document import Document
from borb.pdf.page.page import Page
from borb.pdf.canvas.layout.page_layout.multi_column_layout import SingleColumnLayout
from decimal import Decimal
from borb.pdf.canvas.layout.image.image import Image
from borb.pdf.pdf import PDF

# Create document
pdf = Document()

# Add page
page = Page()
pdf.add_page(page)

page_layout = SingleColumnLayout(page, vertical_margin = (page.get_page_info().get_height() * Decimal(0.02)) )

page_layout.add(    
        Image(        
        "https://s3.stackabuse.com/media/articles/creating-an-invoice-in-python-with-ptext-1.png",        
        width=Decimal(128),        
        height=Decimal(128),    
        ))


with open("output.pdf", "wb") as pdf_file_handle:
    PDF.dumps(pdf_file_handle, pdf)