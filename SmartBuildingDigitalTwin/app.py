from flask import Flask, jsonify, render_template
import paho.mqtt.client as mqtt

app = Flask(__name__)

latest_data = {
    "room101": {
        "temperature": 0
    },
    "room102": {
        "temperature": 0
    },
    "room103": {
        "temperature": 0
    },
    "room104": {
        "temperature": 0
    }
}

history = {
    "room101": [],
    "room102": [],
    "room103": [],
    "room104": []
}

activity_log = []

room_status = {
    "room101": "NORMAL",
    "room102": "NORMAL",
    "room103": "NORMAL",
    "room104": "NORMAL"
}

BROKER = "localhost"
PORT = 1883
TOPIC = "building/+/temperature"


def on_connect(client, userdata, flags, reason_code, properties):
    print("Connected to MQTT Broker")
    client.subscribe(TOPIC)


def on_message(client, userdata, message):
    temperature = float(message.payload.decode())

    room = message.topic.split("/")[1]

    latest_data[room]["temperature"] = temperature

    history[room].append(temperature)

    if len(history[room]) > 20:
        history[room].pop(0)

    if temperature > 35:
        new_status = "ALERT"
    elif temperature > 30:
        new_status = "HIGH"
    else:
        new_status = "NORMAL"

    if new_status != room_status[room]:

        if new_status == "ALERT":
            activity_log.append(
                f"🔴 {room} entered ALERT state at {temperature}°C"
            )

        elif new_status == "HIGH":
            activity_log.append(
                f"🟠 {room} entered HIGH temperature state at {temperature}°C"
            )

        else:
            activity_log.append(
                f"🟢 {room} returned to NORMAL at {temperature}°C"
            )

        room_status[room] = new_status

    if len(activity_log) > 20:
        activity_log.pop(0)

    print(f"Received {room} Temperature: {temperature}°C")


mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

mqtt_client.connect(BROKER, PORT)

mqtt_client.loop_start()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/data")
def get_data():
    return jsonify(latest_data)

@app.route("/api/history")
def get_history():
    return jsonify(history)

@app.route("/api/activity")
def get_activity():
    return jsonify(activity_log)


if __name__ == "__main__":
    app.run(debug=True)