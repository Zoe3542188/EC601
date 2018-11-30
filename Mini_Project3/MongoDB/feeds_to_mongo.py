import tweepy #https://github.com/tweepy/tweepy
import json
import urllib.request
import re
import os
import shutil
import io
import glob
from google.cloud import vision
from google.cloud.vision import types
import pymongo
from pymongo import MongoClient
import datetime
#Twitter API credentials
consumer_key = "OWjpFHd0m3Xv8xDopSupydhHK"
consumer_secret = "bROT7IYeaL7t3GNNUXStGHA3qNsCU45NySBhlCmYozNjWHeWU0"
access_key = "1038144157137739776-uxEgHObDkXDo0OVW2pQz6hn08n2dUW"
access_secret = "StrzYHD0HETNGD55rYMMDlWvZPyTkyjUXgYlf5UJGHtPy"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="C:/Users/lyl5380/EC601/PROJECT3/My First Project-b615fe266883.json"


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
        if(len(alltweets) > 50):
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
    folder=os.path.exists('./Output/'+screen_name)
    if folder:
        os.chmod('./Output/'+screen_name, 0o777)
        shutil.rmtree('./Output/'+screen_name)
    os.makedirs('./Output/'+screen_name)
    #download images to new folder
    count=0
    for url in url_list:
        count=count+1
        identity='%03d' % count
        #transfer to three digits num
        #print(url)
        #identity=str(re.findall(r"http://pbs.twimg.com/media/([^.]+)\.jpg",url))
        #if(len(identity)<=2):
            #identity=str(re.findall(r"img/([^.]+)\.jpg",url))
        image_name="img"+str(identity)
        urllib.request.urlretrieve(url,'./Output/'+screen_name+'/'+image_name+'.jpg')

def analyze_images(screen_name,user_name):
    #initialize MongoDB
    client = MongoClient()
    client = MongoClient("mongodb://localhost:27017")
    mydatabase = client['twitterAPI']
    mycollection = mydatabase['downloads']
    client = vision.ImageAnnotatorClient()
    # The name of the image file to annotate
    WSI_MASK_PATH="./Output/"+screen_name+"/"
    wsi_mask_paths = glob.glob(os.path.join(WSI_MASK_PATH, '*.jpg'))
    wsi_mask_paths.sort()
    img_index = 0
    for image in wsi_mask_paths:
        img_index = img_index + 1
        file_name = os.path.join(
            os.path.dirname(__file__),
            image)
    # Loads the image into memory
        with io.open(file_name, 'rb') as image_file:
            content = image_file.read()
        image = types.Image(content=content)
        # Performs label detection on the image file
        response = client.label_detection(image=image)
        labels = response.label_annotations
        print('Labels for'+file_name+':')
        for label in labels:
            now = datetime.datetime.now()
            #print(label.description)
            record={
            'user_name' : user_name,
            'screen_name' : screen_name,
            'date' : now,
            'label' : label.description,
            'img_index': img_index
            }
            rec = mydatabase.downloads.insert(record)


if __name__ == '__main__':
    user_name = input("what's your username?")
    screen_name=input('Please input a twitter account (example:@realDonaldTrump)')
    print("Downloading feeds images...")
    download_images(screen_name)
    print("Analyzing images...")
    analyze_images(screen_name,user_name)