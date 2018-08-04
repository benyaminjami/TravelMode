from math import sin, cos, sqrt, atan2, radians
import compassbearing as cb
from EarthCoordinatesRotation import *
from FileLoader import *
import numpy as np
import pandas as pd
import transforms3d as tf
import pyproj as proj

"""In this piece of code the four fields ['Speed' , 'DirectionX' ,'DirectionY' , 'CompassBearing'] will be added to 
the data frame 

Where CompassBearing is the angle of the movement relative to the North pole (in degrees)
and DirectionX and DirectionY are the values of the movement vectors (normalized)

--> Use the add_direction function to do the job
"""


# returns the distance of two points in KMs
def get_distance(d_lat1, d_long1, d_lat2, d_long2):
    # this part is another algorithm for testing the answer of the funcion
    # dx = (d_long2 - d_long1) * 40042.74 * math.cos((d_lat1 + d_lat2) * math.pi / 360) / 360
    # dy = (d_lat1 - d_lat2) * 40042.74 / 360
    # result = {'dx' : dx , 'dy' : dy}
    # print(result)
    # print('distance with first solution is: ' , sqrt(dx**2 + dy**2))

    R = 6371.0  # Earth radius in KMs

    lat1 = radians(d_lat1)
    lon1 = radians(d_long1)
    lat2 = radians(d_lat2)
    lon2 = radians(d_long2)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    # here are some mathematical calculations that i don't know why they work but they do! :))
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c

    return distance

def add_direction(input_df):
    df = input_df[['Milliseconds', 'GPSLatitude', 'GPSLongitude']]
    df = df.drop_duplicates(subset='GPSLatitude')
    compassbearing_series = pd.Series()
    direction_x_series = pd.Series()
    direction_y_series = pd.Series()
    speed_series = pd.Series()
    df = df.reset_index()
    for row in range(0, len(df)):
        if row == len(df) - 1 or np.isnan(df.loc[row, 'GPSLatitude']) or np.isnan(df.loc[row + 1, 'GPSLatitude']):
            direction_x_series = direction_x_series.append(pd.Series(direction_x_series.iloc[-1]), ignore_index=True)
            direction_y_series = direction_y_series.append(pd.Series(direction_y_series.iloc[-1]), ignore_index=True)
            speed_series = speed_series.append(pd.Series(speed_series.iloc[-1]), ignore_index=True)
            compassbearing_series = compassbearing_series.append(pd.Series(compassbearing_series.iloc[-1]),
                                                                 ignore_index=True)
        else:

            lat1, long1 = df.loc[row, 'GPSLatitude'], df.loc[row, 'GPSLongitude']
            lat2, long2 = df.loc[row + 1, 'GPSLatitude'], df.loc[row + 1, 'GPSLongitude']

            distance = get_distance(lat1, long1, lat2, long2) * 1000
            diff_timestamp = (df.loc[row + 1, 'Milliseconds'] - df.loc[row, 'Milliseconds']) / 1000

            x, y, compassbearing = cb.calculate_initial_compass_bearing(lat1, long1, lat2, long2)

            direction_x_series = direction_x_series.append(pd.Series(x), ignore_index=True)
            direction_y_series = direction_y_series.append(pd.Series(y), ignore_index=True)
            speed_series = speed_series.append(pd.Series(distance / diff_timestamp), ignore_index=True)
            compassbearing_series = compassbearing_series.append(pd.Series(compassbearing), ignore_index=True)

    df = df.assign(Speed=speed_series.values)
    df = df.assign(DirectionX=direction_x_series.values)
    df = df.assign(DirectionY=direction_y_series.values)
    df = df.assign(CompassBearing=compassbearing_series.values)
    df = df.drop(columns=['index', 'Milliseconds'])
    input_df = pd.merge(input_df, df, how='left', on=['GPSLatitude', 'GPSLongitude'])

    return input_df


if __name__ == '__main__':  # for testing the function
    path = 'data/WalkCarClustering/Car/CarNormalized.csv'
    df = pd.read_csv(path, engine='python')
    Directions = add_direction(df)
    print(Directions.head())
