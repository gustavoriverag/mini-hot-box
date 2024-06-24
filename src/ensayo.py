import serial
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from collections import deque
import json
import os
import time
import pandas as pd
import numpy as np


def readTime():
    # return current time as string in DD/MM/YYYY HH:MM:SS format
    return time.strftime("%d/%m/%Y %H:%M:%S", time.localtime())

def process_data(line):
    global df
    # read data from serial and map to json
    input_data = line.split(",")
    # map data to json
    mapped_data = json.loads(data_structure)
    for i in range(0, len(input_data)):
        for key in mapped_data["g"]:
            for key_sub in key["d"]:
                # print(key_sub["v"])
                if key_sub["v"] == f"{{{i}}}":
                    key_sub["v"] = input_data[i]
                    break
    ordered_data = []
    for key in mapped_data["g"]:
        for key_sub in key["d"]:
            ordered_data.append(float(key_sub["v"]))
    df = np.append(df, np.array([ordered_data]), axis=0)
    timestamps.append(readTime())

def update(frame):
    global df
    line = ser.readline().decode('utf-8').strip()
    if line:
        try:
            process_data(line)
        except ValueError:
            pass  # Ignore any non-numeric data

    cant_datos = min(100, len(df))
    axs[0][0].clear()
    for t in indexes["Probeta caliente"]:
        axs[0][0].plot(df[-cant_datos:, t])
    axs[0][0].set_xlim(0, 100)
    axs[0][0].set_ylim(15, 40)  # Adjust Y-axis limits as per your data
    axs[0][0].set_xlabel('Time')
    axs[0][0].set_ylabel('Temperatura [°C]')
    axs[0][0].set_title('Temperaturas probeta lado caliente')

    axs[0][1].clear()
    for t in indexes["Probeta frío"]:
        axs[0][1].plot(df[-cant_datos:, t])
    axs[0][1].set_xlim(0, 100)
    axs[0][1].set_ylim(0, 25)  # Adjust Y-axis limits as per your data
    axs[0][1].set_xlabel('Time')
    axs[0][1].set_ylabel('Temperatura [°C]')
    axs[0][1].set_title('Temperaturas probeta lado frío')

    axs[1][0].clear()
    potencia = df[-cant_datos:, indexes["Calefactor"][2]] * df[-cant_datos:, indexes["Calefactor"][3]]
    axs[1][0].plot(potencia)
    axs[1][0].set_xlim(0, 100)
    axs[1][0].set_ylim(0, 120)  # Adjust Y-axis limits as per your data
    axs[1][0].set_xlabel('Time')
    axs[1][0].set_ylabel('Potencia [W]')
    axs[1][0].set_title('Potencia consumida por calefactor')

    axs[1][1].clear()
    axs[1][1].plot(df[-cant_datos:, indexes["Cámara Caliente"][0]])
    axs[1][1].plot(df[-cant_datos:, indexes["Cámara Caliente"][1]])
    axs[1][1].plot(df[-cant_datos:, indexes["Cámara Fría"][0]])
    axs[1][1].set_xlim(0, 100)
    axs[1][1].set_ylim(0, 40)  # Adjust Y-axis limits as per your data
    axs[1][1].set_xlabel('Time')
    axs[1][1].set_ylabel('Temperatura [°C]')
    axs[1][1].set_title('Temperaturas cámara caliente y fría')
    axs[1][1].legend([columns[indexes["Cámara Caliente"][0]], columns[indexes["Cámara Caliente"][1]], columns[indexes["Cámara Fría"][0]]])

startTime = readTime()
print("Start Time: ", startTime)

# Set up the serial port.
ser = serial.Serial('COM7', 9600, timeout=1)

# Read json file map from file
data_structure = open("heated_chamber.json", "r", encoding="utf-8").read()

indexes = dict()
columns = []
timestamps = [readTime()]

i=0
for key in json.loads(data_structure)["g"]:
    column_name = key["t"]
    indexes[column_name] = []
    for key_sub in key["d"]:
        columns.append(column_name + "_" + key_sub["t"])
        indexes[column_name].append(i)
        i += 1

df = np.zeros((1, len(columns)))

# Set up the figure and axis
fig, axs = plt.subplots(2,2)
ani = animation.FuncAnimation(fig, update, interval=100)
fig.set_size_inches(10, 10)
plt.show()

timestamps = np.array(["Timestamp"] + timestamps)
df = np.append([columns], df, axis=0)
df = np.c_[timestamps, df]

output_path = "../outputs/"
if not os.path.exists(output_path):
    os.makedirs(output_path)

#save data to csv, with a timestamp in the name
df = pd.DataFrame(df)
df.to_csv(output_path + "data_" + startTime.replace("/", "_").replace(" ", "_").replace(":", "_") + ".csv", index=False, header=False)

# Close the serial port when done
ser.close()
