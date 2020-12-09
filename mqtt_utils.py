import paho.mqtt.client as mqtt
import os
import time
#"db9c38ca/TestCaseResults"
BROKER = os.environ.get('BROKER')
BROKER='broker.hivemq.com'
def publish_message(topic,request):#DONT USE DANGER O DANGER!!
    print(BROKER)
    client = mqtt.Client()
    client.connect(BROKER, 1883, 5)
    time.sleep(2)
    if(client.is_connected):
        client.publish(topic, request)
        client.disconnect()

def find_N_return(array , key , value ):
    for items in array:
        if(items[key]==value):
            return items
    return None
publish_message("db9c38ca/GetAutomationResultsBuild","test")