from bs4 import BeautifulSoup
import requests
import pandas as pd
from gpapi import GimmeProxyApi
import time


lurls = []

api = GimmeProxyApi() # initiate the class (you can pass an apikey if you have one)
random_proxy = api.get_proxy()
proxies = {str(random_proxy['type']):str(random_proxy['curl'])}

def getdata(url):
	headers = {
	"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:70.0) Gecko/20100101 Firefox/70.0"
	}
	r = requests.get(url,proxies=proxies,headers=headers)
	return r.text

time.sleep(2)

if __name__=="__main__":

	n = int(input('Enter the number of results you want\n'))
	i = 0
	nation = input("Enter the nation: ")
	prof = input("Enter the profession: ").split()
	prof = '+'.join(prof)
	page = 0
	while i<n:
		urls = []
		data = getdata(f"https://www.google.co.in/search?start={page}&q=site:linkedin.com/in/%20AND%20%22{prof}%22%20AND%20{nation}")
		if page==0:
			print(f"https://www.google.co.in/search?start={page}&q=site:linkedin.com/in/%20AND%20%22{prof}%22%20AND%20{nation}")
		soup = BeautifulSoup(data, "lxml")
		# print(soup.prettify())
		links = soup.find_all("a", attrs={"data-uch": "1"})
		for link in links:
			urls.append(link['href'][7:])
		for u in urls:
			l = u.split("&")
			lurls.append(l[0])
		i = len(lurls)
		page+=1

	print(lurls[:n])
