class NoAccessTokenException(Exception):
    pass

class FailToSendRedditException(Exception):
    pass

class InvalidPostDetailsException(Exception):
    pass

def basePostDetailsCheck(postDetails):
    errors = ""
    if "type" not in postDetails or len(postDetails["type"].strip()) == 0:
        errors += "type not supplied \n"
    if "sr" not in postDetails or len(postDetails["sr"].strip()) == 0:
        errors += "subreddit not supplied \n"
    
    return errors

def checkPostDetails(postDetails):
    baseCheckErrors = basePostDetailsCheck(postDetails)
    if len(baseCheckErrors) > 0:
        raise InvalidPostDetailsException(baseCheckErrors)
    
    type = postDetails["type"]

    if type == "self":
        if not isinstance(postDetails["body"], str):
            raise InvalidPostDetailsException("'self' post does not have a body of type string")
    elif type == "video" or type == "image":
        if not isinstance(postDetails["body"], list):
            raise InvalidPostDetailsException("'video' or 'image post does not have a body of type list")
    
    if type == "url" and "url" not in postDetails:
        raise InvalidPostDetailsException("No url supplied for type 'url'")
    


