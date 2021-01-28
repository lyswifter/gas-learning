import pickle

import pandas as pd
import numpy as np
import requests

from sklearn.linear_model import LogisticRegression
from sklearn import preprocessing
from sklearn.preprocessing import MinMaxScaler

from .consts import ORIGINAL_DATA_FILE


class Forecastting:

    def forecast(self, file_path):
        L2LR = pickle.load(open('L2LR.pickle', 'rb'))

        gas = pd.read_csv(file_path)

        rate_all = [1.6180339887, 2.058, 2.6180339887, 3.33, 4.236]
        forecast_l_all = [
            157.08203932948422, 135.55, 127.0820393254225, 123.34,
            121.59971939649687
        ]
        score = [0, 0, 0, 0, 0]
        forecast = [0, 0, 0, 0, 0]

        gas = gas.iloc[len(gas) - 10000:len(gas), :]
        gas = gas.drop(columns=[
            'epoch', 'limit_avg_block', 'cap_avg_block', 'premium_avg_block'
        ])

        fee = gas.parent_basefee.copy()
        gas = gas.drop(columns=['parent_basefee'])

        raw_range = round(np.median(gas.range.iloc[len(gas) - 120:len(gas)]))

        if (raw_range == 508):
            raw_ex = [1, 3, 18]
            rate_f = 0
            fee_range = 254

        if (raw_range == 1046):
            raw_ex = [2, 7, 34]
            rate_f = 1
            fee_range = 440

        if (raw_range == 2153):
            raw_ex = [4, 14, 76]
            rate_f = 2
            fee_range = 744

        if (raw_range == 4431):
            raw_ex = [9, 26, 157]
            rate_f = 3
            fee_range = 1242

        if (raw_range == 9122):
            raw_ex = [18, 63, 323]
            rate_f = 4
            fee_range = 2064

        gas = pd.concat(
            [gas, (fee.rolling(round(5 * rate_all[rate_f])).median())], axis=1)
        gas = pd.concat(
            [gas, (fee.rolling(round(8 * rate_all[rate_f])).median())], axis=1)
        gas = pd.concat(
            [gas, (fee.rolling(round(13 * rate_all[rate_f])).median())],
            axis=1)
        gas = pd.concat(
            [gas, (fee.rolling(round(21 * rate_all[rate_f])).median())],
            axis=1)
        gas = pd.concat(
            [gas, (fee.rolling(round(34 * rate_all[rate_f])).median())],
            axis=1)
        gas = pd.concat(
            [gas, (fee.rolling(round(55 * rate_all[rate_f])).median())],
            axis=1)
        gas = pd.concat(
            [gas, (fee.rolling(round(89 * rate_all[rate_f])).median())],
            axis=1)

        gas.block_count = gas.block_count.rolling(120).mean()
        gas.count_block = gas.count_block.rolling(120).mean()
        gas.limit_total_block = gas.limit_total_block.rolling(120).median()
        gas.cap_total_block = gas.cap_total_block.rolling(120).median()
        gas.premium_total_block = gas.premium_total_block.rolling(120).median()

        gas = pd.concat([
            gas,
            gas.block_count.rolling(round(120 * rate_all[rate_f])).mean()
        ],
                        axis=1)
        gas = pd.concat([
            gas,
            gas.count_block.rolling(round(120 * rate_all[rate_f])).mean()
        ],
                        axis=1)
        gas = pd.concat([
            gas,
            gas.limit_total_block.rolling(round(
                120 * rate_all[rate_f])).median()
        ],
                        axis=1)
        gas = pd.concat([
            gas,
            gas.cap_total_block.rolling(round(
                120 * rate_all[rate_f])).median()
        ],
                        axis=1)
        gas = pd.concat([
            gas,
            gas.premium_total_block.rolling(round(
                120 * rate_all[rate_f])).median()
        ],
                        axis=1)

        gas = gas.drop(columns=['range'])

        my_scaler = MinMaxScaler(feature_range=(0, 1))

        gas_test = gas.iloc[len(gas) - raw_range:len(gas), :].copy()
        tmp = gas_test.copy()
        tmp = my_scaler.fit_transform(tmp).copy()
        gas_test.loc[:, :] = tmp.copy()
        gas_test = pd.DataFrame(
            pd.DataFrame(gas_test.iloc[len(gas_test) - 1, :]).values.reshape(
                1, 19))

        fee_percent = [
            round(0.0296 * fee_range),
            round(0.077448747 * fee_range),
            round(0.1548 * fee_range),
            round(0.28 * fee_range),
            round(0.49886 * fee_range),
            round(0.71754 * fee_range),
            round(0.8428246 * fee_range),
            round(0.92 * fee_range),
            round(0.968 * fee_range)
        ]

        _fee_test_raw = fee.iloc[len(gas) - 1].copy()

        fee_test = [
            _fee_test_raw, _fee_test_raw, _fee_test_raw, _fee_test_raw,
            _fee_test_raw, _fee_test_raw, _fee_test_raw, _fee_test_raw,
            _fee_test_raw, _fee_test_raw, _fee_test_raw
        ]
        fee_test = pd.DataFrame(pd.DataFrame(fee_test).values.reshape(1, 11))

        for i in range(1, 11):
            fee_test.iloc[0, i] = 0

        fee_test_raw = fee.iloc[len(gas) -
                                fee_range:len(gas)].copy().sort_values()

        if (fee_test.iloc[0, 0] >= fee_test_sort.iloc[fee_percent[8]]):
            fee_test.iloc[0, 1] = 1
        elif (fee_test.iloc[0, 0] >= fee_test_sort.iloc[fee_percent[7]]):
            fee_test.iloc[0, 2] = 1
        elif (fee_test.iloc[0, 0] >= fee_test_sort.iloc[fee_percent[6]]):
            fee_test.iloc[0, 3] = 1
        elif (fee_test.iloc[0, 0] >= fee_test_sort.iloc[fee_percent[5]]):
            fee_test.iloc[0, 4] = 1
        elif (fee_test.iloc[0, 0] >= fee_test_sort.iloc[fee_percent[4]]):
            fee_test.iloc[0, 5] = 1
        elif (fee_test.iloc[0, 0] >= fee_test_sort.iloc[fee_percent[3]]):
            fee_test.iloc[0, 6] = 1
        elif (fee_test.iloc[0, 0] >= fee_test_sort.iloc[fee_percent[2]]):
            fee_test.iloc[0, 7] = 1
        elif (fee_test.iloc[0, 0] >= fee_test_sort.iloc[fee_percent[1]]):
            fee_test.iloc[0, 8] = 1
        elif (fee_test.iloc[0, 0] >= fee_test_sort.iloc[fee_percent[0]]):
            fee_test.iloc[0, 9] = 1
        else:
            fee_test.iloc[0, 10] = 1

        fee_test = fee_test.iloc[:, 1:]
        gas_test = pd.concat(
            [gas_test.reset_index(drop=True),
             fee_test.reset_index(drop=True)],
            axis=1)

        is_increase = L2LR.predict(gas_test)
        proba_positive, proba_negtive = L2LR.predict_proba(gas_test)
        print(is_increase, proba_negtive, proba_positive)

        return is_increase, proba_positive, proba_negtive