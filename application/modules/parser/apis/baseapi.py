from abc import ABC, abstractmethod
import pickle
import os





class BaseApi(ABC):

    @abstractmethod
    def get_bookings(self, cookies:dict = None):
        pass