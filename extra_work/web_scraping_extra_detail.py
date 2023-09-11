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
github_info = list()


for mainlink in coins["MainLink"] :



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

        sleep(2)
        tag_title = tags.find_all('span',{'class':'sc-16891c57-0 eltohE base-text'})
        tags_in_each = tags.find_all("div",{"class":"sc-16891c57-0 sc-9ee74f67-0 iGa-diC"})
        
        for tag_num in range(len(tag_title)):
            each_group_tags = list(map(lambda x : x.text ,tags_in_each[tag_num].find_all('a', {"class":"cmc-link"})))
            s = ','.join(each_group_tags)
            list_tags.setdefault(tag_title[tag_num].text ,s )
        

    except :
        try :
            
            tags = soup.find('div',attrs={'class':'sc-16891c57-0 itVAyl coin-tags'})
            tags = tags.find_all('a',attrs={'class':'cmc-link'})
            tags = list(map (lambda x:x.text , tags))
            s = ','.join(tags)
            list_tags.setdefault("no_lable",s)
            total_tags.append(list_tags)
            
        except :
            total_tags.append(list_tags)
            

for github in coins["Git_hub"] :
    
    each_github_info = dict()
    

    if type(github) != str :
        print("null")
        
        github_info.append(each_github_info)
        print()
        continue
    

    
    try :
        
        # forks and stars
        driver.get(github)
        sleep(3)
        soup = BeautifulSoup(driver.page_source , 'html.parser')
        
        about = soup.find('div',attrs = {'class':'BorderGrid-cell'})
        info_of_rows = about.find_all('a',{'class':'Link Link--muted'})
        sleep(1)
        
        for each_info in info_of_rows :
            if 'stars' in each_info.text.lower() :
                row = (each_info.text).replace('\n','')
                row = row.split()
                num_stars = row[0].strip()
                each_github_info.setdefault('stars',num_stars)
                
            elif 'forks' in each_info.text.lower() :
                row = (each_info.text).replace('\n','')
                row = row.split()
                num_forks = row[0].strip()
                each_github_info.setdefault('forks',num_forks)
                
            
        # languages 
        
        total_languages = (soup.find_all('div',{'class':'BorderGrid-cell'})[-1]).text
        print('here')
        total_languages = total_languages.replace('Languages','')
        total_languages = total_languages.split('\n')
        
        for i in range(len(total_languages)-1 ):
            if total_languages[i]!='' and total_languages[i+1]!='':
                each_github_info.setdefault(total_languages[i],total_languages[i+1])
        
        print(each_github_info)
        
       

    
    except :
        print(github)
        print("can't scrap")
        print()
    
    
    github_info.append(each_github_info)
        

        
    
set_lan = set()
set_tags = set()

for i in github_info :
    if len(i)==0 :
        continue
    l  = list(i.keys()  )
    l.remove('stars')
    l.remove('forks')
    set_lan.union(set(l))

for i in total_tags :
    if(len(i)==0):
        continue
    l  = list(i.keys() )
    set_tags.union(set(l))
    
    
set_lan = sorted(list(set_lan))
set_tags = sorted(list(set_tags))

data = {'Language_Id':[i for i in range(1,len(set_lan)+1)],
        'Language':set_lan}

lang = pd.DataFrame(data)

data = {'Tag_Id':[i for i in range(1,len(set_tags)+1)],
        'Tag':set_tags}

all_tags = pd.DataFrame(data)

github_info = pd.DataFrame(github_info)



    

    




extra_links = pd.DataFrame(total_links)
extra_tags = pd.DataFrame(total_tags)


lang.to_csv("languages.csv",index=False)
github_info.to_csv("github_info.csv",index=False)

total_links.to_csv("total_links.csv",index = False)
total_tags.to_csv('total_tags.csv',index = False)

all_tags.to_csv("all_tags.csv")

extra_detail = pd.concat([total_links , total_tags] , axis=1 , join="inner")
stop = time()
print(stop - start)          