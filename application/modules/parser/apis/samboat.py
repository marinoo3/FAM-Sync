# Base classes
from .baseapi import BaseApi
from ...event import Event

# Scarpping modules
import requests
from bs4 import BeautifulSoup

# Time modules
import time
import locale
from datetime import datetime, date
from zoneinfo import ZoneInfo

# Analytics modules
import re
import pandas as pd

# File and system modules
import io

        





class ClickAndBoat(BaseApi):


    root_url = "https://www.samboat.fr/private"


    def __safe_requests(self, url, tic=0, cookies:dict = None) -> requests.Response:

        try:
            response = requests.get(url, cookies=cookies)
        except ConnectionError:
            if tic < 3:
                time.sleep(2)
                response = self.__safe_requests(url, tic=tic+1, cookies=cookies)
            else:
                raise Exception(f'Connection Error: failed to requests "{url}"')
        
        if '?redirect' in response.url:
            print(f'    Failed to request "{url}" even after generating new cookie. Request got redirected')
            return None

        return response
    

    def __extract_dates(self, text: str) -> tuple[datetime, datetime]:

        locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')
        text = " ".join(text.split()) # squash spaces

        date_str, time_str = text.split('(')

        #  ➜ 24 juin 2025  (group 1)
        #  ➜ 10:00         (group 2)
        #  ➜ 18:00         (group 3)
        m = re.search(r'(\d{1,2}\s+\w+\s+\d{4})\s+de\s+(\d{1,2}:\d{2})\s+à\s+(\d{1,2}:\d{2})', 
                      text, re.I)
        
        if not m:
            raise ValueError(f"Aucune date lisible trouvée dans : {text!r}")
        
        date_part, start_time, end_time = m.groups()
        start_dt = datetime.strptime(f'{date_part} {start_time}', '%d %B %Y %H:%M').replace(tzinfo=ZoneInfo("Europe/Paris"))
        end_dt = datetime.strptime(f'{date_part} {end_time}',   '%d %B %Y %H:%M').replace(tzinfo=ZoneInfo("Europe/Paris"))

        return start_dt, end_dt
    

    def __parse_bookings(self, html) -> list[Event]:

        soup = BeautifulSoup(html, 'html.parser')
        section = soup.select_one('section#reservations-list')
        table = section.select_one('#confirmed')

        events = []

        for row in table.select('a.card'):

            row_data = {}

            profile_col = row.select_one('div.order-1')
            booking_client = profile_col.getText(strip=True)
            row_data['client'] = booking_client

            details_col = row.select_one('div.order-2')
            _date = details_col.select_one('.text-truncate').getText()
            start_date, end_date = self.__extract_dates(_date)
            row_data['start_date'] = start_date
            row_data['end_date'] = end_date

            price_col = row.select_one('div.order-3')
            booking_price = price_col.getText(strip=True).replace('€', '')
            row_data['price'] = float(booking_price)

            if start_date.date() >= date.today():
                # only append to the list if the booking isn't done already
                e = Event(booking_client, start_date, end_date, booking_price, 'SamBoat')
                events.append(e)

        return events


    def get_bookings(self, cookies:dict = None) -> list[Event]:

        bookings_url = self.root_url + '/reservations'
        response = self.__safe_requests(bookings_url, cookies=cookies)

        bookings = self.__parse_bookings(response.text)

        return bookings