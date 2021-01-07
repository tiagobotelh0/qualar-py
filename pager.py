import tabula
import numpy as np
import pandas as pd

def add_station(df, j):
    
    """
    Extracts the measurement station's name from the empty DataFrame that comes w/ each page...
    ... and adds a constant column.
    
    Inputs:
    
    df: a pandas DataFrame object.
    
    j: an integer.
    
    Output: a string. 
    """
    
    full_name = df[j].columns[0].split()[::-1]

    station_fuzzy = full_name[0:full_name.index('-')][::-1]

    station = ' '.join(station_fuzzy)
    
    df[j+1]['station'] = station
    
    return df[j+1]

def add_pollutant(df):
    
    """
    Extracts the pollutant's name (or rather, its acronym) and adds a constant column.
    
    Inputs:
    
    df: a pandas DataFrame object.
    
    Output: a string.
    """
    
    full_name = df.columns[0]
    
    pollutant_acronym = full_name.split()[0]
    
    df['pollutant'] = pollutant_acronym
    
    df.rename(columns={df.columns[0]: 'day'}, inplace=True)
    
    return df

def add_dates(df):
    
    """
    Extracts month/year dates and adds constant columns for posterior conversion.
    
    Inputs:
    
    df: a pandas DataFrame.
    
    Outputs: a pandas DataFrame object.
    """
    
    month_year = df.iat[0, 0].split()
    
    month, year = month_year[0], month_year[-1]
    
    df['month'], df['year'] = month, year
    
    df.replace({
        'Janeiro': '01',
        'Fevereiro': '02',
        'Março': '03',
        'Abril': '04',
        'Maio': '05',
        'Junho': '06',
        'Julho': '07',
        'Agosto': '08',
        'Setembro': '09',
        'Outubro': '10',
        'Novembro': '11',
        'Dezembro': '12'
      },regex=True, inplace=True)
    
    df.drop([0, 1], inplace=True)
    
    df['date'] = df['year'] + df['month'] + df['day']
    
    df['date'] =  pd.to_datetime(df['date'], format='%Y%m%d')
    
    return df

def typecast(df):
    
    """
    Typecasts variables, by which we mean:
    
    1. It substitutes '-' for NaN types;
    2. It typecasts numeric cells so as to make them correspond to their natural type.
    
    Inputs:
    
    df: a pandas DataFrame object.
    
    Outputs: a pandas DataFrame object.
    """
    
    #Operation 1: adequately label missing values as NaN.
    
    df.replace(to_replace='-', value=np.nan, inplace=True)

    df.replace(to_replace=',', value='.', regex=True, inplace=True)
    
    #Operation 2: typecast numeric types:
    
    i = 0
    
    while (i := i + 1) < len(df.columns) - 5:
        
        df = df.astype({df.columns[i]: 'float'})
    
    return df

def drop_bad_rows(df, k):
    
    """
    Drops rows with at least k missing hourly observations.
    
    Inputs:
    
    df: a pandas DataFrame object.
    
    k: an integer.
    
    Outputs: a pandas DataFrame object
    """
    
    df.reset_index(drop=True, inplace=True)

    df = df[df.isnull().sum(axis=1, numeric_only=True) < 12]
    
    return df

def final_adjustments(df):
    
    """
    Smoothing out the rough edges for the transformations in the next step.
    
    Inputs:
    
    df: a pandas DataFrame object.
    
    Outpus: a pandas DataFrame object.
    """
    
    df.drop(columns=['day', 'month', 'year'], inplace=True)
    
    df.set_index('date', inplace=True)

    s = df.pop('station')
    p = df.pop('pollutant')
    
    df.insert(0, 'station', s)
    
    df.insert(1, 'pollutant', p)

    df.columns = df.columns[:2].tolist() + ['h' + str(i) for i in range(len(df.columns)-2)]
    
    return df

def clean(df, j):

    df = add_station(df, j)
    df = add_pollutant(df)
    df = add_dates(df)
    df = typecast(df)
    df = drop_bad_rows(df, 12)
    df = final_adjustments(df)

    return df
