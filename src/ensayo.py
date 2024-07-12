import tkinter as tk
import tkinter.ttk as ttk
import serial
import serial.tools.list_ports
import matplotlib.pyplot as plt
import matplotlib.backends.backend_tkagg as tkagg
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
    if ser is None:
        line = None
    else: 
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
    axs[0][1].set_title(columns[indexes["Calefactor"][2]])

    axs[1][0].clear()
    potencia = df[-cant_datos:, indexes["Calefactor"][2]] * df[-cant_datos:, indexes["Calefactor"][3]]
    # axs[1][0].plot(potencia)
    axs[1][0].plot(df[-cant_datos:, indexes["Calefactor"][0]])
    axs[1][0].set_xlim(0, 100)
    # axs[1][0].set_ylim(0, 120)  # Adjust Y-axis limits as per your data
    axs[1][0].set_xlabel('Time')
    axs[1][0].set_ylabel('Potencia [W]')
    axs[1][0].set_title('Potencia consumida por calefactor')

    axs[1][1].clear()
    axs[1][1].plot(df[-cant_datos:, indexes["Calefactor"][1]])
    axs[1][1].plot(df[-cant_datos:, indexes["Cámara Caliente"][0]])
    axs[1][1].plot(df[-cant_datos:, indexes["Cámara Caliente"][1]])
    axs[1][1].plot(df[-cant_datos:, indexes["Cámara Fría"][0]])
    axs[1][1].set_xlim(0, 100)
    axs[1][1].set_ylim(0, 40)  # Adjust Y-axis limits as per your data
    axs[1][1].set_xlabel('Time')
    axs[1][1].set_ylabel('Temperatura [°C]')
    axs[1][1].set_title('Temperaturas cámara caliente y fría')
    axs[1][1].legend([columns[indexes["Calefactor"][1]], columns[indexes["Cámara Caliente"][0]], columns[indexes["Cámara Caliente"][1]], columns[indexes["Cámara Fría"][0]]])
    # axs[1][1].clear()
    # axs[1][1].plot(df[-cant_datos:, indexes["Calefactor"][1]])
    # # axs[1][1].plot(df[-cant_datos:, indexes["Calefactor"][3]])
    # axs[1][1].set_xlim(0, 100)
    # axs[1][1].set_ylim(20, 60)  # Adjust Y-axis limits as per your data
    # axs[1][1].set_xlabel('Time')
    # axs[1][1].set_ylabel('Temperatura [°C]')
    # axs[1][1].set_title('Temperaturas calefactor')
    # axs[1][1].legend([columns[indexes["Calefactor"][1]], columns[indexes["Calefactor"][3]]])
    # axs[1][1].legend([columns[indexes["Cámara Caliente"][0]], columns[indexes["Cámara Caliente"][1]], columns[indexes["Cámara Fría"][0]]])
def connect():
    global ser
    if ser is not None:
        ser.close()
        ser = None
        port_combobox.state(["!disabled"])
        connect_button.config(text="Connect")
        start_button.config(state="disabled")
        temp_control_button.config(state="disabled")
        return
    if port_combobox.get() == "":
        return
    port = port_combobox.get()
    ser = serial.Serial(port, 9600, timeout=1)
    print("Connected to: ", port_combobox.get())
    port_combobox.state(["disabled"])
    connect_button.config(text="Disconnect")
    start_button.config(state="normal")

def close():
    global ser
    if ser is not None:
        ser.close()
        ser = None
    root.destroy()

def schedule_update():
    update(0)
    canvas.draw_idle()
    root.after(1000, schedule_update)

def plot_toggle():
    global state
    if state == 0:
        schedule_update()
        ser.write("1".encode())
        state = 1
        temp_control_button.config(state="normal")
        start_button.config(text="Stop Plotting")
    elif state == 1:
        ser.write("0".encode())
        state = 0
        temp_control_button.config(state="disabled")
        start_button.config(text="Start Plotting")

def temp_control_toggle():
    global state
    if state == 1:
        ser.write("2".encode())
        state = 2
        start_button.config(state="disabled")
        temp_control_button.config(text="Stop Temp Control")
    else:
        ser.write("0".encode())
        ser.write("1".encode())
        state = 1
        start_button.config(state="normal")
        temp_control_button.config(text="Start Temp Control")

root = tk.Tk()
# root.geometry("1280x720")
root.title("Ensayo")

startTime = readTime()
print("Start Time: ", startTime)

#Get list of available serial ports
ports = serial.tools.list_ports.comports()
ports = [port.device for port in ports]

# Set up the serial port.
ser = None
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

state = 0

port_combobox = ttk.Combobox(root, values=ports)
port_combobox.pack()

connect_button = tk.Button(root, text="Connect", command=connect)
connect_button.pack()

close_button = tk.Button(root, text="Close window", command=close)
close_button.pack()

start_button = tk.Button(root, text="Start Plotting", command=plot_toggle, state="disabled")
start_button.pack()

temp_control_button = tk.Button(root, text="Start Temp Control", command=temp_control_toggle, state="disabled")
temp_control_button.pack()

# Set up the figure and axis
fig, axs = plt.subplots(2,2, figsize=(12,12))
# ani = animation.FuncAnimation(fig, update, interval=1000)

canvas = tkagg.FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack()

root.mainloop()

timestamps = np.array(["Timestamp"] + timestamps)
df = np.append([columns], df, axis=0)
df = np.c_[timestamps, df]

output_path = "../outputs/"
print(os.path.abspath(output_path))

if not os.path.exists(output_path):
    os.makedirs(output_path)

#save data to csv, with a timestamp in the name
df = pd.DataFrame(df)
df.to_csv(output_path + "data_" + startTime.replace("/", "_").replace(" ", "_").replace(":", "_") + ".csv", index=False, header=False)

# Close the serial port when done
if ser is not None:
    ser.close()
