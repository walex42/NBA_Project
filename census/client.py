from typing import List

import pandas as pd
import us

def endpoint(
    year: int,
    dataset_name: str,
) -> str:
    """Returns the Census API endpoint URL for a given year and dataset.

    Args:
        year: The year of the dataset.
        dataset_name: The name of the dataset.

    Returns:
        str: The Census API endpoint URL for the given dataset.
    """
    base = "https://api.census.gov/data"
    end = base + "/" + str(year) + "/" + dataset_name
    return end


def variables(variables: list[str]) -> str:
    """Converts a list of variables into a comma-separated string of variables
    that can be passed to the Census API.

    Args:
        variables: A list of variables.

    Returns:
        str: A comma-separated string of variables that can be passed to the
            Census API.
    """
    list = variables
    commaList = ",".join(list)
    return commaList


def convert_values(variable_values: dict[str, List[str]]) -> dict[str, List[int]]:
    """Converts human-readable variable values into IDs which can be passed to
    the Census API. Values are mapped to their variables in dictionaries.

    Args:
        variable_values: A dictionary that maps a variable to a list of the user's
        desired values to send to the API.

    Returns:
        A dictionary of the same values represented by appropriate IDs
    """
    variable_int = {}
    for key in variable_values:
        values = variable_values[key]
        i = 0
        for value in values:
            if (value == "Both Sexes" or value == "Both Hispanic Origins"):
                values[i] = str(0)
            if (value == "Male" or value == "Non-Hispanic"):
                values[i] = str(1)
            if (value == "Female" or value == "Hispanic"):
                values[i] = str(2)
            i += 1
        int_values = list(map(int, values))
        variable_int[key] = int_values
    return variable_int
            


def geographies(states: List[str] = [], counties: List[str] = []) -> str:
    """Converts a list of state abbreviations to a comma-separated
    list of FIPS codes that can be passed to the Census API.

    """
    converted = []
    for state in states:
        cur = us.states.lookup(state)
        converted.append(str(cur.fips))
    converted_list = ",".join(converted)
    return converted_list


def county_codes(state_abbr: str) -> pd.DataFrame:
    """Gets a dataframe of county code info for a given state abbreviation"""
    pass


def get(
    year: int,
    dataset: str,
    get: list[str],
    vars: dict[str, List[str]] = {},
    geos: dict[str, List[str]] = {},
) -> pd.DataFrame:
    """Returns a Pandas DataFrame of data from the Census API.

    Args:
        year: The year of the dataset.
        dataset: The name of the dataset.
        get: A list of variables to pass to the 'get' query parameter.
        vars: A mapping of variables to human-readable values.
        geos: A dictionary of counties to include with states as keys
    Returns:
        pd.DataFrame: A Pandas DataFrame of data from the Census API.
    """
    pass


def verify_data() -> None:
    pass
