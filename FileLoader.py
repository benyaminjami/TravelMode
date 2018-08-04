import os

import pandas as pd
import numpy as np

import sys
import glob
import errno


def all2one(path):
    result = pd.DataFrame
    flag = True
    for file in os.listdir(path):
        if not (os.path.isdir(path + '/' + file) and file == 'Normalized.csv'):
            df = pd.read_csv(path + '/' + file)
            newColumns = []
            df['Milliseconds'] = np.floor(df['Milliseconds']//25)*25
            for column in df.columns:
                if column != 'Milliseconds':
                    column = file[:-4] + column
                newColumns.append(column)
            df.columns = newColumns
            # print(df.head())
            if(flag):
                result = df.drop_duplicates()
                flag = False
            else:
                result = pd.merge(result, df.drop_duplicates(subset=['Milliseconds']), how='outer', on='Milliseconds')
    return result


if __name__ == '__main__':

    df = all2one('./data/NormalizationTest')
    print(df.head())
