import re
import os
import io
import glob
import shutil
import tweepy #https://github.com/tweepy/tweepy
import numpy as np
import urllib.request
import matplotlib.pyplot as plt
from matplotlib import cm
from google.cloud import vision
from google.cloud import videointelligence
from google.cloud.vision import types

#Twitter API credentials
#consumer_key = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
#consumer_secret = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
#access_key = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
#access_secret = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

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
    #get image urls from alltweets
    tweets=get_all_tweets(screen_name)
    media_files = set()
    for status in tweets:
        try:
            media = status.extended_entities.get('media',[])
            if(len(media) > 0):
                for item in media:
        #           media_files.add(media[0]['media_url'])
                    media_files.add(item['media_url'])
        #    print(media_files)
        except:
            media=status.entities.get('media',[])
            if(len(media)>0):
                media_files.add(media[0]['media_url'])
                #put image urls to set media_files
    return(media_files)


def download_images(screen_name):
    #Download images from urls
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
        #download images
        urllib.request.urlretrieve(url,'./Output/'+screen_name+'/'+image_name+'.jpg')


def convert_to_video(screen_name):
    #convert downloaded images to video with FFMPEG and os.system
    video=os.path.exists('./Output/Video/'+'v'+screen_name+'.mp4')
    if video:
        os.chmod('./Output/Video/'+'v'+screen_name+'.mp4', 0o777)
        os.remove('./Output/Video/'+'v'+screen_name+'.mp4')
    #os.system("ffmpeg -f image2 -r 3 -i Output/"+screen_name+"/img%03d.jpg -vf scale=800:400 Output/Video/"+screen_name+".mp4")
    #os.system("ffmpeg -f image2 -i Output/"+screen_name+"/img%03d.jpg -vf scale=800:400 -vf setpts=2.0*PTS -vcodec libx264 Output/Video/"+screen_name+".mp4")
    os.system("ffmpeg -f image2 -i Output/"+screen_name+"/img%03d.jpg -vf setpts=4.0*PTS -vcodec libx264 Output/Video/"+'v'+screen_name+".mp4")


def analyze_video(screen_name):
    #analyze video contents with google video intelligence api 
    path='./Output/Video/'+'v'+screen_name+'.mp4'
    print("path="+path)
    label=[]
    confidencial=[]
    video_client = videointelligence.VideoIntelligenceServiceClient()
    features = [videointelligence.enums.Feature.LABEL_DETECTION]
    with io.open(path, 'rb') as movie:
        input_content = movie.read()
    operation = video_client.annotate_video(
        features=features, input_content=input_content)
    print('\nProcessing video for label annotations:')
    result = operation.result(timeout=90)
    print('\nFinished processing.')
    # Process shot level label annotations
    shot_labels = result.annotation_results[0].shot_label_annotations
    for i, shot_label in enumerate(shot_labels):
        label.append(shot_label.entity.description)
        for i, shot in enumerate(shot_label.segments):
            start_time = (shot.segment.start_time_offset.seconds +
                          shot.segment.start_time_offset.nanos / 1e9)
            end_time = (shot.segment.end_time_offset.seconds +
                        shot.segment.end_time_offset.nanos / 1e9)
            positions = '{}s to {}s'.format(start_time, end_time)
            position.append(positions)
            confidence = shot.confidence
            print('\tSegment {}: {}'.format(i, positions))
            print('\tConfidence: {}'.format(confidence))
            value=float(confidence)
            confidencial.append(value)
    #plot the confidencial bar with matplotlib
    idx=np.arange(len(confidencial))
    color=cm.jet(np.array(confidencial)/max(confidencial))
    plt.barh(idx,confidencial,color=color)
    plt.yticks(idx+0.4,label)
    plt.grid(axis='confidence')
    plt.show()

def analyze_images(screen_name):
    #analyze images with Google Vision API
    client = vision.ImageAnnotatorClient()
    # The name of the image file to annotate
    WSI_MASK_PATH="./Output/"+screen_name+"/"
    wsi_mask_paths = glob.glob(os.path.join(WSI_MASK_PATH, '*.jpg'))
    wsi_mask_paths.sort()
    #load downloaded images from local file
    for image in wsi_mask_paths:
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
            print(label.description)


if __name__ == '__main__':
    #Set google application credentials
    #Please replace "your credential path" with path or your .json file
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] ='your credential path'
    while(1):
        screen_name=input('Please input a twitter account (example:@realDonaldTrump)')
        #pass in the username of the account you want to download
        print("Downloading...")
        download_images(screen_name)
        print("Converting to video...")
        convert_to_video(screen_name)
        while(1):
            Flag=input("Do u want to see the output video?(y/n)")
            if (Flag=="y"):
                os.system('cd Output/Video && "'+'v'+screen_name+'.mp4')
                analyze_video(screen_name)
                analyze_images(screen_name)
                break
            elif(Flag!="n"):
                print("please input 'y' or 'n'")
            else:
                analyze_video(screen_name)
                analyze_images(screen_name)
                break
        break
            #os.system("'"+screen_name+".mp4")
#ffmpeg -i output5.mp4 -vf "drawtext=text='lihuibin':fontfile=/usr/share/fonts/truetype/ttf-indic-fonts-core/utkal.ttf:fontsize=24:fontcolor=red@0.8:x=w-tw-20:y=h-th-20" -c:v libx264 -c:a copy output8.mp4