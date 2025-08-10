# data_fetch.py
import pandas as pd

import pandas as pd

def load_data():
    URL = "https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv"
    df = pd.read_csv(URL, parse_dates=['date'])
    return df

    
    # Keep only important columns
    cols = [
        'iso_code', 'location', 'date',
        'total_cases', 'new_cases',
        'total_deaths', 'new_deaths',
        'population'
    ]
    df = df[cols]
    
    # Fill missing values with 0 where needed
    df = df.fillna(0)
    
    # Calculate per million metrics
    df['cases_per_million'] = (df['total_cases'] / df['population']) * 1e6
    df['deaths_per_million'] = (df['total_deaths'] / df['population']) * 1e6
    
    return df
