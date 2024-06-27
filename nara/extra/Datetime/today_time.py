import asyncio
import re
import aiohttp
from bs4 import BeautifulSoup
from datetime import datetime,time

import requests

async def fetch_url(session, url):
    async with session.get(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"}) as response:
        if response.status == 200:return await response.text()
        else: return False
async def async_CurrentDateTime(current_timestamp=False,Current_Date=False,encode=False,Country='India')->str|datetime:
    url = f"https://time.is/{Country}"
    async with aiohttp.ClientSession() as session:
        html = await fetch_url(session, url)
        
        if not html:raise Exception("Invalid Country name or error while fetching time date")
        soup = BeautifulSoup(html, 'html.parser')

        if current_timestamp and Current_Date:
            try:
                clock_element = soup.find('time', id='clock')
                if clock_element:
                    time_obj = clock_element.text.strip()
                    if encode:
                        try:time_obj = datetime.strptime(time_obj, "%H:%M:%S").time()
                        except:
                            try:
                                time_obj = datetime.strptime(time_obj, "%I:%M:%S%p")
                            except:time_obj = datetime.strptime(time_obj,"%I:%M:%S %p")
                
                date_element = soup.find('div', class_='clockdate')
                if date_element:
                    date_info = date_element.text.strip()
                    
                    # Extract and format the date
                    date_parts = date_info.split(',')
                    current_date_obj = date_parts[1].strip() + ' ' + date_parts[2].strip()
                    # print("Formatted Date:", current_date_obj)
                    if encode:
                        try:
                            current_date_obj = datetime.strptime(current_date_obj, r'%B %d %Y').date()
                        except:
                            current_date_obj = datetime.strptime(current_date_obj, r'%d %B %Y').date()
                    
                    return time_obj, current_date_obj
            except:return None, None
        elif current_timestamp:
            # Extract the time
            clock_element = soup.find('time', id='clock')
            if clock_element:
                time_obj = clock_element.text.strip()
                if encode:
                    try:time_obj = datetime.strptime(time_obj, "%H:%M:%S").time()
                    except:
                        time_obj = re.sub(r"(\d{2}:\d{2}:\d{2})([APM]+)", r"\1 \2", time_obj)
                        
                        try:
                            time_obj = datetime.strptime(time_obj, "%I:%M:%S%p")
                        except:time_obj = datetime.strptime(time_obj,"%I:%M:%S %p")

                # print(time_obj)

                return time_obj
            else:
                return 

        ################### CURRENT DATE #####################
        elif Current_Date:        # Extract the date
            date_element = soup.find('div', class_='clockdate')
            if date_element:
                date_info = date_element.text.strip()
                
                # Extract and format the date
                date_parts = date_info.split(',')
                current_date_obj = date_parts[1].strip() + ' ' + date_parts[2].strip()
                # print("Formatted Date:", current_date_obj)
                if encode:
                    try:
                        current_date_obj = datetime.strptime(current_date_obj, r'%B %d %Y').date()
                    except:
                        current_date_obj = datetime.strptime(current_date_obj, r'%d %B %Y').date()

                return current_date_obj
            
            else:
                return None

def CurrentDateTime(current_timestamp=False,Current_Date=False,encode=False,Country='India')->str|datetime:
    headers= {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-language": "en-US,en;q=0.9",
    "cache-control": "max-age=0",
    "priority": "u=0, i",
    "sec-ch-ua": "\"Not/A)Brand\";v=\"8\", \"Chromium\";v=\"126\", \"Google Chrome\";v=\"126\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "none",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
  }
    html = requests.get(f"https://time.is/{Country}", headers=headers)
    if html.status_code!=200:raise Exception("Invalid Country name or error while fetching time date",html.status_code)
    elif html.status_code == 200:
        html = html.content
        soup = BeautifulSoup(html, 'html.parser')
        if current_timestamp and Current_Date:
            try:
                clock_element = soup.find('time', id='clock')
                if clock_element:
                    time_obj = clock_element.text.strip()
                    if encode:
                        try:time_obj = datetime.strptime(time_obj, "%H:%M:%S").time()
                        except:
                            try:
                                time_obj = datetime.strptime(time_obj, "%I:%M:%S%p")
                            except:time_obj = datetime.strptime(time_obj,"%I:%M:%S %p")
                
                date_element = soup.find('div', class_='clockdate')
                if date_element:
                    date_info = date_element.text.strip()
                    
                    # Extract and format the date
                    date_parts = date_info.split(',')
                    current_date_obj = date_parts[1].strip() + ' ' + date_parts[2].strip()
                    # print("Formatted Date:", current_date_obj)
                    if encode:
                        try:
                            current_date_obj = datetime.strptime(current_date_obj, r'%B %d %Y').date()
                        except:
                            current_date_obj = datetime.strptime(current_date_obj, r'%d %B %Y').date()
                    
                    return time_obj, current_date_obj
            except:return None, None
        elif current_timestamp:
            # Extract the time
            clock_element = soup.find('time', id='clock')
            if clock_element:
                time_obj = clock_element.text.strip()
                if encode:
                    try:time_obj = datetime.strptime(time_obj, "%H:%M:%S").time()
                    except:
                        time_obj = re.sub(r"(\d{2}:\d{2}:\d{2})([APM]+)", r"\1 \2", time_obj)
                        
                        try:
                            time_obj = datetime.strptime(time_obj, "%I:%M:%S%p")
                        except:time_obj = datetime.strptime(time_obj,"%I:%M:%S %p")

                # print(time_obj)

                return time_obj
            else:
                return 

        ################### CURRENT DATE #####################
        elif Current_Date:        # Extract the date
            date_element = soup.find('div', class_='clockdate')
            if date_element:
                date_info = date_element.text.strip()
                
                # Extract and format the date
                date_parts = date_info.split(',')
                current_date_obj = date_parts[1].strip() + ' ' + date_parts[2].strip()
                # print("Formatted Date:", current_date_obj)
                if encode:
                    try:
                        current_date_obj = datetime.strptime(current_date_obj, r'%B %d %Y').date()
                    except:
                        current_date_obj = datetime.strptime(current_date_obj, r'%d %B %Y').date()

                return current_date_obj
            
            else:
                return None
    
# Example usage
async def main():
    current_time,current_date = await async_CurrentDateTime(current_timestamp=True,Current_Date=True)
    print("current_time = ",current_time,type(current_date),"current_date = ",current_date,type(current_date))

if __name__ == "__main__":
    # Run the async function
    asyncio.run(main())
    a =CurrentDateTime(current_timestamp=True,encode=True)
    # a = datetime.strptime("00:01:12", "%H:%M:%S").time()
    print(a,type(a))
    if a and a.strftime("%p") == "AM" and (a.hour == 00 and a.minute in [0,1,2,3]):
        print(True)
    else:
        print(False)
