from dataclasses import dataclass


'''
Class to define the parameters of the company creating the invoice.
'''
@dataclass
class Company:
    name:str
    address:str
    phone:str
    email:str
    website:str
    gst_num:str