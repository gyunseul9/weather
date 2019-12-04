import re
import time
import urllib.request
import os
from datetime import datetime

class Tag:

	def mainpage(soup,i,keyword):

		content_weather = soup.find('div',{'id':'content_weather'})

		if keyword == 'amount':
			table_develop3 = content_weather.find('table',{'class':'table_develop3'}) 
			tbody = table_develop3.find('tbody')
			amount = tbody.find_all('tr')
			value = len(amount)

		if keyword == 'mdate': #측정일
			table_topinfo = content_weather.find('p',{'class':'table_topinfo'}) 
			mdate = Utilities.remove_strong_tag(table_topinfo)
			mdate = Utilities.remove_all_tag(mdate)
			value = mdate

		elif keyword == 'area': #지역
			table_develop3 = content_weather.find('table',{'class':'table_develop3'}) 
			tbody = table_develop3.find('tbody')
			tr = tbody.find_all('tr')
			td = tr[i].find_all('td')
			area = td[0].get_text().strip()
			value = area	

		elif keyword == 'state': #현재일기
			table_develop3 = content_weather.find('table',{'class':'table_develop3'}) 
			tbody = table_develop3.find('tbody')
			tr = tbody.find_all('tr')
			td = tr[i].find_all('td')
			state = td[1].get_text().strip()
			value = state	

		elif keyword == 'temp':
			table_develop3 = content_weather.find('table',{'class':'table_develop3'}) 
			tbody = table_develop3.find('tbody')
			tr = tbody.find_all('tr')
			td = tr[i].find_all('td')
			temp = td[5].get_text().strip()
			value = temp	

		elif keyword == 'dis':
			table_develop3 = content_weather.find('table',{'class':'table_develop3'}) 
			tbody = table_develop3.find('tbody')
			tr = tbody.find_all('tr')
			td = tr[i].find_all('td')
			dis = td[7].get_text().strip()
			value = dis	

		elif keyword == 'rain': #일강수
			table_develop3 = content_weather.find('table',{'class':'table_develop3'}) 
			tbody = table_develop3.find('tbody')
			tr = tbody.find_all('tr')
			td = tr[i].find_all('td')
			rain = td[8].get_text().strip()
			value = rain

		elif keyword == 'hum': #습도
			table_develop3 = content_weather.find('table',{'class':'table_develop3'}) 
			tbody = table_develop3.find('tbody')
			tr = tbody.find_all('tr')
			td = tr[i].find_all('td')
			hum = td[10].get_text().strip()
			value = hum		

		elif keyword == 'wdir': #풍향
			table_develop3 = content_weather.find('table',{'class':'table_develop3'}) 
			tbody = table_develop3.find('tbody')
			tr = tbody.find_all('tr')
			td = tr[i].find_all('td')
			wdir = td[11].get_text().strip()
			value = wdir																		
		
		elif keyword == 'wspeed': #풍속
			table_develop3 = content_weather.find('table',{'class':'table_develop3'}) 
			tbody = table_develop3.find('tbody')
			tr = tbody.find_all('tr')
			td = tr[i].find_all('td')
			tmp = td[12].get_text().strip()
			tmp2 = Utilities.tokenize(tmp,'\'')
			try:
				wspeed = round(float(tmp2[1])*3.6,2)
			except ValueError:
				wspeed = '-'
			value = wspeed

		elif keyword == 'hpa': #기압
			table_develop3 = content_weather.find('table',{'class':'table_develop3'}) 
			tbody = table_develop3.find('tbody')
			tr = tbody.find_all('tr')
			td = tr[i].find_all('td')
			hpa = td[13].get_text().strip()
			value = hpa		

		return value

class Utilities:

	def remove_strong_tag(string):
		string = re.sub('<strong.*?>.*?</strong>', '', str(string), 0, re.I|re.S)
		return string	

	def remove_all_tag(string):
		string = re.sub('<[^<]+?>', '', string)
		return string

	def remove_keyword(string):
		string = string.replace('\'', '')
		return string		

	def tokenize(string, token):
		arr = []
		arr = string.split(token)
		return arr	
