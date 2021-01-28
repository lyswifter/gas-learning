
import pandas as pd
import numpy as np
import requests
from sklearn.linear_model import LogisticRegression
from sklearn import preprocessing
from sklearn.preprocessing import MinMaxScaler
import pickle

from .consts import ORIGINAL_DATA_FILE

class Forecastting:
	cou = 0
	def __init__(self, count):
		self.cou = count
	def forecast(self):
		sample_rate = pd.read_csv('sample_rate')
		L2LR = pickle.load(open('L2LR.pickle', 'rb'))
		gas = pd.read_csv('block_new')
		gas = gas.iloc[len(gas) - 10000:len(gas), :]
		rate_all = [1.6180339887, 2.058, 2.6180339887, 3.33, 4.236]
		forecast_l_all = [157.08203932948422, 135.55, 127.0820393254225, 123.34, 121.59971939649687]
		score = [0, 0, 0, 0, 0]
		forecast = [0, 0, 0, 0, 0]
		gas = gas.drop(columns = ['epoch', 'limit_avg_block', 'cap_avg_block', 'premium_avg_block'])
		fee = gas.parent_basefee.copy()
		for j in range(5):
			rate = rate_all[j]
			forecast_l = forecast_l_all[j]
			outter = sample_rate.iloc[0, 2 * j]
			inner = sample_rate.iloc[0, 2 * j + 1]
			res_range = round(inner)
			list = pd.DataFrame(range(res_range))
			for i in range(res_range):
				list.iloc[i, 0] *= outter / inner
			raw_range = round(list.iloc[len(list) - 1, 0])
			res = np.interp(list.values.reshape(len(list)), pd.DataFrame(range(raw_range)).values.reshape(raw_range), fee.iloc[len(fee) - raw_range:len(fee)].sort_index(ascending = False).values.reshape(raw_range)).copy()
			res = pd.DataFrame(res).sort_index(ascending = False)
			l = np.polyfit(range(res_range), res.values.reshape(len(res)), 1)
			k_0 = l[0]
			l = np.poly1d(l)
			b = l(forecast_l)
			for i in range(len(res)):
				res.iloc[i, 0] -= b
			res_raw_0 = res.copy()
			res_0 = res.rolling(5).median().iloc[4:]
			outter = sample_rate.iloc[1, 2 * j]
			inner = sample_rate.iloc[1, 2 * j + 1]
			res_range = round(inner)
			list = pd.DataFrame(range(res_range))
			for i in range(res_range):
				list.iloc[i, 0] *= outter / inner
			raw_range = round(list.iloc[len(list) - 1, 0])
			res = np.interp(list.values.reshape(len(list)), pd.DataFrame(range(raw_range)).values.reshape(raw_range), fee.iloc[len(fee) - raw_range:len(fee)].sort_index(ascending = False).values.reshape(raw_range)).copy()
			res = pd.DataFrame(res).sort_index(ascending = False)
			l = np.polyfit(range(res_range), res.values.reshape(len(res)), 1)
			k_1 = l[0]
			l = np.poly1d(l)
			b = l(forecast_l)
			for i in range(len(res)):
				res.iloc[i, 0] -= b
			res_raw_1 = res.copy()
			res_1 = res.rolling(5).median().iloc[4:]
			outter = sample_rate.iloc[2, 2 * j]
			inner = sample_rate.iloc[2, 2 * j + 1]
			res_range = round(inner)
			list = pd.DataFrame(range(res_range))
			for i in range(res_range):
				list.iloc[i, 0] *= outter / inner
			raw_range = round(list.iloc[len(list) - 1, 0])
			res = np.interp(list.values.reshape(len(list)), pd.DataFrame(range(raw_range)).values.reshape(raw_range), fee.iloc[len(fee) - raw_range:len(fee)].sort_index(ascending = False).values.reshape(raw_range)).copy()
			res = pd.DataFrame(res).sort_index(ascending = False)
			l = np.polyfit(range(res_range), res.values.reshape(len(res)), 1)
			k_2 = l[0]
			l = np.poly1d(l)
			b = l(forecast_l)
			for i in range(len(res)):
				res.iloc[i, 0] -= b
			res_raw_2 = res.copy()
			res_2 = res.rolling(5).median().iloc[4:]
			_res_0 = res_1.iloc[:len(res_0)].values / res_0.values
			_res_1 = res_2.iloc[:len(res_0)].values / res_0.values
			_res_2 = res_2.iloc[:len(res_1)].values / res_1.values
			for i in range(len(_res_0)):
				if( - 1<_res_0[i, 0]<1):
					_res_0[i, 0] = 1 / _res_0[i, 0]
			prop_0 = _res_0.mean()
			_res_1 = np.sign(_res_1) * np.sqrt(np.abs(_res_1))
			for i in range(len(_res_1)):
				if( - 1<_res_1[i, 0]<1):
					_res_1[i, 0] = 1 / _res_1[i, 0]
			prop_1 = _res_1.mean()
			for i in range(len(_res_2)):
				if( - 1<_res_2[i, 0]<1):
					_res_2[i, 0] = 1 / _res_2[i, 0]
			prop_2 = _res_2.mean()
			score[j] = (np.var(_res_0) + np.var(_res_1) + np.var(_res_2) + np.var([prop_0, prop_1, prop_2])) * np.var([k_0 / rate, k_1 / (rate * rate), k_2 / (rate * rate * rate)])
			_res_0 = res_raw_0.values / res_raw_1.iloc[:len(res_raw_0)].values
			_res_1 = res_raw_0.values / res_raw_2.iloc[:len(res_raw_0)].values
			_res_2 = res_raw_1.values / res_raw_2.iloc[:len(res_raw_1)].values
			prop_raw = pd.concat([pd.DataFrame(_res_0), pd.DataFrame(_res_1), pd.DataFrame(_res_2)], axis = 1)
			to_fill = prop_raw.iloc[:, 0]
			to_fill = to_fill.fillna(np.median(to_fill[np.isfinite(to_fill)]))
			prop_raw.iloc[:, 0] = to_fill
			to_fill = prop_raw.iloc[:, 1]
			to_fill = to_fill.fillna(np.median(to_fill[np.isfinite(to_fill)]))
			prop_raw.iloc[:, 1] = to_fill		
			history_raw = pd.concat([pd.DataFrame(res_raw_0), pd.DataFrame(res_raw_1), pd.DataFrame(res_raw_2)], axis = 1)
			for i in range(len(history_raw)):
				if(np.isnan(history_raw.iloc[i, 0])):
					if(np.isnan(history_raw.iloc[i, 1])):
						history_raw.iloc[i, 0] = history_raw.iloc[i, 2] * np.mean(prop_raw.iloc[:, 1]) * np.mean(prop_raw.iloc[:, 1])
					else:
						history_raw.iloc[i, 0] = history_raw.iloc[i, 1] * np.mean(prop_raw.iloc[:, 0])
			history_raw = history_raw.iloc[:, 0]
			for i in range(len(prop_raw)):
				prop_raw.iloc[i, 0] = np.median(prop_raw.iloc[i, :])
			prop_raw = prop_raw.iloc[:, 0]
			for i in range(len(prop_raw)):
				history_raw.iloc[i] *= prop_raw.iloc[i]
			for i in range(len(prop_raw), len(history_raw)):
				history_raw.iloc[i] *= np.median(prop_raw)
			forecast[j] = history_raw.median() - history_raw.rolling(5).median().iloc[4]
		for i in range(5):
			if(np.min(score) == score[i]):
				gas.range.iloc[len(gas) - 1] = sample_rate.iloc[2, 2 * i]
				gas.forecast.iloc[len(gas) - 1] = forecast[i]
		gas.to_csv('gas', index = False)
		gas = gas.drop(columns = ['parent_basefee'])
		raw_range = round(np.median(gas.range.iloc[len(gas) - 120:len(gas)]))
		if(raw_range <= 508):
			raw_ex = [1, 3, 18] 
			rate_f = 0
			fee_range = 254
		elif(raw_range <= 1046):
			raw_ex = [2, 7, 34]
			rate_f = 1
			fee_range = 440
		elif(raw_range <= 2153):
			raw_ex = [4, 14, 76]
			rate_f = 2
			fee_range = 744
		elif(raw_range <= 4431):
			raw_ex = [9, 26, 157]
			rate_f = 3
			fee_range = 1242
		elif(raw_range <= 9122):
			raw_ex = [18, 63, 323]
			rate_f = 4
			fee_range = 2064
		gas = pd.concat([gas, (fee.rolling(round(5 * rate_all[rate_f])).median())], axis = 1)
		gas = pd.concat([gas, (fee.rolling(round(8 * rate_all[rate_f])).median())], axis = 1)
		gas = pd.concat([gas, (fee.rolling(round(13 * rate_all[rate_f])).median())], axis = 1)
		gas = pd.concat([gas, (fee.rolling(round(21 * rate_all[rate_f])).median())], axis = 1)
		gas = pd.concat([gas, (fee.rolling(round(34 * rate_all[rate_f])).median())], axis = 1)
		gas = pd.concat([gas, (fee.rolling(round(55 * rate_all[rate_f])).median())], axis = 1)
		gas = pd.concat([gas, (fee.rolling(round(89 * rate_all[rate_f])).median())], axis = 1)
		gas.block_count = gas.block_count.rolling(120).mean()
		gas.count_block = gas.count_block.rolling(120).mean()
		gas.limit_total_block = gas.limit_total_block.rolling(120).median()
		gas.cap_total_block = gas.cap_total_block.rolling(120).median()
		gas.premium_total_block = gas.premium_total_block.rolling(120).median()
		gas = pd.concat([gas, gas.block_count.rolling(round(120 * rate_all[rate_f])).mean()], axis = 1)
		gas = pd.concat([gas, gas.count_block.rolling(round(120 * rate_all[rate_f])).mean()], axis = 1)
		gas = pd.concat([gas, gas.limit_total_block.rolling(round(120 * rate_all[rate_f])).median()], axis = 1)
		gas = pd.concat([gas, gas.cap_total_block.rolling(round(120 * rate_all[rate_f])).median()], axis = 1)
		gas = pd.concat([gas, gas.premium_total_block.rolling(round(120 * rate_all[rate_f])).median()], axis = 1)
		gas = gas.drop(columns = ['range'])
		my_scaler = MinMaxScaler(feature_range = (0, 1))
		gas_test = gas.iloc[len(gas) - raw_range:len(gas), :].copy()
		tmp = gas_test.copy()
		tmp = my_scaler.fit_transform(tmp).copy()
		gas_test.loc[:, :] = tmp.copy()
		gas_test = pd.DataFrame(pd.DataFrame(gas_test.iloc[len(gas_test) - 1, :]).values.reshape(1, 19))
		fee_percent = [round(0.0296 * fee_range), round(0.077448747 * fee_range), round(0.1548 * fee_range), round(0.28 * fee_range), round(0.49886 * fee_range), round(0.71754 * fee_range), round(0.8428246 * fee_range), round(0.92 * fee_range), round(0.968 * fee_range)]
		_fee_test_raw = fee.iloc[len(gas) - 1].copy()
		fee_test = [_fee_test_raw, _fee_test_raw, _fee_test_raw, _fee_test_raw, _fee_test_raw, _fee_test_raw, _fee_test_raw, _fee_test_raw, _fee_test_raw, _fee_test_raw, _fee_test_raw]
		fee_test = pd.DataFrame(pd.DataFrame(fee_test).values.reshape(1, 11))
		for i in range(1, 11):
			fee_test.iloc[0, i] = 0
		fee_test_sort = fee.iloc[len(gas) - fee_range:len(gas)].copy().sort_values()
		if(fee_test.iloc[0, 0] >= fee_test_sort.iloc[fee_percent[8]]):
			fee_test.iloc[0, 1] = 1
		elif(fee_test.iloc[0, 0] >= fee_test_sort.iloc[fee_percent[7]]):	
			fee_test.iloc[0, 2] = 1
		elif(fee_test.iloc[0, 0] >= fee_test_sort.iloc[fee_percent[6]]):	
			fee_test.iloc[0, 3] = 1
		elif(fee_test.iloc[0, 0] >= fee_test_sort.iloc[fee_percent[5]]):	
			fee_test.iloc[0, 4] = 1
		elif(fee_test.iloc[0, 0] >= fee_test_sort.iloc[fee_percent[4]]):	
			fee_test.iloc[0, 5] = 1
		elif(fee_test.iloc[0, 0] >= fee_test_sort.iloc[fee_percent[3]]):	
			fee_test.iloc[0, 6] = 1
		elif(fee_test.iloc[0, 0] >= fee_test_sort.iloc[fee_percent[2]]):	
			fee_test.iloc[0, 7] = 1
		elif(fee_test.iloc[0, 0] >= fee_test_sort.iloc[fee_percent[1]]):	
			fee_test.iloc[0, 8] = 1
		elif(fee_test.iloc[0, 0] >= fee_test_sort.iloc[fee_percent[0]]):	
			fee_test.iloc[0, 9] = 1
		else:	
			fee_test.iloc[0, 10] = 1
		fee_test = fee_test.iloc[:, 1:]
		gas_test = pd.concat([gas_test.reset_index(drop = True), fee_test.reset_index(drop = True)], axis = 1)
		isIncrease = L2LR.predict(gas_test)
		proba_positive, proba_negtive = L2LR.predict_proba(gas_test)
		print(isIncrease, proba_negtive, proba_positive)
