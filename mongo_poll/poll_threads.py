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
    threads_db = client['reddit_data']
    threadsCollection = threads_db['threads']
    usersCollection = client["users"]["accounts"]

    # lambda boto3
    aws_lambda = boto3.client(
        'lambda',
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY"),
        aws_secret_access_key=os.getenv("AWS_SECRET_KEY")
    )

    documents = threadsCollection.find({"status": "pending"})
    for doc in documents:
        refresh_token = ""
        user = usersCollection.find({"providerAccountId": doc["userId"]})
        for u in user:
            refresh_token = u["refresh_token"]
        
        output = {}
        output["type"] = doc["type"]
        output["title"] = doc["title"]
        output["refreshToken"] = refresh_token
        output["body"] = doc["body"]
        output["sr"] = doc["sr"]
        output["status"] = doc["status"]
        output["userId"] = doc["userId"]
        
        print(output)
        print( "\n\n")
        # response = aws_lambda.invoke(
        #     FunctionName='reddit_scheduler',
        #     InvocationType='Event',
        #     Payload=output
        # )

print(handler("",""))