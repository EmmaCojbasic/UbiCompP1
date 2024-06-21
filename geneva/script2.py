import sys
import time
import requests
import json
import serial

edgexip = "localhost"

# Function to open the serial port
def open_serial_port(port):
    try:
        return serial.Serial(port, 9600)
    except serial.SerialException as e:
        print(f"Failed to open serial port {port}: {e}")
        return None

# Attempt to open the serial port
ser = open_serial_port('COM7')

while not ser:
    print("Retrying to open the serial port in 5 seconds...")
    time.sleep(5)
    ser = open_serial_port('COM7')

while True:
    try:
        # Čitanje podataka sa COM7 porta, preko koga Arduino šalje podatke
        line = ser.readline().decode('utf-8').strip()

        # Parsiranje vrednosti za temperaturu i vlažnost
        tempval, humval = line.split(',')

        tempval = str(float(tempval))
        humval = str(float(humval))

        urlTemp = 'http://%s:49986/api/v1/resource/Temp_and_Humidity_sensor_cluster_01/temperature' % edgexip
        urlHum  = 'http://%s:49986/api/v1/resource/Temp_and_Humidity_sensor_cluster_01/humidity' % edgexip

        headers = {'content-type': 'application/json'}

        if(float(humval) < 100):
            response = requests.post(urlTemp, data=json.dumps(float(tempval)), headers=headers, verify=False)
            response = requests.post(urlHum, data=json.dumps(float(humval)), headers=headers, verify=False)

            print("Temp: %s°C, humidity: %s%%" % (tempval, humval))

        time.sleep(2)

    except serial.SerialException as e:
        print(f"Serial error: {e}")
        ser.close()
        ser = open_serial_port('COM7')
        while not ser:
            print("Retrying to open the serial port in 5 seconds...")
            time.sleep(5)
            ser = open_serial_port('COM7')
    except Exception as e:
        print(f"Error: {e}")
        time.sleep(2)
