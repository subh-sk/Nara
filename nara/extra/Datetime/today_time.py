from datetime import datetime
from typing import Union

import requests


class CurrentDateTime:
    """
    A class to retrieve current date, time, and country codes from a remote API.

    Methods
    -------
    country_codes() -> dict:
        Retrieve a dictionary of country codes from a remote API endpoint.

    time(country_code: str, encode: bool = False) -> Union[dict, dict[str, datetime]]:
        Retrieve current time information for a specified country code.

    date(country_code: str, encode: bool = False) -> Union[str, datetime]:
        Retrieve current date information for a specified country code.
    """
    def country_codes()->dict:
        """
        Retrieve a dictionary of country codes from a remote API endpoint.

        Returns
        -------
        dict
            A dictionary where keys are country names and values are their corresponding codes.
        """
        headers= {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
        }
        html_response = requests.get(f"https://time-epbx.onrender.com/", headers=headers)
        return html_response.json().get("country_codes")
        
    def time(country_code:str,encode=False) -> dict|datetime:
        """
        Retrieve current time information for a specified country code.

        Parameters
        ----------
        country_code : str
            The country code for which time information is requested.
        encode : bool, optional
            Whether to return encoded datetime objects (`True`) or time strings (`False`). Default is `False`.

        Returns
        -------
        Union[dict, dict[str, datetime]]
            If `encode` is `True`, returns a dictionary with 12-hour and 24-hour time as `datetime` objects.
            If `encode` is `False`, returns a dictionary with 12-hour and 24-hour time as strings.

        Notes
        -----
        This function sends a GET request to an external API endpoint to fetch current time information
        for the specified country code. It expects the endpoint to return JSON with time data.

        Example
        -------
        >>> CurrentDateTime.time("IN")
        {'12_hour': '09:30:00 PM', '24_hour': '21:30:00'}
        >>> CurrentDateTime.time("IN", encode=True)
        {'12_hour': datetime.datetime(2024, 7, 8, 21, 30), '24_hour': datetime.datetime(2024, 7, 8, 21, 30)}
        """
        headers= {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    }

        # Define the format of the input strings
        time_12_hour_format = r'%I:%M:%S %p'
        time_24_hour_format = r'%H:%M:%S'
        html_response = requests.get(f"https://time-epbx.onrender.com/?country={country_code}", headers=headers)
        if html_response.status_code!=200:return html_response.json()
        elif html_response.status_code == 200:
            html_response:dict = html_response.json()
            if html_response.get("error") is None:
                time_12_hour = ' '.join(html_response.get("time").get("12_hour").split()[:2])
                time_24_hour = ' '.join(html_response.get("time").get("24_hour").split()[:1])
                if encode:
                    print(f"{time_24_hour = },{time_12_hour = }")
                    time_12_hour_obj = datetime.strptime(time_12_hour, time_12_hour_format)
                    time_24_hour_obj = datetime.strptime(time_24_hour, time_24_hour_format)
                    return {"12_hour": time_12_hour_obj, "24_hour": time_24_hour_obj}
                else:
                    return {"12_hour":time_12_hour,"24_hour":time_24_hour}
            else:
                return html_response.get("error")
    def date(country_code:str,encode=False) -> Union[str, datetime]:
        """
        Retrieve current date information for a specified country code.

        Parameters
        ----------
        country_code : str
            The country code for which date information is requested.
        encode : bool, optional
            Whether to return the date as a `datetime` object (`True`) or as a string (`False`). Default is `False`.

        Returns
        -------
        Union[str, datetime]
            If `encode` is `True`, returns the date as a `datetime` object.
            If `encode` is `False`, returns the date as a string.

        Notes
        -----
        This function sends a GET request to an external API endpoint to fetch current date information
        for the specified country code. It expects the endpoint to return JSON with date data.

        Example
        -------
        >>> CurrentDateTime.date("IN")
        '2024-07-08'
        >>> CurrentDateTime.date("IN", encode=True)
        datetime.datetime(2024, 7, 8, 0, 0)
        """
        headers= {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    }

        # Define the format of the input strings
        html_response = requests.get(f"https://time-epbx.onrender.com/?country={country_code}", headers=headers)
        if html_response.status_code!=200:return html_response.json()
        elif html_response.status_code == 200:
            html_response:dict = html_response.json()
            if html_response.get("error") is None:
                if encode:                    
                    return datetime.strptime(html_response.get("date"), "%Y-%m-%d")
                else:
                    return html_response.get("date")
            else:
                return html_response.get("error")

if __name__ == "__main__":
    datetime_obj = CurrentDateTime
    print(datetime_obj.time("in"))
    print(datetime_obj.time("in",encode=True))
    print(datetime_obj.date("in",encode=True))
    print(datetime_obj.date("in"))
    print(datetime_obj.country_codes())