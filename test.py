from selenium import webdriver
from selenium.webdriver.common.by import By
import mysql.connector
import codecs
import os
from bs4 import BeautifulSoup
import json
import codecs
import time
from pathlib import Path
from selenium.webdriver.chrome.options import Options


path = r"C:\Users\adity\Desktop\chromedriver-win64\chromedriver-win64\chromedriver.exe"
config = {
    'user': 'root',
    'password': '0000',
    'host': 'localhost',
    'database': 'leetcode'
}

# Connect to MySQL
conn = mysql.connector.connect(**config)
cursor = conn.cursor()


def change(s):
    s = s.split("  ")
    if len(s)==0:
        s.append(0)
        s.append(0)
    else:
        if len(s[0])==0:
            s[0] = 0
        else:
            s[0] = s[0].replace(" ","")
            s[0] = s[0].split(":")
            s[0] = int(s[0][0])*60*60+int(s[0][1])*60+int(s[0][2])
    if len(s)==1:
        s.append(0)
    else:
        s[1] = int(s[1])
    
    s = {"finish_time":s[0],"wa":s[1]}
    json_data = json.dumps(s)
    return json_data

def insert(name,last_page):
    for pg in range(1,last_page+1):
        with open(f"weekly/weekly{name}/{pg}.html", 'r', encoding='utf-8') as file:
            html_content = file.read()
            soup = BeautifulSoup(html_content, 'html.parser') 
            usernames = soup.find_all("tr")
            flag = False
            for usr in usernames:
                user_td = usr.find_all("td")
                if flag:
                    data = [i.text for i in user_td]
                    rank = int(data[0])
                    user_id = data[1].replace(r"\xa0\xa0","").strip()
                    score = data[2]
                    finish_time = change(data[3])
                    Q1 = change(data[4])
                    Q2 = change(data[5])
                    Q3 = change(data[6])
                    Q4 = change(data[7])
                    data = []
                    data = [rank, user_id, score , finish_time,Q1,Q2,Q3,Q4]
                    try:
                        query = f"INSERT INTO weekly{name}(rnk, user_id, score, finish_time, Q1, Q2, Q3, Q4) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);"
                        cursor.execute(query, data)
                        conn.commit()
                    except Exception as e:
                        print(f"Failed at weekly{name} at page {pg} Entry {data}")
                    # print(f"{str(rank):5}  {user_id:25}  {str(score):5}  {str(finish_time):12}  {str(Q1):20}  {str(Q2):20}  {str(Q3):20}  {str(Q4):20}")
                    # break
                flag = True

def fetch(name,last_page):
    opt = Options()
    opt.add_argument("--headless=new")
    driver = webdriver.Chrome(options=opt,executable_path=path)
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


def exc(pg):
    print("Starting Contest : ",pg)
    opt = Options()
    opt.add_argument("--headless=new")
    driver = webdriver.Chrome(options=opt,executable_path=path)
    driver.get(f"https://leetcode.com/contest/weekly-contest-{pg}/ranking")
    last_page = driver.find_elements('css selector', '.page-btn')
    last_page = int([i.text for i in last_page][-1])
    driver.quit()
    print(last_page)
    start_time = time.time()
    fetch(pg,last_page)
    insert(pg,last_page)
    print(time.time()-start_time)
    print("----------------------------------------------")

cursor.close()
conn.close()

