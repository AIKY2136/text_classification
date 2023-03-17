import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
from datetime import datetime
import lxml
import pymongo

# Connect to MongoDB

client = pymongo.MongoClient("mongodb+srv://larry1121:AIKY2136@aiky.nu1wkyo.mongodb.net/?retryWrites=true&w=majority")
db = client["AIKY"]
collection = db["news"]

start_date = datetime(2023, 2, 22)
start_date = str(start_date)[:10]

end_date = datetime(2023, 2, 23)
end_date = str(end_date)[:10]

cd_min = start_date[6:7] + '/' + start_date[8:10] + '/' + start_date[:4]
cd_max = end_date[6:7] + '/' + end_date[8:10] + '/' + end_date[:4]

tbs = f'cdr:1,cd_min:{cd_min},cd_max:{cd_max}'

search = 'apple store'
params = {'q': search, 'hl': 'ko', 'tbm': 'nws', 'tbs': tbs}

header = {
  'user-agent':
  'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36'
}
cookie = {'CONSENT': 'YES'}

titles=[]
dates=[]
pag_num=10
for i in range(0, pag_num): # retrieve the first three pages of search results
  params['start'] = i * 10 # set the start parameter to the index of the first result on the current page
  url = 'https://www.google.com/search?' + '&'.join([f'{k}={v}' for k,v in params.items()])
  res = requests.get(url, headers=header, cookies=cookie)
  soup = bs(res.text, 'lxml')

  # Find the relevant HTML elements containing the titles and dates
  news = soup.find_all("div", class_="SoaBEf")
  for new in news:
    title = new.find("div", class_="mCBkyc ynAwRc MBeuO nDgy9d").text
    date = new.find("div", class_="OSrXXb ZE0LJd YsWzw").text
    titles.append(title)
    dates.append(date)
    print(title, date)
  
# Create a Pandas DataFrame from the extracted data
df = pd.DataFrame({"headline": titles, "date": dates})

# Convert DataFrame to dictionary
data_dict = df.to_dict(orient='records')

# Insert data into collection
collection.insert_many(data_dict)
# Print the resulting DataFrame
print(df)
