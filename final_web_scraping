#importing libraries 

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from time import sleep , time
import requests
from bs4 import BeautifulSoup 

start = time()



#URLs

main_url = "https://coinmarketcap.com"
url = "https://coinmarketcap.com/historical/20230825"


driver = webdriver.Firefox()
driver.get(url)
sleep(5)

table = driver.find_element(By.XPATH ,'/html/body/div[1]/div[2]/div[2]/div/div[1]/div[3]/div[1]/div[3]/div/table/tbody')

k = 1

coins = list()

for i in range(20):
    for j in range(10):
        rank = table.find_element(By.XPATH ,'/html/body/div[1]/div[2]/div[2]/div/div[1]/div[3]/div[1]/div[3]/div/table/tbody/tr[%s]/td[1]'%(k))
        name = table.find_element(By.XPATH ,'/html/body/div[1]/div[2]/div[2]/div/div[1]/div[3]/div[1]/div[3]/div/table/tbody/tr[%s]/td[2]'%(k))
        symbol = table.find_element(By.XPATH ,'/html/body/div[1]/div[2]/div[2]/div/div[1]/div[3]/div[1]/div[3]/div/table/tbody/tr[%s]/td[3]'%(k))
        mainlink = table.find_element(By.XPATH ,'/html/body/div[1]/div[2]/div[2]/div/div[1]/div[3]/div[1]/div[3]/div/table/tbody/tr[%s]/td[2]/div/a[2]'%(k)).get_attribute('href')
        historical_link = mainlink + 'historical-data/'
        coins.append([rank.text , name.text , symbol.text , mainlink , historical_link ])
        k+=1
    
    #scroll down the page to load data
    
    scrol_down = driver.find_element(By.XPATH ,'/html/body/div[1]/div[2]/div[2]/div/div[1]/div[3]/div[1]/div[3]/div/table/tbody/tr[%s]/td[2]'%(k-1))
    driver.execute_script('arguments[0].scrollIntoView(true)',scrol_down)
    
    sleep(3)
    
 
driver2 = webdriver.Firefox()

# extracting CSVs


for coin in coins :
    historical_link = coin[4]

    driver2.get(historical_link)
    sleep(5)
    #click on date
    driver2.find_element(By.XPATH , '/html/body/div[1]/div[2]/div[1]/div[2]/div/div/div/div[2]/div/div[1]/div/button[1]/div[1]/div').click()
    sleep(3)
    #click on last 365d
    driver2.find_element(By.XPATH ,'/html/body/div[1]/div[2]/div[1]/div[2]/div/div/div/div[2]/div/div[1]/div[2]/div/div[1]/div/div/div[1]/div[2]/ul/li[5]').click()
    sleep(3)
    #click on continue
    driver2.find_element(By.XPATH , '/html/body/div[1]/div[2]/div[1]/div[2]/div/div/div/div[2]/div/div[1]/div[2]/div/div[1]/div/div/div[2]/span/button').click()
    sleep(3)
    # download csv
    driver2.find_element(By.XPATH ,'/html/body/div[1]/div[2]/div[1]/div[2]/div/div/div/div[2]/div/div[1]/div/button[2]/div[1]/div').click()
    

print('historical link success !')

# extracting github URLs and tags

info = list()


for coin in coins :
    mainlink = coin[3]
    driver2.get(mainlink)
    sleep(5)
   
   # make cookies visible
   
    try :
        
        scrol_down = driver2.find_element(By.XPATH ,'/html/body/div[1]/div[2]/div[1]/div[2]/div/div/div[6]/section/div/div[1]/div/h2')
        driver2.execute_script('arguments[0].scrollIntoView(true)',scrol_down)
        sleep(3)
    
    except :
        pass
    
   #cookie
    try :

       driver2.find_element(By.XPATH ,'//*[@id="onetrust-accept-btn-handler"]').click()
       sleep(3)
    except :
        pass


    #scroll down the page to load data part1 (git hub URL)



    
    soup = BeautifulSoup(driver2.page_source ,'html.parser')

    git_hub = 'null'

    official_links = soup.find_all('a' , attrs={'rel':'nofollow noopener'})
    for link in official_links :
        if 'github' in link.get('href'):
            git_hub = link.get('href')
            break

    list_tags = list()
    try :
        tags = soup.find('div',attrs={'class':'sc-16891c57-0 itVAyl coin-tags'})
        tags = tags.find_all('a',attrs={'class':'cmc-link'})
       
        for tag in tags :
            list_tags.append(tag.text)
        
        info.append([git_hub,list_tags])
    except :
        list_tags = 'null'
        info.append([git_hub,list_tags])
        
        

print('finally successful')

# to delete null tags; values

for i in range(200):
    if len(info[i][1])==0:
        info[i][1]=['null']
    info[i][1] = ','.join(info[i][1])
# to merge info with coins   
for i in range(200):
    coins[i] += info[i]

# save data as csv file 

df = pd.DataFrame(coins,columns=['Rank','Name','Symbol','MainLink','HistoricalLink','Git_hub','Tags'] )
df.to_csv('coins200.csv' ,index=False)

stop = time()

print()
print('execution time : ', stop - start)
