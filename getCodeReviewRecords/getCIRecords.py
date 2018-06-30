#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
author: andy wu
date:	20180115

depends libs: beautifulsoup4, requests, csv
"""
import requests,sys,io,os,datetime,time, csv
from bs4 import BeautifulSoup
from imp import reload
from getpass import getpass
reload(sys)
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8')

class CIRecord():
	def __init__(self, username, password):
		self.session = requests.Session()
		self.session.verify = False
		self.loginWeb(username, password)
		self.data = []

	def loginWeb(self, username, password):
		loginURL = "http://devws048.be.alcatel-lucent.com:5000/_admin/login?came_from=%2F"
		loginData = {'username':username,
			'password':password,
			'remember':'on',
			'sign_in':'Sign In'
			}

		res = self.session.post(loginURL, data=loginData)
		res.close()
		return res.status_code

	def getCIrecords(self, url):
		response = self.session.get(url=url)
		soup=BeautifulSoup(response.content,'html.parser',from_encoding='utf-8')
		table = soup.findAll(class_='table')[1]
		trs = table.find_all('tr')[1:-1]
		#print(trs)
		print("start to get ci records from lastest week")

		for tr in trs:
			tds = tr.findAll('td')
			ci = {}
			ci['title']  = tds[1].a.text.split('\n')[1].strip()
			ci['author'] = tds[2].text.strip().split("(")[1][0:-1]
			ci['commit'] = tds[3].span['title'].split(' ')[0]
			ci['link']   = "http://devws048.be.alcatel-lucent.com:5000" + tds[1].a['href']
			self.data.append(ci)
			#print("===%s	%s	%s	%s==="%(tds[1].a.text, tds[2].text, tds[3].span['title'], tds[5].a.text))
		response.close()
		return self.data

	def filterData(self, duration):
		itoday = datetime.datetime.today()
		new_ci = []
		for i in self.data:
			delta = itoday - datetime.datetime.strptime(i['commit'], "%Y-%m-%d")
			#print(delta.days)
			if  delta.days <= 7:
				new_ci.append(i)
		return new_ci

	def getReviewers(self, cis):
		for ci in cis:
			reviewer_names = ''
			url = ci['link']
			response = self.session.get(url=url)
			#print(response.status_code)
			soup = BeautifulSoup(response.content, 'html.parser', from_encoding='utf-8')
			reviewers = soup.findAll(class_ = 'reviewers_member')
			for reviewer in reviewers:
				r = reviewer.findAll('span')
				#print(r[1].get_text())
				r = r[1].get_text().split("(")[0].strip()
				reviewer_names = reviewer_names + r + ';'
			ci['reviewer'] = reviewer_names
			response.close()
			#print(type(ci['reviewer']))
		return cis

	def saveData2CSV(self, cis):
		with open('CI_records.csv', 'w', encoding='utf8',newline='') as csvfile:
			fieldnames = ['commit','title', 'author', 'reviewer', 'link']
			writer = csv.DictWriter(csvfile, fieldnames=fieldnames,extrasaction='ignore')

			writer.writeheader()
			for ci in cis:
				writer.writerow({'commit': ci['commit'],
								 'title':  ci['title'],
								 'author': ci['author'],
								 'reviewer':ci['reviewer'],
								 'link':   ci['link']})


if __name__ == "__main__":

	user = input("Your account:")
	passwd = getpass("Your password:")

	#user = 'awu'
	#passwd = 'xxx'

	url =  'http://devws048.be.alcatel-lucent.com:5000/my_pullrequests?closed=1'
	cirecords = CIRecord(user, passwd)
	cis = cirecords.getCIrecords(url)
	# default duration is last 7 days
	cis = cirecords.filterData(duration=7)
	cis = cirecords.getReviewers(cis)
	cirecords.saveData2CSV(cis)
	print("A new CI_results.csv file was created in current dir...")
	time.sleep(6)
	'''
	origin = sys.stdout
	ci_file = open("ci_records.txt","w")
	sys.stdout = ci_file
	print ('commit_time		author				link		title	reviewer')
	for ci in cis:
		print('%-15s %-20s %-50s %-60s %-40s'%(ci['commit'], ci['author'], ci['link'], ci['title'], ci['reviewer']))
	'''



