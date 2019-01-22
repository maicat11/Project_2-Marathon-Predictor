import numpy as np


def seconds_converter(time):
    '''Takes a time in the string form '00:00:00' and converts it into integer
    of seconds.  Handles special '-' cases and converts them to NaNs '''

    if time == '-':
        return np.nan

    time_split = [int(x) for x in (time.split(':'))]
    return time_split[0] * (60 ** 2) + time_split[1] * 60 + time_split[2]


def best_fit_slope(x, y):
    '''Calculate the best fit slope for all 5K splits.'''
    m = (((x.mean() * y.mean()) - (x * y).mean()) /
         (x.mean() ** 2 - (x ** 2).mean()))
    return round(m, 2)


def race_slope(row):
    '''Create a new column of the race progression slope.'''
    nK_splits = ['5K', '10K', '15K', '20K', '25K', '30K', '35K', '40K']
    x = np.array([5, 10, 15, 20, 25, 30, 35, 40])
    y = np.array([row['5K']] + list(np.diff(row[nK_splits])))

    return best_fit_slope(x, y)


def clean_data(df):
    '''Takes in a DataFrame, drops unnecessary columns, and applies seconds_converter. '''

    # drop unnecessary columns
    df.drop(list(df.filter(regex='Unnamed')), axis=1, inplace=True)
    df.drop(['Citizen', 'Proj. Time', 'City'], axis=1, inplace=True)

    # rename columns for clarity
    df18.rename(columns={'Overall': 'overall_rank', 'Gender': 'gender_rank',
                         'Division': 'division_rank', 'M/F': 'Gender'}, inplace=True)

    # convert the time to seconds on these columns
    time_cols = ['5K', '10K', '15K', '20K', 'Half', '25K',
                 '30K', '35K', '40K', 'Pace', 'Official Time']
    for col in time_cols:
        df18[col] = df18[col].apply(seconds_converter)

    # fill the State column with NaNs to 'none' instead so it can be
    # concatenated with the country column
    df18['State'].fillna('', inplace=True)
    df18['state_country'] = df18['State'] + '_' + df18['Country']

    # create a new column progression_slope
    df18['progression_slope'] = df18.apply(race_slope, axis=1)

    df.drop(['State', 'Country', '5K', '10K', '15K', '20K', '25K',
             '30K', '35K', '40K'], axis=1, inplace=True)

    return df


