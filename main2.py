from datetime import datetime
import pandas as pd
import requests
from bs4 import BeautifulSoup

# Link to the BOM Site and details
url = "http://www.bom.gov.au/places/vic/melbourne/forecast/detailed/"
city = "Melbourne"
timestamp = datetime.now()
timestamp = timestamp.strftime('%Y-%m-%d %H:%M:%S')

webpage = requests.get(url)

# insert error handling here
soup = BeautifulSoup(webpage.text, 'html.parser')

#insert error handling here
# Grabs the first table in the url, which is the forecast data
table = soup.find_all('table')[0]

# This part is designed to loop through the table from the URL

loop = 0  # This part is to differentiate between the first and second loops
innerloop = 0

# You could write this as a separate function and call it for each city.
with open('BOM Forecast ' + timestamp + '.csv', 'a', encoding='utf-8-sig') as f:
    for element in table.find_all('tr'):

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
