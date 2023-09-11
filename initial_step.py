import sys
sys.path.append(r'C:\Users\ASUS\PycharmProjects\pythonProjectquera')
from selenium import webdriver
from selenium.webdriver.common.by import By
import constant as const
import os
from selenium.webdriver.chrome.options import Options
from time import sleep
from itertools import chain
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep,time
import requests
from bs4 import BeautifulSoup





class CoinMarketCap(webdriver.Chrome):



    def __init__(self):
        # Initialize the Chrome WebDriver with options
        chrome_options = Options()
        chrome_options.add_argument("--detach")  # Equivalent to "detach" option for Firefox
        self.driver_path = const.DRIVER_PATH
        os.environ['PATH'] += os.pathsep + self.driver_path
        super(CoinMarketCap, self).__init__(options=chrome_options)




    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            self.quit()



    def get_data(self):
        # Navigate to the https://coinmarketcap.com/historical/20230825 URL
        self.get(const.url)
        sleep(5)
        # Locate the table containing data
        table = self.find_element(By.XPATH,'/html/body/div[1]/div[2]/div[2]/div/div[1]/div[3]/div[1]/div[3]/div/table/tbody')
        # Extract rank,name,symbol,mainlink,historical_link from the table
        k = 1
        coins = list()
        for i in range(20):
            for j in range(10):
                rank = table.find_element(By.XPATH,'/html/body/div[1]/div[2]/div[2]/div/div[1]/div[3]/div[1]/div[3]/div/table/tbody/tr[%s]/td[1]' % ( k))
                name = table.find_element(By.XPATH,'/html/body/div[1]/div[2]/div[2]/div/div[1]/div[3]/div[1]/div[3]/div/table/tbody/tr[%s]/td[2]' % ( k))
                symbol = table.find_element(By.XPATH,'/html/body/div[1]/div[2]/div[2]/div/div[1]/div[3]/div[1]/div[3]/div/table/tbody/tr[%s]/td[3]' % (k))
                mainlink = table.find_element(By.XPATH,'/html/body/div[1]/div[2]/div[2]/div/div[1]/div[3]/div[1]/div[3]/div/table/tbody/tr[%s]/td[2]/div/a[2]' % (k)).get_attribute('href')
                historical_link = mainlink + 'historical-data/'
                coins.append([rank.text, name.text, symbol.text, mainlink, historical_link])
                k += 1

            # scroll down the page to load more data
            scrol_down = self.find_element(By.XPATH,'/html/body/div[1]/div[2]/div[2]/div/div[1]/div[3]/div[1]/div[3]/div/table/tbody/tr[%s]/td[2]' % (k - 1))
            self.execute_script('arguments[0].scrollIntoView(true)', scrol_down)
            sleep(3)
        return coins




    def extract_csv(self,coins):
        #Extract Historical_link using coins
        for coin in coins:
            historical_link = coin[4]

            self.get(historical_link)
            sleep(5)
            try:

                self.find_element(By.XPATH, '//*[@id="onetrust-accept-btn-handler"]').click()
                sleep(3)
            except:
                pass
            # click on date
            self.find_element(By.XPATH,
                                 '/html/body/div[1]/div[2]/div[1]/div[2]/div/div/div/div[2]/div/div[1]/div/button[1]/div[1]/div').click()
            sleep(3)
            # click on last 365d
            self.find_element(By.XPATH,
                                 '/html/body/div[1]/div[2]/div[1]/div[2]/div/div/div/div[2]/div/div[1]/div[2]/div/div[1]/div/div/div[1]/div[2]/ul/li[5]').click()
            sleep(3)
            # click on continue
            self.find_element(By.XPATH,
                                 '/html/body/div[1]/div[2]/div[1]/div[2]/div/div/div/div[2]/div/div[1]/div[2]/div/div[1]/div/div/div[2]/span/button').click()
            sleep(3)
            # download csv
            self.find_element(By.XPATH,
                                 '/html/body/div[1]/div[2]/div[1]/div[2]/div/div/div/div[2]/div/div[1]/div/button[2]/div[1]/div').click()

        print('historical link success !')



    def github_info(self,coins):
        #extracting_github_URLs_tags
        info = list()
        for coin in coins:
            mainlink = coin[3]
            self.get(mainlink)
            sleep(5)
            # make cookies visible
            try:

                scrol_down = self.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[1]/div[2]/div/div/div[6]/section/div/div[1]/div/h2')
                self.execute_script('arguments[0].scrollIntoView(true)', scrol_down)
                sleep(3)

            except:
                pass

            # cookie
            try:

                self.find_element(By.XPATH, '//*[@id="onetrust-accept-btn-handler"]').click()
                sleep(3)

            except:
                pass

            # scroll down the page to load more data part1 (git hub URL)
            soup = BeautifulSoup(self.page_source, 'html.parser')
            #Extract git_hub link
            git_hub = 'null'
            official_links = soup.find_all('a', attrs={'rel': 'nofollow noopener'})
            for link in official_links:
                if 'github' in link.get('href'):
                    git_hub = link.get('href')
                    break
            # Extract tags
            list_tags = list()
            try:
                tags = soup.find('div', attrs={'class': 'sc-16891c57-0 itVAyl coin-tags'})
                tags = tags.find_all('a', attrs={'class': 'cmc-link'})

                for tag in tags:
                    list_tags.append(tag.text)

                info.append([git_hub, list_tags])
            except:

                list_tags = 'null'
                info.append([git_hub, list_tags])

        return info




    def delete_null_tags(self,info,coins):
        # delete null tags
        for i in range(200):
            if len(info[i][1]) == 0:
                info[i][1] = ['null']
            info[i][1] = ','.join(info[i][1])
        # merge info with coins
        for i in range(200):
            coins[i] += info[i]

        # save data as csv file
        df = pd.DataFrame(coins, columns=['Rank', 'Name', 'Symbol', 'MainLink', 'HistoricalLink', 'Git_hub', 'Tags'])
        df.to_csv('coins200.csv', index=False)




if __name__ == '__main__':
    bot1=CoinMarketCap()
    coins=bot1.get_data()
    bot2 = CoinMarketCap()
    bot2.extract_csv(coins)
    info=bot2.github_info(coins)
    bot2.delete_null_tags(info,coins)







