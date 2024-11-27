import time
import requests
import json
from scd30_i2c import SCD30

headersArray = {'Content-type': 'application/json'}
def post(postJson):
    response = requests.post("http://localhost:5041/api/AirQualities", data=postJson, headers=headersArray)
    print(response)

scd30 = SCD30()

scd30.set_measurement_interval(2)
scd30.start_periodic_measurement()

time.sleep(2)

while True:
    if scd30.get_data_ready():
        m = scd30.read_measurement()
        if m is not None:
            #print(f"CO2: {m[0]:.2f}ppm, temp: {m[1]:.2f}'C, rh: {m[2]:.2f}%")
            #print(m)
            jsonM = json.dumps({"Humidity": m[2], "CO2": m[0]})
            post(jsonM)

        time.sleep(10)
    else:
        time.sleep(0.2)





