from dataclasses import dataclass


'''
Class to define the parameters of the client being billed.
'''
@dataclass()
class Client:
    name:str
    address:str
    phone:str
    email:str
    website:str