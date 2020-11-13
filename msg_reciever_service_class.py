import paho.mqtt.client as mqtt
import json
import sys
import logging

class msg_processor():
    def __init__(self, topic):
        logging.basicConfig(filename=topic.replace('/','__LOG__')+'.log',level=logging.DEBUG)
        self.topic_store=[]
        self.topic = topic
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect("mqtt.eclipse.org", 1883, 60)
        self.client.loop_forever()

    def on_connect(self, client, userdata, flags, rc):
        logging.debug(self.topic+" : Connected with result code "+str(rc))
        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        client.subscribe(self.topic)

    def on_message(self, client, userdata, msg):
        logging.debug(self.topic+" Recieved message: ")
        try:
            fulfilments = json.loads(msg.payload)
            json.dump(fulfilments, open(self.topic.replace('/','')+'.json', 'w+'))
        except:
            logging.error(sys.exc_info())


