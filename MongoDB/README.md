## [MongoDB](https://github.com/Zoe3542188/EC601/tree/Mini_Project_3/MongoDB)
#### Using [pymongo](https://github.com/mongodb/mongo-python-driver) to build connection between Python and MongoDB
#### Using [Robo 3T](https://robomongo.org/) to visualize the database
#### My database structure:
![database](https://raw.githubusercontent.com/Zoe3542188/EC601/screenshots/DBstructureMongo.PNG)
### One collection: </br>
- id: default id (query id)
- user_name: user who create the query session
- screen_name: Twitter account name
- date: the time when the session was created
- img_index: img index in each feed
- label: description

#### Result:
### [feeds_to_mongo.py]()
- Dwonloads images and load info to database

### [search.py]()
- input the label name and get info from the database</br>
![result](https://raw.githubusercontent.com/Zoe3542188/EC601/screenshots/SearchMongo.PNG)

### [statistic.py]()
- get statistic data from database(the most popular description and img nums for each feed)</br>
![imgnums](https://raw.githubusercontent.com/Zoe3542188/EC601/screenshots/statistic1Mongo.PNG)</br>
![popular](https://raw.githubusercontent.com/Zoe3542188/EC601/screenshots/statistic2Mongo.PNG)
