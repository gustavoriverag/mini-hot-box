import matplotlib.pyplot as plt
import numpy as np
import glob

# data_folder = "..\outputs\*.csv"
# print(data_folder)
# data_files = glob.glob(data_folder)

# last_file = data_files[-1]

#numpy open csv file

data = np.genfromtxt("C:/Users/Gustavo/Documents/mini-hot-box/outputs/data_23_07_2024_18_58_04.csv", delimiter=',', encoding='utf-8')

data = data[1:, 1:]

# make matrix with the first nine columns with the last row
nth_data = data[-1, 0:9].reshape(3,3)[::-1]

plt.imshow(nth_data, cmap='hot', interpolation='nearest')
plt.colorbar()
plt.show()

# scatter 9 columns
for i in range(9):
    plt.plot(data[:, i])
# plot straight line at y=30
plt.axhline(y=30, color='r', linestyle='-')
plt.show()

plt.plot(data[:, 9])
plt.plot(data[:, 10])
plt.plot(data[:, 12])
plt.legend(["T amb", "T def", "T calef"])
plt.axhline(y=30, color='r', linestyle='-')
plt.show()

print(data)