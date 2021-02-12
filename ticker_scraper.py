from selenium import webdriver
from bs4 import BeautifulSoup
import random
import pyautogui
import time
import pandas as pd
import re

def open_browser(requests):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    agents = ["Firefox/66.0.3", "Chrome/73.0.3683.68", "Edge/16.16299"]
    print("User agent: " + agents[(requests % len(agents))])
    chrome_options.add_argument('--user-agent=' + agents[(requests % len(agents))] + '"')
    chrome_options.add_experimental_option('useAutomationExtension', False)
    browsr = webdriver.Chrome(executable_path=r"C:\Users\Jimmy\AppData\Local\Programs\Python\Python37\chromedriver.exe",
                              options=chrome_options, desired_capabilities=chrome_options.to_capabilities())
    browsr.maximize_window()
    return browsr


# step 1 --> get all tickers
requests = 0
driver = open_browser(requests)
ticker_list = []
for i in range(1340):
    while True:
        try:
            if i % 10 == 0:
                driver.close()
                requests += 1
                driver = open_browser(requests)
            else:
                pass
            # create url
            customized_url = "https://www.gurufocus.com/stock_list.php?p=" + str(i) + "&n=100"
            print("*** URL: " + customized_url + " ***")
            driver.get(customized_url)
            random_waiting = random.randint(2, 5)
            time.sleep(random_waiting)
            pyautogui.moveTo(x=random.randint(245, 255), y=random.randint(245, 255))
            pyautogui.click()
            html_content = driver.page_source
            soup = BeautifulSoup(html_content, 'html.parser')
            table = soup.find("table", attrs={"class": "R5"})
            for tr in table.find_all("tr"):
                stock_details = []
                for td in tr.find_all("td", attrs={"class": "text"}):
                    stock_details.append(td.get_text())
                if len(stock_details) != 0:
                    ticker_list.append(stock_details)
        except:
            driver.close()
            requests += 1
            driver = open_browser(requests)
            continue
        break
driver.close()

# step 2 --> clean ticker list
for num, ticker in enumerate(ticker_list):
    print("Ticker {}: {}".format(num, ticker[0]))
    clean_ticker = re.sub('\..*', '', ticker[0])
    ticker_list[num][0] = clean_ticker

# step 3 --> remove duplicates
stock_df = pd.DataFrame(ticker_list, columns=['Ticker', 'Stock_Name'])
stock_df = stock_df.drop_duplicates(subset="Ticker")

# step 4 --> excel export. database export also an option depending on use case
stock_df.to_excel("all_ticker.xlsx", index=False)
