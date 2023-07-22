from functions import *
import sys
# now = datetime.now().isoformat()
# now = time.time()
# print(now)

def handler(event, context):
    # documents = threadsCollection.find({"status": "pending"})
    # for doc in documents:
    doc = event["doc"]
    try:
        # access_token = getNewAccessToken(doc["refreshToken"])
        # postSent = sendPost(access_token, doc)
        postSent = sendPost(doc["refreshToken"], doc)
        if postSent:
            res = dbLogAndCleanUp(doc["_id"], "completed")
            print(res)
            return "successfully sent"
        else:
            return "not sent, reddit error"
    except (NoAccessTokenException, FailToSendRedditException) as error:
            dbLogAndCleanUp(doc["_id"], "failed")
            return "not sent, error: " + error

print(handler("",""))