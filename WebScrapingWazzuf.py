import requests
from bs4 import BeautifulSoup
import csv
from itertools import zip_longest

jobs = []
companies = []
locations = []
skills = []
links = []
reqs = []
dates = []

result = requests.get("https://wuzzuf.net/search/jobs/?q=python&a=hpb")
src = result.content
soup = BeautifulSoup(src , "lxml")

#-- Job Title
job_title = soup.find_all("h2",{"class":"css-m604qf"}) 
#-- Company Name
company_name = soup.find_all("a" , {"class":"css-17s97q8"})
#-- Location
location_name = soup.find_all("span",{"class":"css-5wys0k"})
#-- Job Skills
job_skills = soup.find_all("div", {"class":"css-y4udm8"})
#-- Date 
date_new = soup.find_all("div",{"class":"css-4c4ojb"})
date_old = soup.find_all("div",{"class":"css-do6t5g"})

date_ = [*date_old , *date_new]

for i in range(len(job_title)):
	jobs.append(job_title[i].text)
	links.append(job_title[i].find("a").attrs['href'])   ## For Links
	companies.append(company_name[i].text)
	locations.append(location_name[i].text)
	skills.append(job_skills[i].text)
	dates.append(date_[i].text)

for link in links:
	R_link = requests.get(link)
	src_link = R_link.content
	soup_link = BeautifulSoup(src_link , "lxml")
	req = soup_link.find("div" , {"class":"css-1t5f0fr"}).ul.find_all("li")
	respo_text = ""
	for li in req:
		respo_text += li.text+"|| "
	respo_text = respo_text[:-3]
	reqs.append(respo_text)
	
	



file_list = [jobs , companies , locations , skills , links ,reqs , dates ]
exported = zip_longest(*file_list) # (*) unpacking 

with open("C:\\Users\\Sami\\Desktop\\webScraping\\result.csv","w") as myFile:
	wr = csv.writer(myFile)
	wr.writerow(["Jobe Title" , "Company Name","Location","Skills" , "Links" , "Requirments" , "Date"])
	wr.writerows(exported)

