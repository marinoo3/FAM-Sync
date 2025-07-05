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


    root_url = "https://clickandboat.com/account"


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
        section = soup.select_one('section#bookings')
        table = section.select_one('.in_progress.booking-table')

        events = []

        for row in table.select('.booking-row'):

            booking_status = row.select_one('.cell-status span.status')['data-state']
            booking_status = booking_status.lower()
            print(booking_status)

            booking_id = row.select_one('.cell-id').getText(strip=True)
            booking_id = booking_id.replace('N°', '')

            booking_client = row.select_one('.cell-other-account').getText(strip=True)

            booking_price = row.select_one('.cell-price').getText(strip=True)
            booking_price = booking_price.strip().replace('€', '')

            _date = row.select_one('.cell-details .date').getText()
            start_date, end_date = self.__extract_dates(_date)

            if start_date.date() >= date.today() and booking_status == 'accepted':
                # only append to the list if the booking isn't done already
                e = Event(booking_client, start_date, end_date, booking_price, 'Click&Boat')
                events.append(e)

        return events


    def get_csv_bookings(self, cookies:dict = None) -> pd.DataFrame:
        
        download_url = self.root_url + '/bookings/download'
        response = self.__safe_requests(download_url, cookies=cookies)
        csv_bytes = response.content
        return pd.read_csv(io.BytesIO(csv_bytes))


    def get_bookings(self, cookies:dict = None) -> list[Event]:

        bookings_url = self.root_url + '/bookings'
        response = self.__safe_requests(bookings_url, cookies=cookies)

        bookings = self.__parse_bookings(response.text)

        return bookings