## Mini_Project_3
#### Database Project

### [MySQL](https://github.com/Zoe3542188/EC601/tree/Mini_Project_3/MySQL)
#### Using [pymysql](https://github.com/PyMySQL/PyMySQL) to build connection between Python and MySQL
#### My database structure:
![database](https://raw.githubusercontent.com/Zoe3542188/EC601/blob/screenshots/DBstructure.PNG)
> Two tables: 
>> 1. Session table:
![session](https://raw.githubusercontent.com/Zoe3542188/EC601/blob/screenshots/Session.PNG)
- id: default id (query id)
- user_name: user who create the query session
- screen_name: Twitter account name
- session_time: the time when the session was created
>> 2. Label tabel:
![label](https://raw.githubusercontent.com/Zoe3542188/EC601/screenshots/label.PNG)
- id: default id
- session_id: search session id
- img_index: img index in each feed
- label_name: description

#### Result:
## [FeedsToMysql.py](https://github.com/Zoe3542188/EC601/tree/Mini_Project_3/MySQL/FeedsToMysql.py)
- Dwonloads images and load info to database

## [search.py](https://github.com/Zoe3542188/EC601/tree/Mini_Project_3/MySQL/search.py)
- input the label name and get info from the database
![result](https://raw.githubusercontent.com/Zoe3542188/EC601/screenshots/search.PNG)
## [statistic.py](https://github.com/Zoe3542188/EC601/tree/Mini_Project_3/MySQL/statistic.py)
- get statistic data from database(the most popular description and img nums for each feed)
![imgnums](https://raw.githubusercontent.com/Zoe3542188/EC601/screenshots/statistic1.PNG)
![popular](https://raw.githubusercontent.com/Zoe3542188/EC601/screenshots/statistic2.PNG)

### [MongoDB](https://github.com/Zoe3542188/EC601/tree/Mini_Project_3/MongoDB)