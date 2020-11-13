import paho.mqtt.client as mqtt

#"db9c38ca/TestCaseResults"
def publish_message(topic,request):
    client = mqtt.Client()
    client.connect("mqtt.eclipse.org", 1883, 60)
    client.publish(topic, request)
    client.disconnect()

def find_N_return(array , key , value ):
    for items in array:
        if(items[key]==value):
            return items
    return None
