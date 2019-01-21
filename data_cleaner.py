import numpy as np


def seconds_converter(time):
    '''Takes a time in the string form '00:00:00' and converts it into integer of seconds.
    Handles special '-' cases and converts them to NaNs'''

    if time == '-':
        return np.nan
    time_split = [int(x) for x in (time.split(':'))]
    return time_split[0] * (60 ** 2) + time_split[1] * 60 + time_split[2]


def clean_data(df):
    '''Takes in a DataFrame, drops unnecessary columns, and applies seconds_converter.'''

    df.drop(list(df.filter(regex='Unnamed')), axis=1, inplace=True)
    df.drop(['Citizen', 'Proj. Time'], axis=1, inplace=True)

    time_cols = ['5K', '10K', '15K', '20K', 'Half', '25K',
                 '30K', '35K', '40K', 'Pace', 'Official Time']

    for col in time_cols:
        df18[col] = df18[col].apply(seconds_converter)

    return df



