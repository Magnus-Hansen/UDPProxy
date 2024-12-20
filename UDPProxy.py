import time
import requests
import json
from scd30_i2c import SCD30
from gpiozero import LED
from socket import *
from gpiozero import Button
import threading

#serverPort = 12000
#serverSocket = socket(AF_INET, SOCK_STREAM)
#serverSocket.bind(('', serverPort))
#serverSocket.listen(1)

headersArray = {'Content-type': 'application/json'}
def post(postJson):
    #response = requests.post("http://localhost:5041/api/AirQualities", data=postJson, headers=headersArray)
    response = requests.post("https://airqualityrest20241202114729.azurewebsites.net/api/AirQualities", data=postJson, headers=headersArray)
    
    print(response)

try: 
    scd30 = SCD30()
    # led = LED(18)
    button = Button(23)
    

    scd30.set_measurement_interval(2)
    scd30.start_periodic_measurement()

    time.sleep(2)

    def main_stuff():
        m = scd30.read_measurement()
        if m is not None:
            jsonM = json.dumps({"location": "R-D3.07", "humidity": round(m[2]), "cO2": round(m[0]), "temperature": round(m[1])})
#            connectionSocket.send(jsonM.encode())
            post(jsonM)
                
#            if m[0] < 1000:
#               led.off()

#            if m[0] >= 1000:
#               led.on()

    def interval_sensor():
        if scd30.get_data_ready():
            main_stuff()

            time.sleep(10)
        else:
            time.sleep(0.2)
    
    def button_sensor():
        if button.is_pressed:
            main_stuff()
            
        time.sleep(1)
#    connectionSocket, addr = serverSocket.accept()
    while True:

        t1 = threading.Thread(target=interval_sensor)
        t2 = threading.Thread(target=button_sensor)

        t1.start()
        t2.start()

        t1.join()
        t2.join()

except KeyboardInterrupt:
    print('Interrupted')
