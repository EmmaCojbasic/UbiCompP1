import sys
import time
import requests
import json
import serial

edgexip = "localhost"

# Konfigurisanje serijskog porta na koji je Arduino povezan
ser = serial.Serial('COM7', 9600)  

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

            print("Temp: %s°C, humidity: %s%%" % (25, humval))

        time.sleep(2)

    except Exception as e:
        print(f"Error: {e}")
        time.sleep(2)