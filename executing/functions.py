from importModules import *
from errors import *

# mongodb atlas connection
uri = "mongodb+srv://" + os.getenv("MONGO_USERNAME") + ":" + os.getenv("MONGDO_PASSWORD") + "@reddit.hsttylb.mongodb.net/?retryWrites=true"
client = MongoClient(uri, tlsCAFile=certifi.where())
db = client['reddit_data']
threadsCollection = db['threads']

# boto3
s3 = boto3.client(
    's3',
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY"),
    aws_secret_access_key=os.getenv("AWS_SECRET_KEY")
)

def getNewAccessToken(refreshToken):
    res = requests.post(
        "https://www.reddit.com/api/v1/access_token?grant_type=refresh_token&refresh_token=" + refreshToken,
        headers={
            "Accept": "*/*",
            "Authorization" : "Basic " + os.getenv("APP_AUTHORIZATION"),
            "User-Agent": "Thunder Client (https://www.thunderclient.com)"
        }
    )
    res = res.json()
    if "access_token" not in res:
        raise NoAccessTokenException("error from Reddit: ", res["message"])
    return res["access_token"]

def downloadFromS3(media):
    s3.download_file(
        "reddit-integrator-frontend-site-bucketd7feb781-1jm0vvmt28ka1",
        media,
        'tmp/'+ media
    )

def authReddit(refreshToken):
    reddit = praw.Reddit(
        client_id=os.getenv("REDDIT_CLIENT_ID"),
        client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
        refresh_token=refreshToken,
        user_agent="Thunder Client (https://www.thunderclient.com)",
    )
    return reddit

def prawsendImages(media_arr, reddit, doc):
    subreddit = reddit.subreddit(doc["sr"])
    try:
        if (len(media_arr) == 1):
            submission = subreddit.submit_image(
            title=doc["title"],
            image_path=str(media_arr[0]["image_path"]),
            without_websockets = True
        )
        else:
            submission = subreddit.submit_gallery(
                title=doc["title"],
                images=media_arr
            )
        return "image(s) successfully sent"
    except:
        return "an error occured sending image(s)"

def prawSendVideo(video_filepath, reddit, doc):
    subreddit = reddit.subreddit(doc["sr"])
    submission = subreddit.submit_video(
        title=doc["title"],
        video_path=video_filepath,
        without_websockets=True
    )

def sendPost(refreshToken, doc):
    try:
        checkPostDetails(doc)
        reddit = authReddit(refreshToken)

        type = doc["type"]
        if type == 'text':
            type = "self"

        if type == "self":
            # params["text"] = doc["body"]
            pass
        else:
            if type == "video":
                video_filename = doc["body"][0]
                downloadFromS3(video_filename)
                prawSendVideo("tmp/"+video_filename, reddit, doc)
            if type == "image":
                media_arr = []
                for media in doc["body"]:
                    media_arr.append({"image_path": "tmp/"+media})
                    downloadFromS3(media)
                prawsendImages(media_arr, reddit, doc)

        return True
    
    except (InvalidPostDetailsException, FailToSendRedditException) as error:
        raise FailToSendRedditException(error)
        return False

def dbLogAndCleanUp(docID, newStatus):
    result = threadsCollection.find_one_and_update(
        {'_id': ObjectId(docID)}, 
        { '$set': { 'status': newStatus } }
    )
    print(result)
    
    return "process completed for", str(docID)