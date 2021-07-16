import time
from bs4.element import ContentMetaAttributeValue
# import requests
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
import json
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException

# 1. Pegar conteúdo HTML a partir da URL

url = "https://www.nba.com/stats/players/traditional/?sort=PTS&dir=1&SeasonType=Regular%20Season&Season=2019-20&PerMode=Totals"
top10ranking = {}
rankings = {
    '3points': {'field': 'FG3M', 'label': '3PM'},
    'points': {'field': 'PTS', 'label': 'PTS'},
    'assistants': {'field': 'AST', 'label': 'AST'},
    'rebounds': {'field': 'REB', 'label': 'REB'},
    'steals': {'field': 'STL', 'label': 'STL'},
    'blocks': {'field': 'BLK', 'label': 'BLK'},
}


def buildrank(type):

    field = rankings[type]['field']
    label = rankings[type]['label']

    time.sleep(0.5)

    driver.find_element_by_xpath(f"//div[@class='nba-stat-table']//table//thead//tr//th[@data-field='{field}']").click()

    element = driver.find_element_by_xpath("//div[@class='nba-stat-table']//table")
    html_content = element.get_attribute('outerHTML')

    # 2 Parsear o conteúdo HTML - BeautifulSoup

    soup = BeautifulSoup(html_content, 'html.parser')
    table = soup.find(name='table')
    # 3 Estruturar conteúdo em um Data Frame - Pandas

    df_full = pd.read_html(str(table))[0].head(10)
    df = df_full[['Unnamed: 0', 'PLAYER', 'TEAM', label]]
    df.columns = ['pos', 'player', 'team', 'total']

    # 4 Transformar os Dados em um Dicionário de dados próprio
    print(df)
    return df.to_dict('records')


driver = webdriver.Chrome(executable_path=r'C:\chromedriver.exe')

driver.get(url)
time.sleep(2)
driver.find_element_by_xpath("//div[@class='banner-actions-container']//button[@id='onetrust-accept-btn-handler']").click()

for k in rankings:
    top10ranking[k] = buildrank(k)

driver.quit()

# 5. Converter e salvar em um arquivo JSON
js = json.dumps(top10ranking)
fp = open('ranking7.json', 'w')
fp.write(js)
fp.close()
