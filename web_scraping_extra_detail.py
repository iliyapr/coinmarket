'''
/html/body/div[1]/div[2]/div[1]/div[2]/div/div/div[2]/div[3]/section[2]/div/div[7]/div[2]/div/span[4]
/html/body/div[1]/div[2]/div[1]/div[2]/div/div/div[2]/div[3]/section[2]/div/div[7]/div[2]/div/span[4]
<p class="sc-1d3ac72d-3 gQFMuZ text-content"><span data-slate-node="element">[reports: FTX likely to get approval to liquidate it's assets on 13th Sept, though they said they will not going to liquidate in one go most likely certain amount weekly.</span></p>
/html/body/div[5]/div/div[2]/div
/html/body/div[5]/div/div[2]/div

div.itVAyl:nth-child(7)
div.itVAyl:nth-child(7)
                                                                              
'''                                                                            

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from time import sleep , time
import requests
from bs4 import BeautifulSoup 

start = time()

driver = webdriver.Firefox()

#load data
coins = pd.read_csv("coins_200.csv")


total_links = list()
total_tags = list()

n = 0 

for mainlink in coins["MainLink"] :
    print(n+1 , ": ")


    driver.get(mainlink)
    sleep(5)
   
   # make cookies visible
   
    try :
        
        scrol_down = driver.find_element(By.XPATH ,'/html/body/div[1]/div[2]/div[1]/div[2]/div/div/div[6]/section/div/div[1]/div/h2')
        driver.execute_script('arguments[0].scrollIntoView(true)',scrol_down)
        sleep(3)
    
    except :
        pass
    
   #cookie
    try :

       driver.find_element(By.XPATH ,'//*[@id="onetrust-accept-btn-handler"]').click()
       sleep(3)
    except :
        pass


    #scroll down the page to load data part1 (git hub URL)



    
    soup = BeautifulSoup(driver.page_source ,'html.parser')
    
    links = dict()

    official_links = soup.find_all('a' , attrs={'rel':'nofollow noopener'})
    for link in official_links :
        links.setdefault(link.text,link.get('href'))
        
    total_links.append(links)

    


    list_tags = dict()
    
    
    try :
        
        scrol_down = driver.find_element(By.CSS_SELECTOR ,'div.itVAyl:nth-child(7)')
        driver.execute_script('arguments[0].scrollIntoView(true)',scrol_down)
        sleep(3)
        
        
        driver.find_element(By.CSS_SELECTOR , "span.sc-9ee74f67-1:nth-child(4)").click()
        
        soup = BeautifulSoup(driver.page_source ,'html.parser')
        tags = soup.find('div',attrs={'class':'sc-16891c57-0 ddQhJW'})
       # tags = driver.find_element(By.XPATH ,"/html/body/div[5]/div/div[2]/div")
        sleep(2)
        tag_title = tags.find_all('span',{'class':'sc-16891c57-0 eltohE base-text'})
        tags_in_each = tags.find_all("div",{"class":"sc-16891c57-0 sc-9ee74f67-0 iGa-diC"})
        
        for tag_num in range(len(tag_title)):
            each_group_tags = list(map(lambda x : x.text ,tags_in_each[tag_num].find_all('a', {"class":"cmc-link"})))
            s = ','.join(each_group_tags)
            list_tags.setdefault(tag_title[tag_num].text ,s )
        
        print(list_tags)
        total_tags.append(list_tags)
        
        
        #info.append([git_hub,list_tags])
    except :
        try :
            
            tags = soup.find('div',attrs={'class':'sc-16891c57-0 itVAyl coin-tags'})
            tags = tags.find_all('a',attrs={'class':'cmc-link'})
            tags = list(map (lambda x:x.text , tags))
            s = ','.join(tags)
            list_tags.setdefault("no_lable",s)
            print(list_tags)
            total_tags.append(list_tags)
            
        except :
            total_tags.append(list_tags)

    
    n+=1
    if n>15 :
        break

stop = time()

extra_detail_1 = pd.DataFrame(total_links)
extra_detail_2 = pd.DataFrame(total_tags)
extra_detail_1.to_csv("links.csv")
extra_detail_2.to_csv('tags')
extra_detail = pd.concat([extra_detail_1,extra_detail_2] , axis=1 , join="inner")
print(stop - start)          