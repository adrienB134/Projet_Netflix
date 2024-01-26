# Code inspired from Confluent Cloud official examples library
# https://github.com/confluentinc/examples/blob/7.1.1-post/clients/cloud/python/producer.py

from confluent_kafka import Producer
import json
import ccloud_lib  # Library not installed with pip but imported from ccloud_lib.py
import numpy as np
import time
import requests
from datetime import datetime

# Initialize configurations from "python.config" file
CONF = ccloud_lib.read_ccloud_config("python.config")
TOPIC = "netflix"
url = "https://jedha-netflix-real-time-api.herokuapp.com/users-currently-watching-movie"


# Create Producer instance
producer_conf = ccloud_lib.pop_schema_registry_params_from_config(CONF)
producer = Producer(producer_conf)

# Create topic if it doesn't already exist
ccloud_lib.create_topic(CONF, TOPIC)

delivered_records = 0


# Callback called acked (triggered by poll() or flush())
# when a message has been successfully delivered or
# permanently failed delivery (after retries).
def acked(err, msg):
    global delivered_records
    # Delivery report handler called on successful or failed delivery of message
    if err is not None:
        print("Failed to deliver message: {}".format(err))
    else:
        delivered_records += 1
        print(
            "Produced record to topic {} partition [{}] @ offset {}".format(
                msg.topic(), msg.partition(), msg.offset()
            )
        )


try:
    # Starts an infinite while loop that produces random current temperatures
    while True:
        response = requests.get(url)
        record_key = "Netflix"
        record_value = response.json()
        print("Producing record: {}\t{}".format(record_key, record_value))

        # This will actually send data to your topic
        producer.produce(
            TOPIC,
            key=record_key,
            value=record_value,
            on_delivery=acked,
        )
        producer.poll(0)
        time.sleep(30)

# Interrupt infinite loop when hitting CTRL+C
except KeyboardInterrupt:
    pass
finally:
    producer.flush()  # Finish producing the latest event before stopping the whole script
