from tkinter.constants import FALSE
import praw
from prawcore.exceptions import OAuthException, ResponseException
import time
import csv
import textwrap

def getredditor(user):
    with open("RedditCredentials.csv",'r') as redditcreds:
        csv_reader = csv.DictReader(redditcreds,delimiter=',',)
        for cred in csv_reader:
            if cred["Username"] == user:
                creds = cred
                break

    reddit = praw.Reddit(client_id=creds['client_id'],
            client_secret=creds['client_secret'],
            password=creds['password'],
            user_agent=creds['user_agent'],
            username=creds['Username'])
    redditor = reddit.redditor(creds['Username'])
    return redditor

def createredditor(credentials):
    print(credentials)
    success = True
    unique = True
    reddit = praw.Reddit(client_id=credentials[0],
            client_secret=credentials[1],
            password=credentials[2],
            user_agent=credentials[3],
            username=credentials[4])
    try:
        reddit.user.me()
        print("User Credentials added")
        
    except ResponseException:
        print("Invalid Credentials")
        success = False
    if success == True:
        with open("RedditCredentials.csv",'r') as creddata:
            csv_reader = csv.DictReader(creddata,delimiter=',')
            for users in csv_reader:
                if credentials[4] == users['Username']:
                    unique = False
        if unique == True:
            with open("RedditCredentials.csv",'a') as creddata:
                # using csv.writer method from CSV package
                write = csv.writer(creddata)
                write.writerow(credentials)
        

    return(success,unique,credentials[4])

def getusers():
    names = []
    with open("RedditCredentials.csv",) as credentials:
        csv_reader = csv.DictReader(credentials,delimiter=',',)
        for users in csv_reader:
            names.append(users['Username'])
    return names

def subfind(user,delcom,delsub):
    redditor = getredditor(user)
    subreddits = []
    if delcom == 1:
        for comment in redditor.comments.new():
            if comment.subreddit.display_name not in subreddits:
                subreddits.append(comment.subreddit.display_name)

    if delsub == 1:
        for submission in redditor.submissions.new():
            if submission.subreddit.display_name not in subreddits:
                subreddits.append(submission.subreddit.display_name)
    return subreddits

def clear(user,sublist,delcom,delsub,listtype,daterange,voterange):
    redditor = getredditor(user)
    if delcom == 1:
        for comment in redditor.comments.new():
            age = (time.time() - comment.created_utc)/86400
            score = comment.score
            insubs = comment.subreddit.display_name in sublist
            content = comment.subreddit.display_name
            clearit(age,score,insubs,content,listtype,daterange,voterange)

    if delsub == 1:
        for submission in redditor.submissions.new():
            age = (time.time() - submission.created_utc)/86400
            score = submission.score
            insubs = submission.subreddit.display_name in sublist
            content = submission.title
            clearit(age,score,insubs,content,listtype,daterange,voterange)

def clearit(age,score,insubs,content,listtype,voterange,daterange):
    print(age)
    print(score)
    if insubs and listtype == 1:            
        print("delete" + content)
    elif insubs and listtype == 0 or daterange[0] < age or daterange[1] > age \
        or voterange[0] > score or voterange[1] < score or listtype == 1:
        print("keep" + content)
    else:
        print("delete" + content)
    time.sleep(1)