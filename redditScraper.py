import requests
import json

TITLE = 'title'
AUTHOR = 'author'
TIMESTAMP = 'time'
COMMENT_COUNT = 'comment_count'
POSTS_NUM = 100

def getToken():
    token_recv_url = "https://www.reddit.com/auth/v2/oauth/access-token/loid"
    tokenHeaders = {"Client-Vendor-ID" : "7bfddb97-7bfa-41e5-8643-6b390ba815ea", 'Authorization' : "Basic b2hYcG9xclpZdWIxa2c6", 'Content-Type' : "application/x-www-form-urlencoded"}
    tokenData = {'scopes' : ["*", "email", "pii"]}
    response = requests.post(token_recv_url, headers=tokenHeaders, data=json.dumps(tokenData))
    tokenDetails = json.loads(response.content.decode())
    return tokenDetails['token_type'] + ' ' + tokenDetails['access_token']

if __name__ == '__main__':
    requestData = {
    "operationName": "SubredditFeedElements",
    "variables": {
        "subredditName": "interesting",
        "sort": "HOT",
        "adContext": {
            "distance": None,
            "layout": "CARD",
            "deviceAdId": "f6d43140-6ec8-4dfb-9f2f-1041e729bc2a",
            "clientSignalSessionData": {
                "adsSeenCount": 12,
                "totalPostsSeenCount": 144,
                "sessionStartTime": "2024-10-09T09:24:57.631Z"
            }
        },
        "forceAds": {},
        "feedFilters": {},
        "optedIn": True,
        "includeSubredditInPosts": False,
        "includeAwards": True,
        "feedContext": {
            "experimentOverrides": []
        },
        "includePostStats": True,
        "includeCurrentUserAwards": False,
        "includeQueryOptimizations": True,
        "includeStillMediaAltText": True,
        "includeMediaAuth": False
    },
    "extensions": {
        "persistedQuery": {
            "version": 1,
            "sha256Hash": "ef8fd6f295afd8df1787ed998c53b40422e87417065fc275bfcae9e938e576bf"
        }
    }
}

    hdr = {"__temp_suppress_gql_request_latency_seconds": "true",
            'Authorization': getToken()}

    subredditName = input("Please enter name of subreddit\nr/")
    requestData['variables']['subredditName']= subredditName
    response = requests.post("https://gql-fed.reddit.com/",json=requestData,headers=hdr)
    fullResponse = json.loads(response.content.decode())
    if fullResponse['data']['postFeed'] == None:
        print("Subreddit does not exist!")
        input("Press enter to finish")
    elif fullResponse['data']['postFeed']['__typename'] == 'UnavailableSubreddit':
        print("Unavailable subreddit!")
        input("Press enter to finish")
    else:
        postList = []
        count = 0
        while count < POSTS_NUM:
            posts = fullResponse['data']['postFeed']['elements']['edges']
            for post in posts:
                post = post['node']
                if post['__typename'] == "SubredditPost":
                    count += 1
                    postDetails = {TITLE : post['title'], AUTHOR : post['authorInfo']['name'], COMMENT_COUNT : post['commentCount'], TIMESTAMP : post['createdAt']}
                    postList.append(postDetails)
            pageInfo = fullResponse['data']['postFeed']['elements']['pageInfo']
            if pageInfo['hasNextPage'] == False:
                break
            requestData['variables']['after'] = pageInfo['endCursor']
            response = requests.post("https://gql-fed.reddit.com/",json=requestData,headers=hdr)
            fullResponse = json.loads(response.content.decode())
        for post in postList:
            print(post)
            print()
        print("shown " + f"{count}" + " posts")
        input("Press enter to finish")

