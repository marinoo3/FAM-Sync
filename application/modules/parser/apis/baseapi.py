from abc import ABC, abstractmethod
import pickle
import os





class BaseApi(ABC):

    cookies_dir = "cookies"
    cookie_file: str

    def _format_cookies(self, cookies) -> dict:

        """
        format cookies to dict
        """

        formated_cookies = {}
        for c in cookies:
            formated_cookies[c['name']] = c['value']

        return formated_cookies
    

    def _load_cookies(self) -> dict:

        """
        Load session cookies from file and return as dict
        """

        if not os.path.exists(os.path.join(self.cookies_dir, self.cookie_file)):
            print(f'WARNING: cookies file "{self.cookie_file}" not found')
            return None
                
        try:
            with open(os.path.join(self.cookies_dir, self.cookie_file), "rb") as fh:
                cookies = pickle.load(fh)
        except Exception as exc:
            print(f"Cannot write cookie file {self.cookie_file}: {exc}")

        return cookies


    def _save_cookies(self, cookies) -> None:
        
        """
        Save cookies to json file
        """

        if not self.cookie_file:
            print('No "cookie_file" initialized, impossible to save the cookies')
        
        try:
            with open(os.path.join(self.cookies_dir, self.cookie_file), "wb") as fh:
                pickle.dump(cookies, fh)
        except Exception as exc:
            print(f"Cannot write cookie file {self.cookie_file}: {exc}")


    @abstractmethod
    def get_bookings(self, cookies:dict = None):
        pass