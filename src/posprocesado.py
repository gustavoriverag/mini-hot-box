import matplotlib.pyplot as plt
import numpy as np
import glob

# data_folder = "..\outputs\*.csv"
# print(data_folder)
# data_files = glob.glob(data_folder)

# last_file = data_files[-1]

#numpy open csv file

data = np.genfromtxt("C:/Users/Gustavo/Documents/mini-hot-box/outputs/datos_experimento_calefaccion.csv", delimiter=',', encoding='utf-8')

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


plt.show()
off = 100
x_lineal = np.array(range(0, 150, 5)) + off
m, n = np.polyfit(x_lineal, data[1:, 9][off//5:len(x_lineal)+off//5], 1)
#r squared factor
r = np.corrcoef(x_lineal, data[1:, 9][off//5:len(x_lineal)+off//5])
print(r)
print(m, n)

fig, ax1 = plt.subplots()
ax1.plot(x_lineal, m*x_lineal + n)
ax1.plot(range(0, 5*len(data[1:,9]), 5), data[1:, 9], 'g-')
ax1.set_xlabel('time (s)')
ax1.set_ylabel('T amb', color='g')
ax1.tick_params('y', colors='g')
ax2 = ax1.twinx()
ax2.plot(np.array(range(0, 5*len(data[1:,9]), 5)) + 60, data[1:, 11], 'b-')
ax2.set_ylabel('T def', color='b')
ax2.tick_params('y', colors='b')
plt.show()

T_max = 23.3
T_min = 19.6
dT = T_max - T_min
dPWM = 255
K = dT/dPWM
T_63_2 = 0.632 * dT
tau = T_63_2 / m
theta = 60
print(K, tau, theta)

#Ziegler nichols
Kp = 1.2*tau/(K*(theta + tau))
Ti = 2*(theta + tau)
Td = 0.5*theta

#Cohen Coon
Kp = 1/K*(1.35 + (0.27*theta)/tau)
Ti = tau*(2.5+0.85*theta/tau)
Td = 0.37*tau*(1+0.95*theta/tau)

Ki = Kp/Ti
Kd = Kp*Td


print(Kp, Ki*5, Kd/5)

# print(data)