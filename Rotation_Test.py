from transforms3d import axangles as tf
import pandas as pd
import numpy as np
import math
import os


def Normalization(df):
    # output_path = path + '/Normalized/'
    # if not os.path.exists(output_path):
    #     os.makedirs(output_path)
    # pd.DataFrame(rotation_vector).to_csv(output_path+'RotationVector.csv',sep=',')
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
    from FileLoader import all2one
    path = './data/NormalizationTest'
    df = all2one(path)
    return Normalization(df)


if __name__ == '__main__':

    from FileLoader import all2one
    path = 'data/WalkCarClustering'
    df = all2one(path+'/Walk')
    Normalization(df)
    df.to_csv(path+'/Walk/Normalized.csv',sep=',',index=False)
    print(1)
#
#
#
# rotated_gravity
#     gravity = pd.read_csv(path + 'Gravity.csv')
#     rotated_gravity = pd.DataFrame()
#
#     for row in range(0, len(gravity)):
#         axis = rotation_vector.iloc[row, 1:4].values
#         angle = math.acos(rotation_vector.iloc[row, 4])
#
#         rotation_matrix = tf.axangle2mat(axis, 2 * angle, is_normalized=False)
#
#         rotated = pd.DataFrame([np.matmul(rotation_matrix, gravity.iloc[row, 1:4])])
#
#         rotated_gravity = rotated_gravity.append(rotated)
# print(rotated_gravity.head())
