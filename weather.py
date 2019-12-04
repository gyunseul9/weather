import os, glob
import requests
from bs4 import BeautifulSoup
import time
import datetime
import sys
from mod_weather import Utilities,Tag
from config import Configuration
from db import DBConnection,Query
from PIL import Image, ImageDraw, ImageFont

class Weather:

	def __init__(self,platform):	
		self.platform = platform

	def set_params(self):	
		self.platform = sys.argv[1]

	def validate(self):
		default	= {
			'platform':'local'
		}

		self.platform = default.get('platform')	if self.platform == '' else self.platform.lower()	

	def make_image(self,mdate,src,key,area,state,temp,dis,rain,hum,wdir,wspeed,hpa):
		
		now = time.localtime()

		name = str(now.tm_year)+str(now.tm_mon)+str(now.tm_mday)+str(now.tm_hour)

		target = Image.open('/home/ubuntu/weather/half.png')

		filename = '/home/ubuntu/images/weather/{}.png'.format(key)		

		fontname = '/usr/share/fonts/truetype/nanum/NanumGothic.ttf'
		fontsize = 15
		width = 600
		height = 400		

		area = '{} 지역 현재날씨'.format(area)

		contents = '출처:{}\n측정일:{}\n상태:{}\n기온: {}\n불쾌지수: {}\n강수량: {}\n습도: {}\n풍향: {}\n풍속: {}\n기압: {}\n'.format(src,mdate,state,temp,dis,rain,hum,wdir,wspeed,hpa)
		
		draw = ImageDraw.Draw(target)

		_area = ImageFont.truetype(fontname, 18)
		draw.text((10,0), area, font=_area, fill=(132,0,165))	

		_contents = ImageFont.truetype(fontname, 15)
		draw.text((10,40), contents, font=_contents, fill='black')

		target.save(filename)	

	def merge_image(self,length):

		now = time.localtime()

		fontname = '/usr/share/fonts/truetype/nanum/NanumGothic.ttf'	

		title = '#낚다 #{}월{}일{}시 #현재날씨'.format(now.tm_mon,now.tm_mday,now.tm_hour)

		folder ='/home/ubuntu/images/weather/'	

		target_image = Image.open('/home/ubuntu/weather/weather.png')

		draw = ImageDraw.Draw(target_image)

		_title = ImageFont.truetype(fontname, 24)
		draw.text((120,30), title, font=_title, fill=(75,0,135))

		for i in range(1,length):

			if i%2 != 0: 

				odd_name = str(i)+'.png'
				even_name = str(i+1)+'.png'

				merge_name = 'merge_'+str(i)+'.png'
				merge_name2 = 'merge_'+str(i+1)+'.png'

				odd_image = Image.open(folder+odd_name)
				even_image = Image.open(folder+even_name)

				odd_width , odd_height = odd_image.size
				even_width , even_height = even_image.size

				target_image.paste(odd_image, (0,100))		

				target_image.save(folder+merge_name)	

				target_image2 = Image.open(folder+merge_name)

				target_image2.paste(even_image, (300,100))	

				target_image2.save(folder+merge_name2)		

	def delete_image(self,length):

		now = time.localtime()

		folder ='/home/ubuntu/images/weather/'

		for i in range(1,length+1):	
			os.remove(folder+str(i)+'.png')

			if i%2 != 0:
				os.remove(folder+'merge_'+str(i)+'.png')

	def rename_image(self,length):
		
		folder ='/home/ubuntu/images/weather/'

		for i in range(1,length+1):
			os.rename(folder+'merge_'+str(i*2)+'.png',folder+'merge_'+str(i)+'.png')							

	def crawling(self):

		self.validate()

		try:
			configuration = Configuration.get_configuration(self.platform)
			_host = configuration['host']
			_user = configuration['user']
			_password = configuration['password']
			_database = configuration['database']
			_port = configuration['port']
			_charset = configuration['charset']

			conn = DBConnection(host=_host,
				user=_user,
				password=_password,
				database=_database,
				port=_port,
				charset=_charset)

			src = '기상청'

			url = 'http://www.weather.go.kr/weather/observation/currentweather.jsp'

			response = requests.get(url)
			html = response.text
			soup = BeautifulSoup(html, 'html.parser')

			location = {
						'1':'강릉',
						'2':'광주',
						'3':'대구',
						'4':'대전',
						'5':'목포',
						'6':'백령도',
						'7':'부산',
						'8':'서울',
						'9':'수원',
						'10':'안동',
						'11':'여수',
						'12':'울산',
						'13':'인천',
						'14':'전주',
						'15':'창원',
						'16':'청주',
						'17':'춘천',
						'18':'포항'
						}

			print('location cnt:',len(location))		

			amount  = Tag.mainpage(soup,0,'amount')

			#print('amount:',amount)

			for i in range(0,int(amount)-1):
 				mdate = Tag.mainpage(soup,i,'mdate')
 				area = Tag.mainpage(soup,i,'area')
 				state = Tag.mainpage(soup,i,'state')
 				temp = Tag.mainpage(soup,i,'temp')
 				dis = Tag.mainpage(soup,i,'dis')
 				rain = Tag.mainpage(soup,i,'rain')
 				hum = Tag.mainpage(soup,i,'hum')
 				wdir = Tag.mainpage(soup,i,'wdir')
 				wspeed = Tag.mainpage(soup,i,'wspeed')
 				hpa = Tag.mainpage(soup,i,'hpa')

 				#print('wspeed',wspeed)

 				for key, val in location.items():

 					if area == val:
 						
 						cnt = conn.exec_select_weather(mdate,area)

 						if cnt:
 							print('overlap seq: ',cnt)
 						else:
 							print('does not overlap seq: ',cnt)
 							conn.exec_insert_weather(mdate,src,area,state,temp,dis,rain,hum,wdir,wspeed,hpa)
 							self.make_image(mdate,src,key,area,state,temp,dis,rain,hum,wdir,wspeed,hpa)
 						
			self.merge_image(len(location))
			self.delete_image(len(location))
			self.rename_image(int(len(location)/2))
		except Exception as e:
			with open('./weather.log','a') as file:
				file.write('{} You got an error: {}\n'.format(datetime.datetime.now().strtime('%Y-%m-%d %H:%M:%S'),str(e)))

def run():
	weather = Weather('')
	weather.set_params()
	weather.crawling()

if __name__ == "__main__":
	run()
