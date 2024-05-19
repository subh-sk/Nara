import json
import time
from functools import wraps
from typing import Any, Callable, Dict, List, Union
from rich import print as rprint

def SaveTestResults(OutputFile: str, **outerkwargs: Dict[str, Callable]) -> Callable:
    """
    Decorator function to save the results of a test function to a JSON file with additional data computed by specified functions.

    Parameters
    ----------
    OutputFile : str
        The name of the file to which the test results will be saved.
    **kwargs : Dict[str, Callable]
        Keyword arguments where the key is the name of the additional data and the value is a function to compute that data.
        The function should take the test result as input and return the computed data.

    Returns
    -------
    Callable
        A decorator function that can be used to decorate test functions.

    Examples
    --------
    @SaveTestResults("test_results.json", mean=lambda result: sum(result) / len(result), max_val=max)
    def test_function(numbers: List[int]) -> int:
        return sum(numbers)

    test_function([1, 2, 3, 4, 5])

    This will save the results of the 'test_function' to the file "test_results.json" after each execution,
    along with additional computed data such as mean and maximum value.
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            StartTime: float = time.time()
            result: Any = func(*args, **kwargs)
            EndTime: float = time.time()
            
            testResult: Dict[str, Union[str, Any, float]] = {
                "functionName": func.__name__,
                "args": args,
                "kwargs": kwargs,
                "result": result,
                "timeTaken": EndTime - StartTime
            }

            # Compute additional data using specified functions
            for key, value in outerkwargs.items():
                try:
                    # Check if result is iterable, if not, convert it to a single-element list
                    if not isinstance(result, (list, tuple)):
                        result = [result]
                    computed_value = value(result)
                    testResult[key] = computed_value
                except Exception as e:
                    rprint(f"[bold red]Error computing {key}:[/bold red] {str(e)}")

            try:
                with open(OutputFile, 'a') as f:
                    json.dump(testResult, f)
                    f.write('\n')
            except Exception as e:
                rprint("[bold red]Error saving test result:[/bold red] {}".format(str(e)))
                
            return result
        return wrapper
    return decorator

def LoadTestResults(inputFile: str) -> List[Dict[str, Union[str, Any, float]]]:
    """
    Load test results from a JSON file.

    Parameters
    ----------
    inputFile : str
        The name of the file containing the test results.

    Returns
    -------
    List[Dict[str, Union[str, Any, float]]]
        A list of dictionaries representing the test results.

    Examples
    --------
    test_results = LoadTestResults("test_results.json")
    for result in test_results:
        print(result)

    This will load test results from the file "test_results.json" and print each result.
    """
    try:
        with open(inputFile, 'r') as f:
            testResults: List[Dict[str, Union[str, Any, float]]] = [json.loads(line) for line in f]
        return testResults
    except Exception as e:
        rprint("[bold red]Error loading test results:[/bold red] {}".format(str(e)))
        return []


def TimeIt(func: Callable) -> Callable:
    """
    Decorator function to time the execution of a function.

    Parameters
    ----------
    func : Callable
        The function to be decorated.

    Returns
    -------
    Callable
        The decorated function with timing functionality.

    Examples
    --------
    @TimeIt
    def test_function(x: int, y: int) -> int:
        return x + y

    test_function(1, 2)

    This will time the execution of the 'test_function' function and print the result.
    """
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        StartTime: float = time.time()
        result: Any = func(*args, **kwargs)
        EndTime: float = time.time()

        rprint("[bold green]Time taken:[/bold green] {} seconds".format(EndTime - StartTime))
        return result
    return wrapper


if __name__ == "__main__":

    @SaveTestResults("test_results.json", mean=lambda result: sum(result) / len(result), max_val=max)
    def test_function(x: int, y: int) -> int:
        return x + y

    test_function(1, 2)

    LoadedResults = LoadTestResults("test_results.json")
    for result in LoadedResults:
        rprint("[bold green]Test Result:[/bold green] {}".format(result))

    @TimeIt
    def test_function(x: int, y: int) -> int:
        return x + y

    print(test_function(1, 2))