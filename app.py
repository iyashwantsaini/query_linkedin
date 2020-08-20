from flask import Flask, render_template, request, send_file
from query_lib.ProfileScraper import ProfileScraper
import pandas as pd
from bs4 import BeautifulSoup
import requests
#from gpapi import GimmeProxyApi
import json 
app = Flask(__name__)

my_cook='AQEDARp9aBMDsTpCAAABdAsxhSIAAAF0Lz4JIk4AfYbewgSlKOpeSBE2aVmA5jx1IvylHf5IxZlRrsUGheUMWpRssg4udUEBThh4mx_JDxaSKAaZkpDca6D0rsRk4Gyn_4O206j1X3QYhcyyeR6schgY'

def getdata(url):
	headers = {
    	"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:70.0) Gecko/20100101 Firefox/70.0"
	}
	return requests.get(url,headers=headers).text

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
    
    with ProfileScraper(cookie=my_cook) as scraper:
      profile = scraper.scrape(user=new)
      l.append(profile.to_dict())
    json_object = json.dumps(l, indent = 1) 
    f.write(json_object)
    f.close()
    path='sample.json'
    return send_file(path, as_attachment=True)




@app.route('/cpresult', methods=["POST"])
def cpresult():
    urls = set()
    prof=request.form['prof']
    print(';hello')
    nation=request.form['nation']
    n=request.form['number']
    n=int(n)
    #time.sleep(2)
    #n = int(input('Enter the number of results you want\n'))
    i = 0
	#nation = input("Enter the nation: ")
    prof = prof.split()
    prof = '+'.join(prof)
    page = 0
    while 1:
		# urls = []
         x,y = 0,0
         data = getdata(f"https://www.bing.com/search?q=site%3alinkedin.com%2fin%2f+AND+%22{prof}%22+AND+{nation}&sp=-1&pq=site%3alinkedin.com%2fin%2f+and+%22{prof}%22+and+{nation}&sc=1-52&qs=n&sk=&cvid=B8AD94293F0C48109178B93CC18447EB&first={10*page+1}")
         soup = BeautifulSoup(data, "lxml")
         if page==0:
             x = soup.prettify()
         else:
            y = soup.prettify()
         links = soup.find_all("li",{"class":"b_algo"})
         for link in links:
            urls.add(link.h2.a.get('href'))
		#print(urls[i:])
         i = len(urls)
         if i>=n:
             break
         page+=1

    urls = list(urls)
    d = {"Profile Links": urls}
    df = pd.DataFrame(d)
    return render_template('searchbycp.html', tables=[df.to_html(render_links=True,classes=['table table-striped table-bordered table-hover table-responsive text-white'])])

@app.route('/scrape', methods=["POST"])
def scrape():
    print('hello and ok')
    urls = set()
    print('2')
    prof=request.form['prof']
    print('helllllllooooo')
    nation=request.form['nation']
    n=request.form['number']
    print('1')
    n=int(n)
    #time.sleep(2)
    #n = int(input('Enter the number of results you want\n'))
    i = 0
	#nation = input("Enter the nation: ")
    prof = prof.split()
    prof = '+'.join(prof)
    page = 0
    while 1:
		# urls = []
         x,y = 0,0
         data = getdata(f"https://www.bing.com/search?q=site%3alinkedin.com%2fin%2f+AND+%22{prof}%22+AND+{nation}&sp=-1&pq=site%3alinkedin.com%2fin%2f+and+%22{prof}%22+and+{nation}&sc=1-52&qs=n&sk=&cvid=B8AD94293F0C48109178B93CC18447EB&first={10*page+1}")
         soup = BeautifulSoup(data, "lxml")
         if page==0:
             x = soup.prettify()
         else:
            y = soup.prettify()
         links = soup.find_all("li",{"class":"b_algo"})
         for link in links:
            urls.add(link.h2.a.get('href'))
		#print(urls[i:])
         i = len(urls)
         if i>=n:
             break
         page+=1

    urls = list(urls)
    print(urls)
    #ok=lurls[:n]
    l=[]
    outfile=open("profile.json", "w")
    for name in urls : 
        new=name.split("in/",1)[1]
	
        with ProfileScraper(cookie=my_cook) as scraper:
            profile = scraper.scrape(user=new)
            l.append(profile.to_dict())
    json_object = json.dumps(l, indent = 1) 
    outfile.write(json_object)
    outfile.close()
    path='profile.json'
    return send_file(path, as_attachment=True)



if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=5000, debug=True)
    app.run(debug=True)

