from flask import Flask, render_template, request, send_file
from scrape_linkedin import ProfileScraper
import pandas as pd
from bs4 import BeautifulSoup
import requests
#from gpapi import GimmeProxyApi
import time
import json 
app = Flask(__name__)

def getdata(url):
	headers = {
	"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:70.0) Gecko/20100101 Firefox/70.0"
	}
	r =requests.get(url,headers=headers)
	return r.text

@app.route('/', methods=["POST", "GET"])
def qlinkedin():
	return render_template("linkedin.html")

@app.route('/byurl', methods=["POST"])
def searchbyurl():
	return render_template("searchbyurl.html")

@app.route('/bycp', methods=["POST"])
def searchbycp():
	return render_template("searchbycp.html")

@app.route('/byurlresult', methods=["POST"])
def urlresult():
    name=request.form['url']
    l=[]
    f=open("sample.json", "w")
    new=name.split("in/",1)[1]
    
    with ProfileScraper(cookie='AQEDAS9oddoAec7fAAABcD_bsSwAAAFy_6x9m1EAx95DMXjHJwD-5r2oOCGGAoSFV3WMprqlWBST_FgB77_Lt8DlUPOCXLQJKD10pbNvoW_3sndp1_4OJoU-Os_I2A7ECwpOx1I8rkkf9fF0fiVh_qsd') as scraper:
      profile = scraper.scrape(user=new)
      l.append(profile.to_dict())
    json_object = json.dumps(l, indent = 1) 
    f.write(json_object)
    f.close()
    path='sample.json'
    return send_file(path, as_attachment=True)




@app.route('/cpresult', methods=["POST"])
def cpresult():
    prof=request.form['prof']
    print(';hello')
    nation=request.form['nation']
    n=request.form['number']
    time.sleep(2)
    #n = int(input('Enter the number of results you want\n'))
    i = 0
	#nation = input("Enter the nation: ")
    prof = prof.split()
    prof = '+'.join(prof)
    page = 0
    n=int(n)
    while i<n:
        urls = []
        lurls=[]
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

    ok=lurls[:n]
    d = {"Profile Links": ok}
    df = pd.DataFrame(d)
    return render_template('searchbycp.html', tables=[df.to_html(render_links=True,classes=['table table-striped table-bordered table-hover table-responsive text-white'])])

@app.route('/scrape', methods=["POST"])
def scrape():
    prof=request.form['prof']
    nation=request.form['nation']
    n=request.form['number']
    time.sleep(2)
    #n = int(input('Enter the number of results you want\n'))
    i = 0
	#nation = input("Enter the nation: ")
	#prof = input("Enter the profession: ").split()
    prof = prof.split()
    prof = '+'.join(prof)
    page = 0
    n=int(n)
    while i<n:
        urls = []
        lurls=[]
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

    ok=lurls[:n]
    l=[]
    outfile=open("profile.json", "w")
    for name in ok : 
        new=name.split("in/",1)[1]
        with ProfileScraper(cookie='AQEDAS9oddoAec7fAAABcD_bsSwAAAFy_6x9m1EAx95DMXjHJwD-5r2oOCGGAoSFV3WMprqlWBST_FgB77_Lt8DlUPOCXLQJKD10pbNvoW_3sndp1_4OJoU-Os_I2A7ECwpOx1I8rkkf9fF0fiVh_qsd') as scraper:
            profile = scraper.scrape(user=new)
            l.append(profile.to_dict())
    json_object = json.dumps(l, indent = 1) 
    outfile.write(json_object)
    outfile.close()
    path='profile.json'
    return send_file(path, as_attachment=True)



if __name__ == '__main__':
    app.run()




