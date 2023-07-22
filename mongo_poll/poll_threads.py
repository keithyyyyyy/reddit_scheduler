from pymongo import MongoClient, ReturnDocument
import certifi
from dotenv import load_dotenv
load_dotenv()
import os
import boto3
import json

def handler(event, context):
    # mongodb atlas connection
    uri = "mongodb+srv://" + os.getenv("MONGO_USERNAME") + ":" + os.getenv("MONGDO_PASSWORD") + "@reddit.hsttylb.mongodb.net/?retryWrites=true"
    client = MongoClient(uri, tlsCAFile=certifi.where())
    db = client['reddit_data']
    threadsCollection = db['threads']
    # userCollection = db["users"]

    # lambda boto3
    aws_lambda = boto3.client(
        'lambda',
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY"),
        aws_secret_access_key=os.getenv("AWS_SECRET_KEY")
    )

    documents = threadsCollection.find({"status": "pending"})
    for doc in documents:
        # userCollection.find({})
        output = {}
        
        output["type"] = doc["type"]
        output["title"] = doc["title"]
        output["refreshToken"] = doc["refreshToken"]
        output["body"] = doc["body"]
        output["sr"] = doc["sr"]
        output["status"] = doc["status"]
        output["userId"] = doc["userId"]
        
        response = aws_lambda.invoke(
            FunctionName='reddit_scheduler',
            InvocationType='Event',
            Payload=output
        )

print(handler("",""))