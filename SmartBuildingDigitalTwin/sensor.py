import paho.mqtt.client as mqtt
import random
import time

BROKER = "localhost"
PORT = 1883
TOPICS = {
    "room101": "building/room101/temperature",
    "room102": "building/room102/temperature",
    "room103": "building/room103/temperature",
    "room104": "building/room104/temperature"
}

temperatures = {
    "room101": 25.0,
    "room102": 25.0,
    "room103": 25.0,
    "room104": 25.0
}

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

client.connect(BROKER, PORT)

print("Room 101 Temperature Sensor Started...")


while True:
    for room, topic in TOPICS.items():
        temperatures[room] += random.uniform(-0.5, 0.8)

        if temperatures[room] > 30:
            temperatures[room] -= 1.2

        temperatures[room] = max(20, min(40, temperatures[room]))
        temperature = round(temperatures[room], 1)

        client.publish(topic, temperature)

        print(f"{room} Temperature: {temperature}°C")

    time.sleep(3)