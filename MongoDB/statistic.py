import pymongo
from pymongo import MongoClient
#initialize MongoDB
client = MongoClient()
client = MongoClient("mongodb://localhost:27017")
mydatabase = client['twitterAPI']
mycollection = mydatabase['downloads']
count = []
label = []
result = []
screen = []
img_count = []

#get distinct labels
for item in mydatabase.downloads.find().distinct('label'):
	label.append(item)
#count labels
for i in range(0, len(label)):
	temp = mydatabase.downloads.count({'label':label[i]})
	count.append(temp)
for i in range(0, len(label)):
	result.append([count[i],label[i]])
result = sorted(result,reverse = True)
for i in range(0, len(result)):
	print("label",result[i][1],"appears",result[i][0],"times")

#find popular
popular_count = result[0][0]
t = 0
print("the most popular description is:")
while(result[t][0] == popular_count):
	print(result[t][1])
	t = t + 1


#get distinct screen names
for item in mydatabase.downloads.find().distinct('screen_name'):
	screen.append(item)
#count images
for i in range(0,len(screen)):
	temp = mydatabase.downloads.count({'screen_name':screen[i]})
	img_count.append(temp)
for i in range(0,len(screen)):
	print("Tweets from ",screen[i]," has ",img_count[i]," images.")
