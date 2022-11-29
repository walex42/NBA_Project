import pandas as pd

import census.client as client


def test_base_url():
    expected_url = "https://api.census.gov/data/2019/pep/charagegroups"
    actual_url = client.endpoint(
        year=2019,
        dataset_name="pep/charagegroups",
    )
    assert actual_url == expected_url


def test_variables():
    expected_value = "NAME,POP"
    actual_value = client.variables(["NAME", "POP"])
    assert expected_value == actual_value


def test_variable_predicates():
    expected_key_value_pair = {"HISP": [1, 2]}
    actual_key_value_pair = client.convert_values(
        {"HISP": ["Non-Hispanic", "Hispanic"]}
    )
    assert expected_key_value_pair == actual_key_value_pair


def test_states_abbr():
    expected_states_predicate = "29,30"
    actual_states_predicate = client.geographies(states=["MO", "MT"])
    assert expected_states_predicate == actual_states_predicate


def test_county_fips():
    expected_first_row = pd.Series(["MO", "29", "001", "Adair County", "H1"], name=0)
    actual_first_row = client.county_codes("MO").iloc[0]
    pd.testing.assert_series_equal(expected_first_row, actual_first_row)


def test_api_call():
    expected = pd.DataFrame(
        [
            ["St. Charles County, Missouri", "13754", "2", "29", "183"],
            ["St. Louis city, Missouri", "12543", "2", "29", "510"],
        ],
        columns=["NAME", "POP", "HISP", "state", "county"],
    )
    actual = client.get(
        year=2019,
        dataset="pep/charagegroups",
        get=["NAME", "POP"],
        vars={"HISP": ["Hispanic"]},
        geos={"MO": ["St. Louis city", "St. Charles County"]},
    )

    pd.testing.assert_frame_equal(actual, expected)
