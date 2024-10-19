* **JSON Manipulation:**
    * **`loadJson(FileName="Json.json", PickRandom=None)`:** Loads JSON data from a file.  If `PickRandom` is an integer, it returns a dictionary or list containing that many randomly selected items from the JSON data.
        ```python
        from nara.extra.extended_json import loadJson

        data = loadJson("data.json")  # Load all data
        random_data = loadJson("data.json", PickRandom=2)  # Load 2 random items
        ```
        **Error Handling:** Raises `FileNotFoundError` if the file doesn't exist and `ValueError` for invalid JSON or if `PickRandom` exceeds the data length.

    * **`jsonList(FileName="JsonList.json", **kwargs)`:**  Appends key-value pairs (provided as keyword arguments) as a new dictionary entry to a JSON list. Creates a new list if the file doesn't exist or handles invalid data.
        ```python
        from nara.extra.extended_json import jsonList

        jsonList(FileName="my_list.json", name="Alice", age=30)
        jsonList(FileName="my_list.json", name="Bob", age=25)
        ```
        **Error Handling:** Displays warnings for non-existent files, empty files, or files not containing a list. Raises `ValueError` if the JSON file is empty or does not contain a list.

    * **`jsonDict(Key, Value, FileName="JsonDict.json")`:** Updates or adds a single `Key`-`Value` pair to a JSON dictionary stored in a file. Creates a new dictionary if the file doesn't exist.
        ```python
        from nara.extra.extended_json import jsonDict

        jsonDict("name", "Charlie", FileName="my_dict.json")
        jsonDict("age", 35, FileName="my_dict.json")
        ```
        **Error Handling:**  Displays warnings for similar file errors as `jsonList`.  Raises `ValueError` if the JSON file is empty or does not contain a dictionary.


* **Asynchronous Task Handling:**
    * **`asyncThreadedTask(thread_count=1, *threading_args, **threading_kwargs)`:** Executes an asynchronous function in a separate thread. Useful for running async operations within synchronous code or managing blocking I/O. This example demonstrates the usage with and without parameters:
    ```python
    import asyncio
    from nara import asyncThreadedTask
    
    @asyncThreadedTask
    async def async_function():
        print("Async function started")
        await asyncio.sleep(2)  # Simulate some async operation
        print("Async function finished")

    @asyncThreadedTask(2) # Use two threads
    async def async_function_2():
        print("Async function 2 started")
        await asyncio.sleep(2)
        print("Async function 2 finished")


    async def main():
        await async_function()
        await async_function_2()


    asyncio.run(main())
    ```


    * **`runMultipleTimes(count=1)`:** Runs an asynchronous function multiple times concurrently using `asyncio.gather`.
        ```python
        import asyncio
        from nara.extra.tools import runMultipleTimes
    
        @runMultipleTimes(5)  # Run the function 5 times concurrently
        async def my_async_task():
            print("Task started")
            await asyncio.sleep(1)
            print("Task finished")
    
        asyncio.run(my_async_task())
        ```


* **Structured Threading:**
    * **`retry(retries=3, delay=1)`:**  This decorator retries a function call if it raises an exception. It will retry up to `retries` times, pausing for `delay` seconds between attempts.
        ```python
        from nara.extra.tools import retry
        import random

        @retry(retries=5, delay=2)
        def might_fail():
            if random.random() < 0.5:
                raise Exception("Function failed!")
            print("Function succeeded!")
        
        might_fail()
        ```
    * **`repeatForever(sleep_interval=None, end_after=None)`:**  Executes a function or coroutine repeatedly.  `sleep_interval` specifies the pause between calls. `end_after` (a human-readable time string, e.g., "10 minutes") allows setting a time limit.
        ```python
        from nara.extra.tools import repeatForever
        import asyncio
        import time

        @repeatForever(sleep_interval=1, end_after="5 seconds")  # Repeat every second for 5 seconds
        def print_hello():
            print("Hello")

        @repeatForever(sleep_interval=1, end_after="5 seconds")
        async def async_print_hello():
            print("Async Hello")
            await asyncio.sleep(0.5) # Simulate some work
        

        print_hello() # Normal function example

        async def main(): # Asyncio function example
            await async_print_hello()

        asyncio.run(main())

        ```
        **Error Handling:** `repeatForever` raises `humanfriendly.InvalidTimespan` if `end_after` is not a valid timespan string.


