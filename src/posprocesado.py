import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# data_folder = "..\outputs\*.csv"
# print(data_folder)
# data_files = glob.glob(data_folder)

# last_file = data_files[-1]

#numpy open csv file

data = np.genfromtxt("C:\\Users\\Gustavo\\Downloads\\data_2024_08_13_11_52_36.csv", delimiter=',', encoding='utf-8')
data = np.genfromtxt("..\\outputs\\data_2024_09_02_15_11_38.csv", delimiter=',', encoding='utf-8')

data = data[1:, 1:]

# make matrix with the first nine columns with the last row
hot_map = np.mean(data[-100:, 0:9], axis=0).reshape(3,3)[::-1]
cold_map = np.mean(data[-100:, -12:-3], axis=0).reshape(3,3)[::-1]

fig, ax = plt.subplots(1, 2)
ax[0].imshow(hot_map, cmap='hot', interpolation='nearest')
# ax[0].colorbar()
ax[1].imshow(cold_map, cmap='cool', interpolation='nearest')
# plt.colorbar()
plt.show()


# scatter 9 columns
x_axis = range(0, 5*len(data[:,9]), 5)
for i in range(9):
    plt.plot(x_axis, data[:, i])
# plot straight line at y=30
plt.axhline(y=35, color='r', linestyle='--')
plt.show()

for i in range(-12, -3):
    plt.plot(x_axis, data[:, i])
# plot straight line at y=30
plt.axhline(y=28, color='b', linestyle='--')
plt.ylim(10, 35)
plt.show()

excl_c = []
mask_c = [False if i in excl_c else True for i in range(0,9)]
#excl_f = [1, 4]
excl_f = []
mask_f = [False if i in excl_f else True for i in range(0,9)]
prom_c = np.mean(data[:, 0:9][-35:, mask_c])
prom_f = np.mean(data[:, -12:-3][-35:, mask_f])

print("Promedio lado caliente:", prom_c)
print("Promedio lado frío:", prom_f)
print("Delta:", prom_c - prom_f)

prom_c_temp = np.mean(data[:, 0:9][:, mask_c], axis=1)
prom_f_temp = np.mean(data[:, -12:-3][:,mask_f], axis=1)
tamano = min(100, len(prom_c_temp)-1)
poly_c = np.polyfit(range(0, 5*len(prom_c_temp[-tamano:]), 5), prom_c_temp[-tamano:], 1)
poly_f = np.polyfit(range(0, 5*len(prom_f_temp[-tamano:]), 5), prom_f_temp[-tamano:], 1)

print("Pendiente lado caliente:", poly_c[0]*3600)
print("Pendiente lado frío:", poly_f[0]*3600)

plt.plot(x_axis, prom_c_temp)
plt.plot(x_axis, prom_f_temp)
plt.plot(x_axis[-tamano:], np.polyval(poly_c, range(0, 5*tamano, 5)), linestyle='--')
plt.plot(x_axis[-tamano:], np.polyval(poly_f, range(0, 5*tamano, 5)), linestyle='--')
plt.axhline(y=35, color='r', linestyle='--')
# plt.axhline(y=28.3, color='g', linestyle='--')
plt.axhline(y=28, color='b', linestyle='--')
plt.grid()
plt.xlabel('Tiempo (s)')
plt.ylabel('Temperatura (°C)')
plt.legend(["Promedio probeta caliente", "Promedio probeta fría"])
plt.show()

plt.plot(data[:, 9])
plt.plot(data[:, 10])
plt.plot(data[:, 12])
plt.legend(["T amb", "T def", "T calef"])
plt.axhline(y=35, color='r', linestyle='--')
plt.show()

pwm = [0, 35, 36, 38, 40, 81, 82, 83, 85, 100, 255]
V = [0, 1.88, 1.92, 2.02, 2.11, 4.03, 4.07, 4.12, 4.19, 4.91, 11.9]

factor = np.polyfit(pwm, V, 3)
print(factor)
# plt.scatter(pwm, V)
# plt.plot(np.linspace(0, 255, 100), np.polyval(factor, np.linspace(0, 255, 100)), linestyle='--')
# plt.grid()
# plt.show()

V = np.polyval(factor, data[:, 11])
plt.plot(x_axis, V)
plt.show()

Q_aux = 1.7 + 1
R = 1.3
Q_h = (V**2)/R
Q_net = Q_h + Q_aux
# print(Q_net)
A = 0.5*0.7

U = Q_net/(A*(prom_c_temp - prom_f_temp))

#Stationarity analysis for U

tamano = min(1080, len(U)-1)

u_pd = pd.Series(U[-tamano:])
rolling_mean = u_pd.rolling(window=50).mean()
rolling_std = u_pd.rolling(window=50).std()

plt.plot(x_axis[-tamano:], u_pd)
plt.plot(x_axis[-tamano:], rolling_mean, label='mean', color='r')
plt.plot(x_axis[-tamano:], rolling_std + rolling_mean, label='std', color='g')
plt.plot(x_axis[-tamano:], rolling_mean - rolling_std, label='std', color='g')
plt.grid()
plt.ylim(0, 10)
plt.xlabel('Tiempo (s)')
plt.ylabel('Transmitancia térmica (W/m²K)')
plt.legend()
plt.show()


fit = np.polyfit(range(0, 5*len(U[-tamano:]), 5), U[-tamano:], 1)
print("Promedio U:", np.mean(U[-tamano:]))
print("Pendiente U:", fit[0]*3600)
print("Desviación U:", np.std(U[-tamano:]))
print("SNR U:", np.mean(U[-tamano:])/np.std(U[-tamano:]))

plt.plot(x_axis, U)
plt.plot(x_axis[-tamano:], np.polyval(fit, range(0, 5*tamano, 5)), linestyle='--')
plt.grid()
plt.xlabel('Tiempo (s)')
plt.ylabel('Transmitancia térmica (W/m²K)')
plt.ylim(0, 10)
plt.show()


off = 100
x_lineal = np.array(range(0, 150, 5)) + off
m, n = np.polyfit(x_lineal, data[1:, 9][off//5:len(x_lineal)+off//5], 1)
#r squared factor
r = np.corrcoef(x_lineal, data[1:, 9][off//5:len(x_lineal)+off//5])
#print(r)
#print(m, n)

fig, ax1 = plt.subplots()
ax1.plot(x_lineal, m*x_lineal + n)
ax1.plot(range(0, 5*len(data[1:,9]), 5), data[1:, 9], 'g-')
ax1.set_xlabel('time (s)')
ax1.set_ylabel('T amb', color='g')
ax1.tick_params('y', colors='g')
ax2 = ax1.twinx()
ax2.plot(np.array(range(0, 5*len(data[1:,9]), 5)) + 60, data[1:, 11], 'b-')
ax2.set_ylabel('PWM', color='b')
ax2.tick_params('y', colors='b')
plt.show()

# T_max = 23.3
# T_min = 19.6
# dT = T_max - T_min
# dPWM = 255
# K = dT/dPWM
# T_63_2 = 0.632 * dT
# tau = T_63_2 / m
# theta = 60
# print(K, tau, theta)

# #Ziegler nichols
# Kp = 1.2*tau/(K*(theta + tau))
# Ti = 2*(theta + tau)
# Td = 0.5*theta

# #Cohen Coon
# Kp = 1/K*(1.35 + (0.27*theta)/tau)
# Ti = tau*(2.5+0.85*theta/tau)
# Td = 0.37*tau*(1+0.95*theta/tau)

# Ki = Kp/Ti
# Kd = Kp*Td


# print(Kp, Ki*5, Kd/5)

# print(data)