from dataclasses import dataclass


'''
Class that defines the information about a company
'''
@dataclass
class ClientInfo():
    recipient:str
    company_name:str
    street_address:str
    city_province_areacode:str
    phone:str



'''
Class to define the parameters of the client, including their billing and shipping information.
'''
@dataclass
class Client():
    billing_info: ClientInfo
    shipping_info: ClientInfo