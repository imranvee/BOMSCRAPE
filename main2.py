from datetime import datetime
import pandas as pd
import requests
from bs4 import BeautifulSoup

# Link to the BOM Site and details
url = "http://www.bom.gov.au/places/vic/melbourne/forecast/detailed/"  # would need a forloop to loop thorugh all
# of these
city = "Melbourne"  # Would need this to go into the CSV so that each DF will have this as a heading, there is a
# part of this in the write function, would have to be an input might have to call the requests.get as a seperate
# function and the output of this could then go into the table function
timestamp = datetime.now()
timestamp = timestamp.strftime('%Y-%m-%d %H:%M:%S')

errorlist = []
try:
    webpage = requests.get(url)
except requests.ConnectionError:
    error = "No Internetss"
    errorlist.append(error)
    dffault = pd.DataFrame(errorlist, columns=["column"])
    dffault.to_csv('errorlist.csv', index=False)
    exit()  # include date and time in the file name like you did for the normal CSV

# insert error handling here
soup = BeautifulSoup(webpage.text, 'html.parser')

# insert error handling here
# Grabs the first table in the url, which is the forecast data
table = soup.find_all('table')[0]

# This part is designed to loop through the table from the URL

loop = 0  # This part is to differentiate between the first and second loops
innerloop = 0

# You could write this as a separate function and call it for each city.
with open('BOM Forecast ' + timestamp + '.csv', 'a',
          encoding='utf-8-sig') as f:  # would have to move this out of the function
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
