from pymongo import MongoClient, ReturnDocument
import argparse
import subprocess
from functions import *



    # subprocess.call(["python3", "reddit_scheduler.py " + doc])
    data = str(doc)
    data = data.replace("\'", "\"")
    print(data)
    print(type(json.loads(data)))