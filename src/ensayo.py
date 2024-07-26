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

def elapsedTime(cant_datos):
    st = time.mktime(time.strptime(startTime, "%d/%m/%Y %H:%M:%S"))
    stamps = np.array([time.mktime(time.strptime(t, "%d/%m/%Y %H:%M:%S")) for t in timestamps[-cant_datos:]]) - st
    return stamps

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
    x_axis = elapsedTime(cant_datos)
    axs[0][0].clear()
    for t in indexes["Probeta caliente"]:
        axs[0][0].scatter(x_axis, df[-cant_datos:, t], marker='-')
    axs[0][0].axhline(y=30, color='r', linestyle='-')
    axs[0][0].set_ylim(15, 40)  # Adjust Y-axis limits as per your data
    axs[0][0].set_xlabel('Tiempo transcurrido [s]')
    axs[0][0].set_ylabel('Temperatura [°C]')
    axs[0][0].set_title('Temperaturas probeta lado caliente')
    axs[0][0].legend([columns[t] for t in indexes["Probeta caliente"]])

    axs[0][1].clear()
    for t in indexes["Probeta frío"]:
        axs[0][1].scatter(x_axis, df[-cant_datos:, t], marker='-')
    axs[0][1].set_ylim(0, 25)  # Adjust Y-axis limits as per your data
    axs[0][1].axhline(y=10, color='r', linestyle='-')
    axs[0][1].set_xlabel('Tiempo transcurrido [s]')
    axs[0][1].set_ylabel('Temperatura [°C]')
    axs[0][1].set_title('Temperaturas probeta lado frío')
    axs[0][1].legend([columns[t] for t in indexes["Probeta frío"]])

    axs[1][0].clear()
    axs[1][0].scatter(x_axis, df[-cant_datos:, indexes["Calefactor"][0]], marker='-')
    axs[1][0].scatter(x_axis, df[-cant_datos:, indexes["Refrigerador"][0]], marker='-')
    axs[1][0].set_ylim(0, 255)  # Adjust Y-axis limits as per your data
    axs[1][0].set_xlabel('Tiempo transcurrido [s]')
    axs[1][0].set_ylabel('PWM')
    axs[1][0].legend([columns[indexes["Calefactor"][0]], columns[indexes["Refrigerador"][0]]])
    axs[1][0].set_title('Valores PWM')

    axs[1][1].clear()
    axs[1][1].scatter(x_axis, df[-cant_datos:, indexes["Calefactor"][1]], marker='-')
    axs[1][1].scatter(x_axis, df[-cant_datos:, indexes["Cámara Caliente"][0]], marker='-')
    axs[1][1].scatter(x_axis, df[-cant_datos:, indexes["Cámara Caliente"][1]],  marker='-')
    axs[1][1].scatter(x_axis, df[-cant_datos:, indexes["Cámara Fría"][0]], marker='-')
    axs[1][1].scatter(x_axis, df[-cant_datos:, indexes["Cámara Fría"][1]], marker='-')
    axs[1][1].axhline(y=30, color='r', linestyle='-')
    axs[1][1].axhline(y=10, color='b', linestyle='-')
    axs[1][1].set_ylim(0, 80)  # Adjust Y-axis limits as per your data
    axs[1][1].set_xlabel('Tiempo transcurrido [s]')
    axs[1][1].set_ylabel('Temperatura [°C]')
    axs[1][1].set_title('Temperaturas cámara caliente y fría')
    axs[1][1].legend([columns[indexes["Calefactor"][1]], columns[indexes["Cámara Caliente"][0]], columns[indexes["Cámara Caliente"][1]], columns[indexes["Cámara Fría"][0]], columns[indexes["Cámara Fría"][1]]])

def connect():
    global ser
    global df
    if ser is not None:
        ser.write("0".encode())
        ser.close()
        ser = None
        port_combobox.state(["!disabled"])
        connect_button.config(text="Connect")
        start_button.config(text="Start Plotting")
        start_button.config(state="disabled")
        temp_control_button.config(text="Start Temp Control")
        temp_control_button.config(state="disabled")
        save_data()
        return
    if port_combobox.get() == "":
        return
    port = port_combobox.get().split(" ")[0]
    ser = serial.Serial(port, 115200, timeout=1)
    print("Connected to: ", port_combobox.get())
    port_combobox.state(["disabled"])
    connect_button.config(text="Disconnect")
    start_button.config(state="normal")

def get_ports():
    ports = serial.tools.list_ports.comports()
    ports = [port.device + " " + port.description for port in ports]
    port_combobox.configure(values=ports)
    
def save_data():
    global df
    global timestamps
    temp_timestamps = np.array(["Timestamp"] + timestamps)
    temp_df = np.append([columns], df, axis=0)
    temp_df = np.c_[temp_timestamps, temp_df]
    temp_df = pd.DataFrame(temp_df)
    temp_df.to_csv(output_path + "data_" + startTime.replace("/", "_").replace(" ", "_").replace(":", "_") + ".csv", index=False, header=False)
    print("Data saved!")

def close():
    global ser
    if ser is not None:
        ser.close()
        ser = None
    try:
        root.destroy()
    except:
        pass

def schedule_update():
    global lastSave
    update(0)
    canvas.draw_idle()
    if time.time() - lastSave > 5*60:
        save_data()
        lastSave = time.time()
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

output_path = "../outputs/"

root = tk.Tk()
#root.geometry("1280x720")
root.title("Ensayo")

startTime = readTime()
print("Start Time: ", startTime)

lastSave = time.time()

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

frame = tk.Frame(root)

port_combobox = ttk.Combobox(frame, values=ports, postcommand=get_ports)
port_combobox.grid(row=0, column=0, columnspan=2)

connect_button = tk.Button(frame, text="Connect", command=connect)
connect_button.grid(row=0, column=2, columnspan=2)

close_button = tk.Button(frame, text="Close window", command=close)
# close_button.pack()

start_button = tk.Button(frame, text="Start Plotting", command=plot_toggle, state="disabled")
start_button.grid(row=1, column=0, columnspan=4, sticky="ew")

temp_control_button = tk.Button(frame, text="Start Temp Control", command=temp_control_toggle, state="disabled")
temp_control_button.grid(row=2, column=0, columnspan=4, sticky="ew")

hot_pwm = tk.Scale(frame, from_=0, to=255, orient="horizontal", label="Heater PWM")
hot_pwm.grid(row=3, column=0, columnspan=4, sticky="ew")
cold_pwm = tk.Scale(frame, from_=0, to=255, orient="horizontal", label="Cooler PWM")
cold_pwm.grid(row=4, column=0, columnspan=4, sticky="ew")

# Set up the figure and axis
fig, axs = plt.subplots(2,2, figsize=(4.5, 4.5))
# fig, axs = plt.subplots(2,2)
# ani = animation.FuncAnimation(fig, update, interval=1000)

frame.grid(row=0, column=0, sticky="n")
frame2 = tk.Frame(root)
canvas = tkagg.FigureCanvasTkAgg(fig, master=frame2)
canvas.get_tk_widget().pack()
frame2.grid(row=0, column=1, sticky="n")

root.mainloop()
close()



if not os.path.exists(output_path):
    os.makedirs(output_path)

#save data to csv, with a timestamp in the name
save_data()
# print("Data saved to: ", os.path.abspath(output_path))
