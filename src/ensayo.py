import serial
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from collections import deque
import json
import os

# Set up the serial port. Replace 'COM3' with your serial port.
ser = serial.Serial('COM3', 9600, timeout=1)

# Deque to store incoming data
data = deque(maxlen=100)  # Adjust maxlen as per your requirements

# Read json file map from file
cwd = os.getcwd()
map = open("heated_chamber.json", "r")

# Initialize the deque with zeros
for _ in range(100):
    data.append(0)

def process_data(line):
    # read data from serial and map to json
    data = line.split(",")
    print(data)
    # map data to json
    mapped_data = map.format(*data)
    json_data = json.loads(mapped_data)
    print(json_data)

def update(frame):
    line = ser.readline().decode('utf-8').strip()
    if line:
        try:
            process_data(line)
            data.append(value)
        except ValueError:
            pass  # Ignore any non-numeric data

    axs[0].clear()
    axs[0].plot(data)

    axs[0].set_xlim(0, 100)
    axs[0].set_ylim(-10, 10)  # Adjust Y-axis limits as per your data
    axs[0].set_xlabel('Time')
    axs[0].set_ylabel('Value')
    axs[0].set_title('Live Serial Data')

    axs[1].scatter(range(100), data, c='r', s=5)


# Set up the figure and axis
fig, axs = plt.subplots(1,2)
ani = animation.FuncAnimation(fig, update, interval=100)

plt.show()

# Close the serial port when done
ser.close()
