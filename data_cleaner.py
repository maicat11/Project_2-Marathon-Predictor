import numpy as np


def clean_bib(bib):
    '''Strip the bib number and make an int'''
    return int(bib.strip('F'))


def seconds_converter(time):
    '''Takes a time in the string form '00:00:00' and converts it into integer
    of seconds.  Handles special '-' cases and converts them to NaN '''

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


def add_weather_data(df, year):
    '''Add the weather data for the corresponding year.'''

    year = int(year)
    median = df['Official Time'].median() / 3600

    pre_median_2015 = {'temp': 48, 'dew_point': 39, 'humidity': 0.71, 'wind': 17, 'gusts': 26}
    post_median_2015 = {'temp': 44, 'dew_point': 41, 'humidity': 0.89, 'wind': 16, 'gusts': 0}
    pre_median_2016 = {'temp': 64, 'dew_point': 31, 'humidity': 0.29, 'wind': 14, 'gusts': 22}
    post_median_2016 = {'temp': 53, 'dew_point': 37, 'humidity': 0.55, 'wind': 14, 'gusts': 0}
    pre_median_2017 = {'temp': 74, 'dew_point': 40, 'humidity': 0.29, 'wind': 21, 'gusts': 29}
    post_median_2017 = {'temp': 73, 'dew_point': 34, 'humidity': 0.24, 'wind': 22, 'gusts': 28}
    pre_median_2018 = {'temp': 45, 'dew_point': 43, 'humidity': 0.93, 'wind': 14, 'gusts': 23}
    post_median_2018 = {'temp': 44, 'dew_point': 44, 'humidity': 1.00, 'wind': 17, 'gusts': 0}

    new_cols = ['temp', 'dew_point', 'humidity', 'wind', 'gusts']

    for col in new_cols:
        if year == 2015:
            df[col] = [pre_median_2015[col] if x < median else post_median_2015[col] for x in df['Official Time']]
        elif year == 2016:
            df[col] = [pre_median_2016[col] if x < median else post_median_2016[col] for x in df['Official Time']]
        elif year == 2017:
            df[col] = [pre_median_2017[col] if x < median else post_median_2017[col] for x in df['Official Time']]
        else:
            df[col] = [pre_median_2018[col] if x < median else post_median_2018[col] for x in df['Official Time']]

    return df


def clean_data(df, year):
    '''Takes in a DataFrame, drops unnecessary columns, and applies seconds_converter. '''

    # drop duplicates bib as they should be unique
    df.drop_duplicates('Bib', inplace=True)

    # clean the bib value convert to int
    df['Bib'] = df['Bib'].apply(clean_bib)

    # rename columns for clarity
    df.rename(columns={'Overall': 'overall_rank', 'Gender': 'gender_rank',
                       'Division': 'division_rank', 'M/F': 'Gender'}, inplace=True)

    # convert the time to seconds on these columns
    time_cols = ['5K', '10K', '15K', '20K', 'Half', '25K',
                 '30K', '35K', '40K', 'Official Time']
    for col in time_cols:
        df[col] = df[col].apply(seconds_converter)

    # fill the State column with NaNs to 'none' instead so it can be
    # concatenated with the country column
    df['State'].fillna('', inplace=True)
    df['state_country'] = df['State'] + '_' + df['Country']

    # create a new column progression_slope
    df['progression_slope'] = df.apply(race_slope, axis=1)

    df = add_weather_data(df, year)

    # drop unnecessary columns
    df.drop(['Citizen', 'City', 'State', 'Country', '5K', '10K', '15K', '20K',
             '25K', '30K', '35K', '40K', 'Pace'], axis=1, inplace=True)
    df.drop(list(df.filter(regex='Unnamed')), axis=1, inplace=True)
    df.drop(list(df.filter(regex='Proj')), axis=1, inplace=True)

    return df
