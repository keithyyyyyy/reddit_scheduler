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
            return doc["_id"] + " failed " + str(error)

# print(handler({"doc": {"_id": "64bb6d9c375a1989bed55a0c", "type": "image", "title": "test", "refreshToken": "66371868-uUzLql17BztWiDaGB51g3uyg3j1jlw", "body": ["2546d527-5e4e-4888-8206-a9bf1c4555d8-cat.jpg"], "sr": "sandboxtest", "status": "pending", "userId": "13ikv0"}},""))