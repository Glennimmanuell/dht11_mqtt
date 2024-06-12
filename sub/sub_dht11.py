import paho.mqtt.client as mqtt
from collections import deque
from matplotlib import pyplot as plt

mqtt_server = 'broker.hivemq.com'
topic_sub_temp = 'esp/dht/temperature_glenn'
topic_sub_hum = 'esp/dht/humidity_glenn'

class dhtdata:
    def __init__(self, maxdata=1000):
        self.axis_x = deque(maxlen=maxdata)
        self.axis_temp = deque(maxlen=maxdata)
        self.axis_hum = deque(maxlen=maxdata)

    def add(self, x, temp, hum):
        self.axis_x.append(x)
        self.axis_temp.append(temp)
        self.axis_hum.append(hum)

def main():
    global data, myplot
    data = dhtdata()
    print(data)
    fig, ax = plt.subplots()
    plt.title("Plot data temperature dan humidity")
    myplot = dhtplot(ax)

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(mqtt_server, 1883, 60)
    client.loop_start()

    count = 0
    while True:
        count += 1
        plt.pause(0.25)

class dhtplot:
    def __init__(self, axes):
        self.axes = axes
        self.lineplot, = axes.plot([], [], "go--", label="Temperature")
        self.lineplot2, = axes.plot([], [], "bo:", label="Humidity")

    def plot(self, dataplot):
        self.lineplot.set_data(dataplot.axis_x, dataplot.axis_temp)
        self.lineplot2.set_data(dataplot.axis_x, dataplot.axis_hum)
        self.axes.set_xlim(min(dataplot.axis_x), max(dataplot.axis_x))
        ymin = min(min(dataplot.axis_temp), min(dataplot.axis_hum)) - 5
        ymax = max(max(dataplot.axis_temp), max(dataplot.axis_hum)) + 5
        self.axes.set_ylim(ymin, ymax)

def on_connect(client, userdata, flags, rc):
    print("Puji Tuhan connect, result code = "+str(rc))
    client.subscribe(topic_sub_temp)
    client.subscribe(topic_sub_hum)

def on_message(client, userdata, msg):
    global data, myplot
    print(msg.topic+" "+msg.payload.decode())
    temp = 0
    hum = 0
    if msg.topic == topic_sub_temp:
        temp = float(msg.payload.decode())
    elif msg.topic == topic_sub_hum:
        hum = float(msg.payload.decode())
    if temp is not None and hum is not None:
        data.add(len(data.axis_x), temp, hum)
        myplot.plot(data)


if __name__ == "__main__":
    main()
