import paho.mqtt.client as mqtt
import os
#"db9c38ca/TestCaseResults"
BROKER = os.environ.get('BROKER')

def publish_message(topic,request):
    client = mqtt.Client()
    client.connect(BROKER, 1883, 60)
    client.publish(topic, request)
    client.disconnect()

def find_N_return(array , key , value ):
    for items in array:
        if(items[key]==value):
            return items
    return None
