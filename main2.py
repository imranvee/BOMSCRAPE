from datetime import datetime
import pandas as pd
import requests
from bs4 import BeautifulSoup


# defining functions

def pageparse(link):
    errorlist = []
    try:
        webpage = requests.get(link)
    except requests.ConnectionError:
        error = "No Internetss"
        errorlist.append(error)
        dffault = pd.DataFrame(errorlist, columns=["column"])
        dffault.to_csv('errorlist.csv', index=False)
        exit()  # include date and time in the file name like you did for the normal CSV

    soup = BeautifulSoup(webpage.text, 'html.parser')
    table = soup.find_all('table')[0]

    return table, soup, errorlist

def tablemaker (table, timestamp, city):

    loop = 0  # This part is to differentiate between the first and second loops
    innerloop = 0
    for element in table.find_all('tr'):  # from here onwards this could go into a separate function (table function)

        chancelist = []

        if loop == 0:
            listheaders = []
            for element2 in element.find_all('th'):
                listheaders.append(element2.text)
            loop = loop + 1
            df = pd.DataFrame(columns=listheaders)

        else:
            for element2 in element.find_all('th'):
                chancelist.append(element2.text)
                for element3 in element.find_all('td'):
                    chancelist.append(element3.text)
                df.loc[len(df), :] = chancelist
    f.write(city + " , " + "logged at: " + timestamp + "\n")
    df.to_csv(f, index=False, encoding='utf-8-sig', mode='a')
    f.write("\n")
    print(df)

    return


# Link to the BOM Site and details
# Putting them into a list

Geo_list = []

url1 = "http://www.bom.gov.au/places/vic/melbourne/forecast/detailed/"
url2 = "http://www.bom.gov.au/places/nsw/sydney/forecast/detailed/"
city1 = "Melbourne"
city2 = "Sydney"

entry = {
            'url': url1,
            'city': city1,
    }
Geo_list.append(entry)

entry = {
            'url' : url2,
            'city': city2
    }
Geo_list.append(entry)


timestamp = datetime.now()
timestamp = timestamp.strftime('%Y-%m-%d %H:%M:%S')

with open('BOM Forecast ' + timestamp + '.csv', 'a',
          encoding='utf-8-sig') as f:

    for item in Geo_list:
        print(item['url'])

        data = pageparse(item['url'])
        table = data[0]
        tablemaker(table,timestamp,item['city'])



