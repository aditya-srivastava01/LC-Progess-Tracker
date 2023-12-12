from selenium import webdriver
from selenium.webdriver.common.by import By
import codecs
import os
import time
from pathlib import Path
from selenium.webdriver.chrome.options import Options

path = r"C:\Users\adity\Desktop\chromedriver-win64\chromedriver-win64\chromedriver.exe"

def fetch(name,last_page):
    opt = Options()
    opt.add_argument("--headless=new")
    driver = webdriver.Chrome(options=opt)
    Path(f"weekly/weekly{name}/").mkdir(exist_ok=True)
    for i in range(1, last_page + 1):
        driver.get(f"https://leetcode.com/contest/weekly-contest-{name}/ranking/{i}/")
        n=os.path.join(f"weekly/weekly{name}/",f"{i}.html")
        time.sleep(1)
        file = codecs.open(n, "w", "utf−8")
        h = driver.page_source
        file.write(h)
        file.close()
        print(f"Saved {i}/{last_page}.html Successfully!!!!")
    driver.quit()


for pg in range(340,0,-1):    
    opt = Options()
    opt.add_argument("--headless=new")
    driver = webdriver.Chrome()
    driver.get(f"https://leetcode.com/contest/weekly-contest-{pg}/ranking")
    last_page = driver.find_elements('css selector', '.page-btn')
    last_page = int([i.text for i in last_page][-1])
    driver.quit()
    print(last_page)
    start_time = time.time()
    fetch(pg,last_page)
    print(time.time()-start_time)
    break