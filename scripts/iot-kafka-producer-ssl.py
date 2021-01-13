import time
import datetime
import json
import sys
import random
from awscrt import io, mqtt, auth, http
from awsiot import mqtt_connection_builder
from kafka import KafkaProducer, KafkaConsumer

topic = "streaming-data"
client_id = "raspberrypi"

def collect_and_send_data():
    publish_count = 0
    while(True):

        humidity = random.randint(0,120)
        print("Humidity: %s H" % humidity)

        temp = random.randint(0,60)
        print("Temperature: %s C" % temp)

        pressure = random.randint(0,1600)
        print("Pressure: %s Millibars" % pressure)

        orientation = {"pitch":"sample", "roll":"demo", "yaw":"test"}
        print("p: {pitch}, r: {roll}, y: {yaw}".format(**orientation))

        timestamp = datetime.datetime.fromtimestamp(
            time.time()).strftime('%Y-%m-%d %H:%M:%S')

        message = {
            "client_id": client_id,
            "timestamp": timestamp,
            "humidity": humidity,
            "temperature": temp,
            "pressure": pressure,
            "pitch": orientation['pitch'],
            "roll": orientation['roll'],
            "yaw": orientation['yaw'],
            "count": publish_count
        }
        print("Publishing message to topic '{}': {}".format(topic, message))
        
        kafka_producer(message)
        
        time.sleep(1)
        publish_count += 1

def kafka_producer(message):
    consumer = KafkaConsumer(bootstrap_servers='ip-172-31-33-0.cn-north-1.compute.internal:9094',
                            security_protocol='SSL',
                            ssl_check_hostname=False,
                            ssl_cafile='/home/ec2-user/kafka/ssl/private/CARoot.pem',
                            ssl_certfile='/home/ec2-user/kafka/ssl/private/certificate.pem',
                            ssl_keyfile='/home/ec2-user/kafka/ssl/private/key.pem',
                            ssl_password='Password')

    producer = KafkaProducer(bootstrap_servers='ip-172-31-33-0.cn-north-1.compute.internal:9094',
                            value_serializer=lambda m: json.dumps(m).encode('utf-8'), 
                            security_protocol='SSL',
                            ssl_check_hostname=False,
                            ssl_cafile='/home/ec2-user/kafka/ssl/private/CARoot.pem',
                            ssl_certfile='/home/ec2-user/kafka/ssl/private/certificate.pem',
                            ssl_keyfile='/home/ec2-user/kafka/ssl/private/key.pem',
                            ssl_password='Password')
    
    future = producer.send('AWSKafkaTutorialTopic' ,  value= message, partition= 0)
    future.get(timeout= 10)
        
    

if __name__ == '__main__':
    collect_and_send_data()
