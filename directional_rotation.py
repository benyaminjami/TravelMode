import math
import transforms3d.derivations.eulerangles as eular
import numpy as np
import pandas as pd
import transforms3d


def directional_normalization(df):
    rotation_vector = df[['Milliseconds', 'CompassBearing']]
    # pd.options.mode.chained_assignment = None
    sensors = ['AccelerometerLinear', 'Accelerometer', 'Gravity', 'Compass', 'Gyroscope']
    headers = df.columns

    df_sensors = []
    for sensor in sensors:
        if headers.contains(sensor + 'X'):
            df_sensors.append(sensor)

    for row in range(0, len(df)):

        compassbearing = rotation_vector.loc[row, 'CompassBearing']

        axis = [0,0,1]
        # rotation_matrix = transforms3d.axangles.axangle2mat(axis , np.radians(compassbearing))
        rotation_matrix = np.array(eular.z_rotation(np.radians(compassbearing))).astype(np.float64)
        for sensor in df_sensors:
            sensor_data = df.ix[row][[sensor + 'X', sensor + 'Y', sensor + 'Z']]
            normalized_row = np.matmul(rotation_matrix, np.asarray(sensor_data))
            df.ix[row,[sensor + 'X', sensor + 'Y', sensor + 'Z']] = normalized_row

    return df


if __name__ == '__main__':
    from Direction import add_direction
    path = 'data/MoveDirectionNormalization/Normalized.csv'
    df = pd.read_csv(path, engine='python')
    df = add_direction(df)
    df2 = df.copy()
    Directions = directional_normalization(df)
    print(1)