* **File Management:**
    * **`clearPycacheDirectories(directory, display_status=False)`:** Recursively deletes all `__pycache__` directories within the given `directory`. Set `display_status=True` to print which directories were removed.
        ```python
        from nara.extra.file_manager import clearPycacheDirectories

        clearPycacheDirectories(".", display_status=True)  # Clear __pycache__ in the current directory and subdirectories
        ```

    * **`displayFileStructure(directory=os.getcwd(), tree=None, console=None)`:**  Prints a tree-like representation of the directory structure to the console.
        ```python
        from nara.extra.file_manager import displayFileStructure
        
        displayFileStructure(".")  # Display the file structure of the current directory
        ```

* **Date and Time Utilities:**
    * **`CurrentDateTime`:**  Retrieve current date and time information for various countries using external API.  Uses [this API](https://time-epbx.onrender.com/).
        ```python
        from nara.extra.date_time import CurrentDateTime

        dt = CurrentDateTime()
        country_codes = dt.countryCodes()  # Get available country codes
        indian_time = dt.time("IN", encode=True)  # Get current Indian time as datetime object
        us_date = dt.date("US") # Get current US date as string
        print(f"Country Codes: {country_codes}")
        print(f"Indian Time: {indian_time}")
        print(f"US Date: {us_date}")


        ```


* **Testing Tools:**
    * **`saveTestResults(OutputFile, **outerkwargs)`:**  This decorator saves test results to a JSON file. `outerkwargs` can include functions to calculate additional metrics (like mean or max) based on the test result.
        ```python
        from nara.extra.extended_json.testing_tools import saveTestResults

        @saveTestResults("results.json", mean=lambda x: sum(x)/len(x), maximum=max)
        def test_function(a, b):
            return [a + b, a * b]

        test_function(2, 3)  # Save results and calculated metrics to results.json
        ```

    * **`LoadTestResults(inputFile)`:**  Loads and returns the test results saved by `saveTestResults`.
        ```python
        from nara.extra.extended_json.testing_tools import LoadTestResults

        results = LoadTestResults("results.json")
        print(results)
        ```

* **SQL Utilities:** (Examples use a database file named `mydatabase.db`)
    * **`SqlQueue(db_file)`:**  Implements a queue using a SQLite database, enabling persistent queueing even if your application restarts.
        ```python
        from nara.extra.extended_sql import SqlQueue
        
        q = SqlQueue("mydatabase.db")
        q.put(10)
        q.put("Hello")
        
        retrieved_item = q.get() # Returns 10 (FIFO)
        print(retrieved_item)
        ```

    * **`TextStore(dbName)`:** Stores and manages text lines in a SQLite database, providing methods for adding, updating, deleting, and retrieving text lines by ID or slices. 
        ```python
        from nara.extra.extended_sql import TextStore
        
        ts = TextStore("mydatabase.db")
        ts.addRecord("This is a test line.")
        ts.addRecord("Another line of text.")
        
        all_records = ts.listRecords() # Retrieve all records
        print(all_records)
        ```

    * **`SqlList(DbName, TableName)`:** Enables you to use a SQLite table as if it were a Python list. You can append, access by index, slice, extend, pop, remove, and perform other list-like operations. Elements are stored as JSON strings.

        ```python
        from nara.extra.extended_sql import SqlList

        sl = SqlList("mydatabase.db", "my_list_table")
        sl.append({"name": "Alice", "age": 30})
        sl.append({"name": "Bob", "age": 25})
        
        print(sl[0])  # Access by index (returns a dictionary)
        print(len(sl)) # Get the length of the SqlList
        ```

    * **`SQLiteDict(db_name)`:** Uses a SQLite database as a persistent dictionary. Supports dictionary operations like setting, getting, deleting items, checking membership (`in`), and iterating through keys or items. Stores all data types as strings.
        ```python
        from nara.extra.extended_sql import SQLiteDict

        sd = SQLiteDict("mydatabase.db")
        sd['name'] = "Charlie"
        sd['age'] = 35
        
        print(sd['name'])  # Access by key
        print("name" in sd) # Check for key existence
        ```
        **Error Handling:** The `get` method will return `None` if the requested key is not found and the data in the "value" column cannot be evaluated as valid Python code, the SQLiteDict's `get` method will return `None`, instead of raising an exception. It will also print an error message indicating the failure to evaluate the value.


* **Time Utilities:**
    * **`timeIt(func)`:** A decorator to measure and print the execution time of a function (both synchronous and asynchronous).

        ```python
        import asyncio
        from nara.extra.tools import timeIt
        import time

        @timeIt
        def my_function():
            time.sleep(1) # Simulate a second of work

        @timeIt
        async def my_async_function():
            await asyncio.sleep(1)

        my_function()
        asyncio.run(my_async_function())

        ```


