import tweepy #https://github.com/tweepy/tweepy
import json
import urllib.request
import re
import os
import shutil
#Twitter API credentials
consumer_key = "GMvT0Xg24yHqyM9kX3ElE3t8L"
consumer_secret = "apapD1DiWD408tYA0q12SJKi90dCytpNNV9v8qtZlFf6g2SvzD"
access_key = "1038144157137739776-gl3OA88h34HQMELzbfccXA8vQf0ONm"
access_secret = "nAB8Cw4reHbGwCgozq75sfcXZCRloROH2SviYdPDQNfWW"

def get_all_tweets(screen_name):
    #authorize twitter, initialize tweepy
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)
    #initialize a list to hold all the tweepy Tweets
    alltweets = []    
    #make initial request for most recent tweets (200 is the maximum allowed count)
    new_tweets = api.user_timeline(screen_name = screen_name,count=10)
    #save most recent tweets
    alltweets.extend(new_tweets)
    #save the id of the oldest tweet less one
    oldest = alltweets[-1].id - 1
    #keep grabbing tweets until there are no tweets left to grab
    while len(new_tweets) > 0:
        #all subsiquent requests use the max_id param to prevent duplicates
        new_tweets = api.user_timeline(screen_name = screen_name,count=10,max_id=oldest)
        #save most recent tweets
        alltweets.extend(new_tweets)
        #update the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1
        if(len(alltweets) > 15):
            break
    return(alltweets)

def get_image_urls(screen_name):
    tweets=get_all_tweets(screen_name)
    media_files = set()
    for status in tweets:
        try:
            media = status.extended_entities.get('media',[])
            if(len(media) > 0):
                for item in media:
        #            media_files.add(media[0]['media_url'])
                    media_files.add(item['media_url'])
        #    print(media_files)
        except:
            media=status.entities.get('media',[])
            if(len(media)>0):
                media_files.add(media[0]['media_url'])
    return(media_files)

def download_images(screen_name):
    #get image urls
    url_list=get_image_urls(screen_name)
    #creat a new folder
    folder=os.path.exists('./'+screen_name)
    if folder:
        os.chmod('./'+screen_name, 0o777)
        shutil.rmtree('./'+screen_name)
    os.makedirs('./'+screen_name)
    #download images to new folder
    for url in url_list:
        print(url)
        identity=str(re.findall(r"http://pbs.twimg.com/media/([^.]+)\.jpg",url))
        if(len(identity)<=2):
            identity=str(re.findall(r"img/([^.]+)\.jpg",url))
        image_name="img_"+identity
        urllib.request.urlretrieve(url,'./'+screen_name+'/'+image_name+'.jpg')

        if __name__ == '__main__':
    #pass in the username of the account you want to download
    download_images('@realDonaldTrump')