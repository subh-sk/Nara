from datetime import datetime
from typing import Union

import pycountry
import pytz
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
    @staticmethod
    def country_codes() -> dict:
        """
        Retrieve a dictionary of all country codes and their corresponding country names.

        Returns
        -------
        dict
            A dictionary where keys are country names and values are their corresponding codes.
        """
        # Initialize an empty dictionary to store country names and codes
        countries_dict = {}

        # Iterate over all countries in pycountry and populate the dictionary
        for country in pycountry.countries:
            countries_dict[country.name] = country.alpha_2

        return countries_dict

    @staticmethod
    def date_time(country_code: str, encode: bool = False) -> dict:
        """
        Retrieve current time information for a specified country code.

        Parameters
        ----------
        country_code : str
            The 2-letter country code for which time information is requested.
        encode : bool, optional
            Whether to return the times as datetime objects (`True`) or as strings (`False`). Default is `False`.

        Returns
        -------
        dict
            A dictionary containing country name, date, and time in both 12-hour and 24-hour formats.
            If `encode` is True, the times will be datetime objects. If `encode` is False, the times will be strings.

        Raises
        ------
        ValueError
            If the country code is invalid or not found.
        """
        try:
            # Validate and get the country name from the country code
            country = pycountry.countries.get(alpha_2=country_code.upper())
            if not country:
                raise ValueError(f"Invalid country code: {country_code}")

            # Get the first timezone for the country code
            tz = pytz.country_timezones[country_code.upper()][0]
            current_time = datetime.now(pytz.timezone(tz))

            # Prepare the response with country name and time details
            if encode:
                # Return datetime objects
                return {
                    'country': country.name,
                    'date': current_time.date(),
                    'time': {
                        '12_hour': current_time,  # 12-hour datetime object
                        '24_hour': current_time   # 24-hour datetime object
                    }
                }
            else:
                # Return formatted time strings
                return {
                    'country': country.name,
                    'date': current_time.strftime('%Y-%m-%d'),
                    'time': {
                        '12_hour': current_time.strftime('%I:%M:%S %p %Z %z'),  # 12-hour format string
                        '24_hour': current_time.strftime('%H:%M:%S %Z %z')      # 24-hour format string
                    }
                }

        except (KeyError, ValueError) as e:
            raise ValueError(f"Error: {str(e)}")
        
    

