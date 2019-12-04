import pymysql

class DBConnection:
	def __init__(self,host,user,password,database,charset,port):
		self.connection = pymysql.connect(
			host=host,
			user=user,
			password=password,
			db=database,
			charset=charset,
			port=port,
			cursorclass=pymysql.cursors.DictCursor)

	def exec_select_weather(self,mdate,area):
		with self.connection.cursor() as cursor:
			query = Query().get_select_weather(mdate,area)
			cursor.execute(query)
			for row in cursor:
				data = row.get('cnt')
		return data	

	def exec_insert_weather(self,mdate,src,area,state,temp,dis,rain,hum,wdir,wspeed,hpa): 
		query = Query().get_insert_weather(mdate,src,area,state,temp,dis,rain,hum,wdir,wspeed,hpa) 
		with self.connection as cur:
			cur.execute(query)

	def close(self):
		self.connection.close()

	def commit(self):
		self.connection.commit()

class Query:
	def get_select_weather(self,mdate,area):
		query = 'select \
		count(*) as cnt \
		from weather \
		where mdate=\'{}\' and area=\'{}\''.format(mdate,area)

		return query

	def get_insert_weather(self,mdate,src,area,state,temp,dis,rain,hum,wdir,wspeed,hpa):
		query = 'insert into weather (mdate,src,area,state,temp,dis,rain,hum,wdir,wspeed,hpa) \
		values (\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\')'.format(mdate,src,area,state,temp,dis,rain,hum,wdir,wspeed,hpa)

		return query		