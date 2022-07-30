from dataclasses import dataclass

'''
Class to describe an item to bill for.
'''
@dataclass
class BillableItem():
    item_description:str
    item_quantity: float
    item_unit_price: float