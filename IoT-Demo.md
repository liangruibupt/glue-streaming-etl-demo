# glue-streaming-etl-demo

## IoT - Kinesis - Glue Streaming - Athena demo

[Detail guide](https://aws.amazon.com/blogs/aws/new-serverless-streaming-etl-with-aws-glue/)

Archiecture

![serverless-etl-diagram](media/serverless-etl-diagram.png)

# Generate the stream IoT events

1. Create the IoT Thing glue-demo-iot by follow up [IoT Core Getting Start](https://docs.aws.amazon.com/iot/latest/developerguide/iot-gs.html)

2. Put the certificates under iot folder

3. Update the code endpoint and certificates file name
```bash
# Get the IoT endpoint
aws iot describe-endpoint --endpoint-type iot:Data-ATS --region cn-northwest-1
```

4. Install dependency
```bash
pip install -r scripts/requirements.txt
```

5. Run code to send, once per second, a JSON message with sensor data to the `streaming-data` MQTT topic. 
```bash
cd scripts
python scripts/iot-producer.py
```

6. Check the IoT console -> Test, subscribe the `streaming-data` MQTT topic, make sure the message can be print out
```json
{
  "client_id": "raspberrypi",
  "timestamp": "2020-05-26 11:19:14",
  "humidity": 49,
  "temperature": 7,
  "pressure": 450,
  "pitch": "sample",
  "roll": "demo",
  "yaw": "test",
  "count": 39
}
```

# Processing Streaming Data with AWS Glue

1. In the Kinesis console, create the my-data-stream data stream (1 shard is enough). 

2. Back in the AWS IoT console, create an IoT rule to send all data from the MQTT topic to this Kinesis data stream.
