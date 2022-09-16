#!/usr/bin/python3
import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
rawdata_dir = 'rawdata/'
filenames = os.listdir(rawdata_dir)
data = {'2bar':[], '6bar':[], \
            '10bar':[], '14bar':[]}


for filename in filenames:
	pressure = filename.split('_')[1]
	file_dir = rawdata_dir + filename
	raw = pd.read_csv(file_dir, sep='\t')
	raw = raw.to_numpy()
	data[pressure].append(raw)

for key, cases in data.items():
	print(key)
	for it in cases:
		print(it.shape)
		plt.plot(it[:,1])
		plt.plot(it[:,2])
		plt.show()
iterations = 3
pressures = ['2', '6', '10', '14']
prefix = '10'
