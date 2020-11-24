from logging import DEBUG
from typing import Dict
import mqtt_utils
from flask import Flask, request, jsonify
#from flask_ngrok import run_with_ngrok
from datetime import datetime
import time as T
import json
import logging
import subprocess


# Create Flask app and enable info level logging
app = Flask(__name__)
#run_with_ngrok(app)

INTENTS_2_CHANNELS={
"Reterive Test Cases":"db9c38ca/TestCaseResults"
}
FULFILLMENT_TIME_LIMIT=5



@app.route('/', methods=['POST'])
def webhook():
    """Handle webhook requests from Dialogflow."""
    # Get request body
    try:
        request_ = request.get_json(force=True)
        id = request_['responseId']
        intent = request_['queryResult']['intent']['displayName']
        logging.debug("Recieved Request with id = {0} , intent = {1}".format(id , intent))
    except Exception as e :
        logging.error("Error Occurred while reciving the incoming  request: {0} , \n Error: {1}".format(str(request_), str(e.__traceback__()) ))
        return jsonify({
            "fulfillmentText": "Some Error Occured while processing your request ",
        })
    
    #Send the Request to Remote Processing Engine: 
    try:
        mqtt_utils.publish_message(INTENTS_2_CHANNELS[intent], json.dumps(request_))
        logging.debug("Successfully published the request {0} \n\nto the channel: {1}".format(str(request_), INTENTS_2_CHANNELS[intent] ))
    except Exception as e :
        logging.error("Error Occurred while Send the Request to Remote Processing Engine : \n request: {0} , \n Error: {1}".format(str(request_), str(e.__traceback__()) ))
        return jsonify({
            "fulfillmentText": "Some Error Occured While processing your request ",
        })

    # Wait for Remote Processing to be over: 
    try:
        
        count =0
        while count<FULFILLMENT_TIME_LIMIT:
            logging.debug("attempt: {0}".format(str(count)))
            T.sleep(1)
            fulfilment = json.load(open(INTENTS_2_CHANNELS[intent].replace('/','')+'_FullFillment.json','r'))
            FFM=mqtt_utils.find_N_return(fulfilment, 'id', id )
            if( FFM is not None):
                try:
                    FFM_DATA = FFM['data']['fulfillmentText']
                except:
                    logging.error(" incorrect schema of FFM : {0}".format(str(FFM)))
                    return jsonify({
            "fulfillmentText": "Some Error Occured While processing your request ",
        })
                logging.debug("Successfully fulfilled id {0} with {1} ".format(id , str(FFM)))
                return jsonify({
                "fulfillmentText":FFM_DATA
                })          

            count = count +1
        logging.error("FFM Unsuccessful for id {0}".format(id))
        return jsonify({
            "fulfillmentText": "Oops , something went Wrong while processing your request  ",
        })
    except Exception as e :
        logging.error("Error Occurred while Wait for Remote Processing to be over  request: {0} , \n\n Error: {1}".format(str(request_), str(e.__traceback__()) ))
        return jsonify({
            "fulfillmentText": "Some Error Occured ",
        })
    
    return "FATAL ERROR",500


@app.route('/ping')
def ping():
    return "hello , im alive ",200


@app.route('/fulfilment/<channel>', methods = ['POST'])
def fulfilment(channel):
    incoming_data = request.get_json()
    json.dump(incoming_data , open(channel+'.json','w+'))
    return "Recieved FulFilment",200

if __name__ == '__main__':
    #process=None
    pids=[]
    logging.basicConfig(filename='activity.log',level=logging.DEBUG)
    # for items in INTENTS_2_CHANNELS.keys():        
    #     process= subprocess.Popen(['python messaging_wrapper.py '+INTENTS_2_CHANNELS[items]+'_FullFillment'], shell=True,
    #         stdin=None, stdout=None, stderr=None, close_fds=True)
    #     pids.append(process.pid)
    logging.info("process ids: "+ str(pids))
    app.run( threaded = True)