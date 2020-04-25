# imports
import numpy as np
import pandas as pd
from datetime import date, timedelta
import random


# function definition
def create_data_set(number_of_rows, measurement_columns=1):
    """ Create a two part data set with various flaws """

    # minimum of 1 measurement column
    measurement_columns = 1 if measurement_columns < 1 else measurement_columns

    start_date = date.today()-timedelta(days=365)
    end_date = date.today()

    # data1 is the primary dataset
    data1 = pd.DataFrame()
    data1['ID'] = range(1, number_of_rows+1)
    data1['ID'] = data1['ID'].apply(lambda x: str(x).zfill(len(str(number_of_rows))))
    data1['Start Date'] = start_date
    data1['End Date'] = end_date
    data1['Active'] = np.random.random(number_of_rows)
    data1['Active'] = data1['Active'].apply(lambda x: True if x < 0.9 else False)
    data1['-'] = '-'

    # create a mean and standard deviation for each column of measurements
    means = []
    standard_deviations = []
    multipliers = [1, 10, 100, 1000, 10000, 100000]
    for i in range(measurement_columns):
        multiplier = np.random.choice(multipliers)
        mean = multiplier+multiplier*np.random.random()
        means.append(mean)

        standard_deviation = mean/10
        standard_deviation *= abs(np.random.normal())
        standard_deviations.append(standard_deviation)

        # fill each column of measurements with values
        data1['Measurements {}'.format(i+1)] = \
            np.random.normal(means[i], standard_deviations[i], number_of_rows).astype('str')

    # each row has its own set of measurement dates
    measurement_dates_columns = []
    for i in range(number_of_rows):
        measurement_dates = np.sort(np.random.choice(365, size=measurement_columns, replace=False))
        measurement_dates = [start_date+timedelta(days=int(i)) for i in measurement_dates]
        measurement_dates_columns.append(measurement_dates)
    data1 = pd.concat([data1, pd.DataFrame(measurement_dates_columns).astype('str')], axis=1)

    # create a string describing the value and date of each measurement
    for i in range(0, measurement_columns):
        data1['Measurements {}'.format(i+1)] = \
            'Value of '+data1['Measurements {}'.format(i+1)] + ' recorded on ' + data1[i]
    data1 = data1.drop(columns=range(measurement_columns))

    # select a number of errors (np.nan values) to create and randomly apply them to the data set
    number_of_errors = max(1, np.random.randint(int(data1.size/100)))
    for i in range(number_of_errors):
        data1.iloc[np.random.randint(data1.shape[0]), np.random.randint(data1.shape[1])] = np.nan

    # remove a measurement column number
    data1 = data1.rename(columns={'Measurements {}'.format(random.randint(1, measurement_columns)): 'Measurements '})

    # shuffle rows and create duplicate rows
    data1 = data1.sample(frac=1, replace=False)
    data1 = data1.append(data1.sample(frac=0.01, replace=False)).reset_index(drop=True)

    # create second data set from the ID and Active columns, then remove the Active column from the primary data set
    data2 = data1[['ID', 'Active']]
    data1 = data1.drop(columns='Active')

    # output data sets to file

   # data1.to_csv('measurements.csv', index=False)
   # data2.to_csv('active.csv', index=False)


# create the actual data sets
create_data_set(10000, 10)
