

from nara.extra import async_CurrentDateTime
import asyncio
async def main():
    # Example 1: Fetch only the current time as a string
    current_time = await async_CurrentDateTime(current_timestamp=True, Country='unitedstates')
    print(f"Current Time (string): {current_time}")

    # Example 2: Fetch only the current date as a string
    current_date = await async_CurrentDateTime(Current_Date=True, Country='India')
    print(f"Current Date (string): {current_date}")

    # Example 3: Fetch both current time and date as strings
    current_time, current_date = await async_CurrentDateTime(current_timestamp=True, Current_Date=True, Country='Japan')
    print(f"Current Time (string): {current_time}")
    print(f"Current Date (string): {current_date}")

    # Example 4: Fetch only the current time as a datetime object
    current_time = await async_CurrentDateTime(current_timestamp=True, encode=True, Country='India')
    print(f"Current Time (datetime): {current_time}")

    # Example 5: Fetch only the current date as a datetime object
    current_date = await async_CurrentDateTime(Current_Date=True, encode=True, Country='India')
    print(f"Current Date (datetime): {current_date}")

    # Example 6: Fetch both current time and date as datetime objects
    current_time, current_date = await async_CurrentDateTime(current_timestamp=True, Current_Date=True, encode=True, Country='India')
    print(f"Current Time (datetime): {current_time}")
    print(f"Current Date (datetime): {current_date}")

# Run the async main function
asyncio.run(main())

