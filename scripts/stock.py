import json
import boto3
import random
import datetime

kinesis = boto3.client('kinesis')


def getReferrer(count):
    data = {}
    now = datetime.datetime.now()
    str_now = now.isoformat()
    data['EVENT_TIME'] = str_now
    data['TICKER'] = random.choice(['AAPL', 'AMZN', 'MSFT', 'INTC', 'TBV'])
    price = random.random() * 100
    data['PRICE'] = round(price, 2)
    data['ID'] = count
    return data


count = 0
while True:
    data = json.dumps(getReferrer(count))
    count += 1
    print(data)
    kinesis.put_record(
        StreamName="ExampleInputStream",
        Data=data,
        PartitionKey="partitionkey")
