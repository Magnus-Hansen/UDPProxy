from socket import *
import requests

def post(postJson):
        response = requests.post("https://airqualityrest20241202114729.azurewebsites.net/api/AirQualities", data=postJson, headers=headersArray)
        
        print(response)

try: 
    serverPort = 10100
    serverSocket = socket(AF_INET, SOCK_DGRAM)

    serverAddress = ('', serverPort)

    serverSocket.bind(serverAddress)
    print("The server is ready")

    headersArray = {'Content-type': 'application/json'}

    while True:
        message, clientAddress = serverSocket.recvfrom(2048)
        print("Received message:" + message.decode())
        post(message)
        
except KeyboardInterrupt:
    print('Interrupted')