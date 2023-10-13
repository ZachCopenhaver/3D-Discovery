import matplotlib.pyplot as plt
import csv
import os
import re
import numpy as np

def num_sort(test_string):
    return list(map(int, re.findall(r'\d+', test_string)))[0]

files = []
x = [0,5,10,15,20,25,30]
y = []
i = 0
y10 = []
y25 = []
y1 = []

for filename in os.listdir('./'):
	if os.path.isfile(filename):
		if (os.path.splitext(filename)[1] == '.csv'):
			files.append(filename)
	else:
		continue
files.sort(key = num_sort)

for test in files:
	inFile = open(test, 'r')
	size = os.path.getsize(test)
	inFile.seek(size - 7)
	line = inFile.readline()
	total = ''
	if (line[0] == '0'):
		total = line[0]
		if (test[5:7] == '1m'):
			y1.append(int(total))
		elif (test[5:9] == '10cm'):
			y10.append(int(total))
		elif (test[5:9] == '25cm'):
			y25.append(int(total))
		elif (test[6:8] == '1m'):
			y1.append(int(total))
		elif (test[6:10] == '10cm'):
			y10.append(int(total))
		elif (test[6:10] == '25cm'):
			y25.append(int(total))
		#y.append(int(total))
	else:
		total = line[0:3]
		if (test[5:7] == '1m'):
			y1.append(int(total))
		elif (test[5:9] == '10cm'):
			y10.append(int(total))
		elif (test[5:9] == '25cm'):
			y25.append(int(total))
		elif (test[6:8] == '1m'):
			y1.append(int(total))
		elif (test[6:10] == '10cm'):
			y10.append(int(total))
		elif (test[6:10] == '25cm'):
			y25.append(int(total))

plt.plot(x,np.array(y10)/300,label = '10cm')
plt.plot(x,np.array(y25)/300,label = '25cm')
plt.plot(x,np.array(y1)/300,label = '1m')
plt.xlabel('Divergence Angle (Degrees)')
plt.ylabel('Probability of Successful Transmissions (logscale)')
plt.legend()
plt.title('Success Rate Test')
plt.yscale('log')
plt.tight_layout()
plt.savefig('success_test_plot.pdf', format="pdf", bbox_inches="tight")
plt.show()
