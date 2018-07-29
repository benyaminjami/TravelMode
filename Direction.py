from Rotation_Test import *
from FileLoader import *
import numpy as np
import pandas as pd
import transforms3d as tf


def get_lat_long(df):
    return df[['Milliseconds', 'GPSLatitude', 'GPSLongitude']]

def get_distance(lat1,lat2,long1,long2):
    R = 6378.1  # Radius of the Earth
    brng = 1.57  # Bearing is 90 degrees converted to radians.
    d = 15  # Distance in km

    lat1 = math.radians(52.20472)  # Current lat point converted to radians
    lon1 = math.radians(0.14056)  # Current long point converted to radians

    lat2 = math.asin(math.sin(lat1) * math.cos(d / R) +
                     math.cos(lat1) * math.sin(d / R) * math.cos(brng))

    lon2 = lon1 + math.atan2(math.sin(brng) * math.sin(d / R) * math.cos(lat1),
                             math.cos(d / R) - math.sin(lat1) * math.sin(lat2))

    lat2 = math.degrees(lat2)
    lon2 = math.degrees(lon2)

def get_direction(df2):
    df = df2.drop_duplicates(subset = 'GPSLatitude')
    lat_dif_series = pd.Series()
    long_dif_series = pd.Series()
    speed_series = pd.Series()
    df = df.reset_index()
    for row in range(0, len(df) - 1):
        if row == len(df) - 2:
            lat_dif_series.append(lat_dif_series.iloc[-1])
            long_dif_series.append(long_dif_series.iloc[-1])
            speed_series.append(speed_series.iloc[-1])
        else:
            lat_dif = df.loc[row + 1, 'GPSLatitude'] - df.loc[row, 'GPSLatitude']
            long_dif = df.loc[row + 1, 'GPSLongitude'] - df.loc[row, 'GPSLongitude']
            lat_dif_series = lat_dif_series.append(pd.Series(lat_dif),ignore_index=True)
            long_dif_series = long_dif_series.append(pd.Series(long_dif),ignore_index=True)
            distance = np.sqrt(lat_dif**2 + long_dif**2)
            speed_series = speed_series.append(pd.Series(distance / (df.loc[row+1 , 'Milliseconds'] - df.loc[row , 'Milliseconds'])),
                                               ignore_index=True)
    df = df.assign(Speed = speed_series.values)
    df = df.assign(LatitudeMove = lat_dif_series.values )
    df = df.assign(LongitudeMove = long_dif_series.values)
    return df


if __name__ == '__main__':
    path = 'data/MoveDirectionNormalization/Normalized.csv'
    df = pd.read_csv(path,engine = 'python')
    Directions = get_direction(get_lat_long(df))
    print(Directions.head())