from .apis.clickandboat import ClickAndBoat
from .apis.baseapi import BaseApi
from ..event import Event





class Parser():

    def __init__(self):
        self.platforms = {
            'clickandboat': ClickAndBoat(),
            'samboat': None
        }

    def get_bookings(self, platforms=['clickandboat', 'samboat'], cookies:dict = None) -> list[Event]:

        bookings = []

        for p in platforms:

            api: BaseApi = self.platforms[p]
            data = api.get_bookings(cookies)
            bookings.extend(data)

        return bookings

        