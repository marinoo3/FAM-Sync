from ..event import Event

import os
from datetime import datetime, timedelta
import time
import requests
import json





class NotionCalendar:

    base_url = "https://api.notion.com/v1"
    bookings: list[Event] = []


    def __init__(self):
        self.headers = {
            'Authorization': f"Bearer {os.environ['NOTION_KEY']}",
            'Content-Type': 'application/json',
            'Notion-Version': '2022-06-28'
        }


    def __safe_requests(self, url, headers: dict = None, data: dict = None, tic=0):
        
        try:
            response = requests.post(url, headers=headers, data=data)
        except ConnectionError:
            if tic < 3:
                time.sleep(2)
                response = self.__safe_requests(url, headers=headers, data=data, tic=tic+1)
            else:
                print('Connection Error: Failed to requests Notion API')
                response = None

        return response
    

    def __within_one_hour(self, date1:datetime, date2:datetime) -> bool:
        one_hour = timedelta(hours=1)
        return abs(date1 - date2) <= one_hour


    def load_calendar(self, db_id:str) -> dict:

        today_str = datetime.now().strftime('%Y-%m-%d')

        data = {
            "filter": {
                "or": [{
                    "property": "Date",
                    "date": {
                        "on_or_after": today_str
                    }
                }]
            }
        }

        db_api_url = self.base_url + '/databases/' + db_id + '/query'

        response = self.__safe_requests(db_api_url, headers=self.headers, data=json.dumps(data))
        content = response.json()

        for event in content['results']:

            client = event['properties']['Client']['title'][0]['plain_text']
            ca = event['properties']['CA Net']['number']
            source = event['properties']['Source']['rich_text']
            boat = event['properties']['Bateau']['select']['name']
            _date = event['properties']['Date']['date']
            start_date = datetime.fromisoformat(_date['start'])
            end_date = datetime.fromisoformat(_date['end'])

            self.bookings.append(Event(client, start_date, end_date, ca, boat, source))

        return response.json()


    def add_event(self, db_id:str, event:Event) -> dict:

        data = {
            'parent': {
                'database_id': db_id
            },
            'properties': {
                "Client": {
                    "title": [
                        {
                            "text": {
                                "content": event.client
                            }                        
                        }
                    ],
                },
                "CA Net": {
                    "number": float(event.ca)
                },
                "Source": {
                    "rich_text": [
                        {
                            "text": {
                                "content": event.source
                            }
                        }
                    ]
                },
                "Bateau": {
                    "select": {
                        "name": event.boat
                    }
                },
                "Date": {
                    "date": {
                        "start": event.start_date.isoformat(),
                        "end": event.end_date.isoformat()
                    }
                }
            }
        }

        pages_api_url = self.base_url + '/pages'

        response = self.__safe_requests(pages_api_url, headers=self.headers, data=json.dumps(data))        
        response.raise_for_status() # raises response status error
        print(f'{event.client} added to calendar on {event.start_date.date()}')

        return response.json()


    def match_event(self, event:Event) -> Event:
        
        for booking in self.bookings:

            same_start = self.__within_one_hour(booking.start_date, event.start_date)
            same_end = self.__within_one_hour(booking.end_date, event.end_date)

            if all([same_start, same_end]):
                return booking