import pymysql

def find_popular_description():
	conn = pymysql.connect('localhost', 'root', 'root', 'TwitterAPI')
	#get all the labels and their appear times
	with conn.cursor() as cursor:
		sql = """SELECT label_name as label, COUNT(*) as count FROM LABEL GROUP BY label_name"""
		cursor.execute(sql)
		data = cursor.fetchall()
	conn.close()

	#sort labels by count
	result = sorted(data,key=lambda x:(-x[1],x[0]))

	for item in result:
		print("label",item[0],"appears",item[1],"times")
	popular_count = result[0][1]
	i = 0
	print("the most popular description is:")
	while(result[i][1]==popular_count):
		print(result[i][0])
		i=i+1

def num_of_img_per_feed():
	flag = 1
	session_id = 1
	result = []
	screen = []
	conn = pymysql.connect('localhost', 'root', 'root', 'TwitterAPI')
	while(flag):
		with conn.cursor() as cursor:
			sql = """SELECT img_index FROM LABEL WHERE session_id = %s"""
			cursor.execute(sql,(session_id))
			data = cursor.fetchall()
			if(len(data)>0):
				result.append(max(data))
				with conn.cursor() as cursor:
					sql = """SELECT screen_name FROM SESSION WHERE id = %s"""
					cursor.execute(sql,(session_id))
					screen.append(cursor.fetchall())
			else:
				flag = 0
		session_id = session_id+1
	conn.close()
	for i in range(0, len(result)):
		print("Tweets from ",screen[i][0][0],"has", result[i][0],"images.")

if __name__ == "__main__":
	find_popular_description()
	num_of_img_per_feed()