from bs4 import BeautifulSoup
import requests
import json

def getSkin(id):

    request = requests.get("https://csgostash.com/skin/"+str(id))

    if request.status_code != 200:
        return None
    
    soup = BeautifulSoup(request.text, 'html.parser')

    name = soup.find('h2').text

    try:
        collection = soup.find('p',class_="collection-text-label").text
    except:
        collection = "Not Applicable"

    price_data = str(soup.find_all('div',id="prices"))

    newsoup = BeautifulSoup(price_data, 'html.parser')

    wears = newsoup.find_all('span',class_="pull-left")
    prices = newsoup.find_all('span',class_="pull-right")

    skinData = {}
    wearList = []
    prevStat = False
    wearToAdd = 0

    skinData['Name'] = name
    skinData['Collection'] = collection
    
    for wear in wears:
        
        if wear.text == "StatTrak":
            prevStat = True
        else:
            if prevStat:
                wearList.append("StatTrak " + wear.text)
                
            else:
                wearList.append(wear.text)
                
            prevStat = False

    i = 0

    for price in prices:

        skinData[wearList[i]] = price.text
        
        i += 1


    return skinData


skins = []
for index in range(7,1601):
    toAppend = getSkin(index)
    if toAppend != None:
        print("Fetched skin " + str(index))
        skins.append(toAppend)

with open('skins.json','w',encoding='utf8') as json_file:
    json.dump(skins, json_file,indent=4)
    

