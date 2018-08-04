from transforms3d import axangles as tf
import pandas as pd
import numpy as np
import math
import os
from FileLoader import all2one


def normalization(df):
    rotation_vector = df[['Milliseconds','RotationVectorX', 'RotationVectorY', 'RotationVectorZ', 'RotationVectorcos']]

    sensors = ['AccelerometerLinear', 'Accelerometer', 'Gravity', 'Compass', 'Gyroscope']
    headers = df.columns

    df_sensors = []
    for sensor in sensors:
        if headers.contains(sensor + 'X'):
            df_sensors.append(sensor)

    for row in range(0, len(df)):
        axis = rotation_vector.iloc[row, 1:4].values
        angle = 2 * math.acos(rotation_vector.iloc[row, 4])

        rotation_matrix = tf.axangle2mat(axis, angle)
        for sensor in df_sensors:
            sensor_data = df.ix[row][[sensor+'X', sensor+'Y', sensor+'Z']]
            normalized_row = np.matmul(rotation_matrix , np.asarray(sensor_data))
            df.ix[row][sensor + 'X', sensor + 'Y', sensor + 'Z'] = normalized_row

    return df

def all2one_normalized(path):
    df = all2one(path)
    return normalization(df)


if __name__ == '__main__':

    from FileLoader import all2one
    path = 'data/WalkCarClustering'
    df = all2one_normalized(path+'/Walk')
    normalization(df)
    df.to_csv(path+'/Walk/Normalized.csv',sep=',',index=False)