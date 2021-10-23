from tkinter.constants import FALSE
import praw
from prawcore.exceptions import OAuthException, ResponseException
import time
import csv
import textwrap

def getredditor(user):
    creds = []
    print('start')
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

def clear(user,delcom,delsub,sublist,listtype,daterange):
    redditor = getredditor(user)
    if delcom == 1:
        for comment in redditor.comments.new():
            if comment.subreddit.display_name in sublist and listtype == 1:
                print("keep" + comment.body)
            elif comment.subreddit.display_name in sublist and listtype == 0 :#or comment.created_utc in daterange and listtype == 1:
                print("Deleted " + comment.body)
            else:
                print("Keep comment" + comment.body)
    if delsub == 1:
        for submission in redditor.submissions.new():
            if submission.subreddit.display_name in sublist and listtype == 1:
                print("keep" + submission.title)
            elif submission.subreddit.display_name in sublist and listtype == 0 :#or submission.created_utc in daterange and listtype == 1:
                print("Deleted " + submission.title)
            else:
                print("Keep comment" + submission.title)

# def choosecontent(user):
#     comments = []
#     redditor = getredditor(user)
#     for comment in redditor.comments.new(limit=None):
#             # if delcom == 1:
#         body = '\n'.join(textwrap.wrap(comment.body,80))
#         temp = [str(comment.subreddit),str(comment.score),"comment"]
#         content = ' - '.join(temp)
#         content = content + '\n'+ body
#         contlist = [content]
#         comments.append(contlist)
#     return comments
    # return comments
            # if comment.subreddit.display_name in sublist and listtype == 1:
            #     content = python
            #     comments.append(content)
            # elif comment.subreddit.display_name in sublist and listtype == 0 :#or comment.created_utc in daterange and listtype == 1:
            #     print("Deleted " + comment.body)
            # else:
            #     print("Keep comment" + comment.body)
    # if delsub == 1:
    #     for submission in redditor.submissions.new():
    #         if submission.subreddit.display_name in sublist and listtype == 1:
    #             print("keep" + submission.title)
    #         elif submission.subreddit.display_name in sublist and listtype == 0 :#or submission.created_utc in daterange and listtype == 1:
    #             print("Deleted " + submission.title)
    #         else:
    #             print("Keep comment" + submission.title)
