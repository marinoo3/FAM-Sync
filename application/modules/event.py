from datetime import datetime




class Event:

    def __init__(self, client:str, start_date:datetime, end_date:datetime, ca:float, boat:str, source:str):
        
        self.client = client
        self.start_date = start_date
        self.end_date = end_date
        self.ca = ca
        self.boat = boat
        self.source = source