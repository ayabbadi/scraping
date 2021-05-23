import requests
from bs4 import BeautifulSoup 
import numpy as np
import pandas as pd
from openpyxl.workbook import Workbook



pages = [0, 1, 2, 3]
titles = []
dois = []
dates = []
abstracts = []
authorsx = []


for page in pages:

	base_url = "https://dl.acm.org/action/doSearch?AllField=morocco&startPage={}&ContribAffiliationId=10.1145%2F".format(page)
	endings = ['institution-60019337&pageSize=20', 'institution-60025457&pageSize=20', 'institution-60025506&pageSize=20','institution-60011066&pageSize=20']
	for ending in endings:
		url = base_url + ending
		r = requests.get(url)
		print(url)
		data = BeautifulSoup(r.content, 'html.parser')
		articles = data.find("body").find("ul", attrs={'class': 'items-results'}).find_all('li', attrs={'class': 'search__item issue-item-container'})
		for a in articles:
			title = a.find('h5', attrs={'class': 'issue-item__title'}).find('span').find('a')
			if title:
				titles.append(title.text)
				print(title.text)
			else:
				titles.append(np.nan)
				print(np.nan)
			
			doi = a.find('a', attrs={'class': 'issue-item__doi'})
			if doi:
				dois.append(doi.text)
				print(doi.text)
			else:
				dois.append(np.nan)
				print(np.nan)
			
			date =a.find('span', attrs={'class': 'dot-separator'})
			if date:
				datespan = date.find('span')
				if datespan:
					dates.append(datespan.text)
					print(datespan.text)
				
			else:
				dates.append(np.nan)
				print(np.nan)
			
			abstract=a.find('div', attrs={'class': 'issue-item__abstract'}).find('p')
			if abstract:
				abstracts.append(abstract.text)
				print(abstract.text)
			else:
				abstracts.append(np.nan)
				print(np.nan)
			
			
			authors = []
			auths = a.find('ul', attrs={'aria-label': 'authors'}).find_all('li')
			for auth in auths:
				authors.append(auth.find('span').text)
			authorsx.append(authors)

			print(authors)

print(len(titles))
print(len(dois))
print(len(dates))
print(len(abstracts))
print(len(authorsx))



test_df = pd.DataFrame({
	'Titre' : titles,
	'Doi' : dois,
	'Date' : dates,
	'Abstract' : abstracts,
	'Authors' : authorsx 

})
print(test_df.iloc[ 0 , : ])
test_df.to_json('temp.json', orient='records', lines=True)
print("SAVE TO FILE")


	
test_df.to_csv (r'export_dataframe.csv', index = False, header=True)
writer = pd.ExcelWriter('output.xlsx')
# write dataframe to excel
test_df.to_excel(writer)
# save the excel
writer.save()
print('DataFrame is written successfully to Excel File.')


# Credentials to database connection
"""hostname="localhost"
dbname="scacm"
uname="root"
pwd=""
engine = create_engine("mysql+pymysql://{user}:{pw}@{host}/{db}"
				.format(host=hostname, db=dbname, user=uname, pw=pwd))
test_df.to_sql('articles', engine, index=True)
	
engine = create_engine('mysql+mysqlconnector://root@127.0.0.1:3306/scacm', echo=False)
test_df.to_sql(name='articles', con=engine, if_exists = 'append', index=False , schema='scacm.articles')"""
