from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from seleniumwire import webdriver as wiredriver

path = r"C:\Users\adity\Desktop\chromedriver-win64\chromedriver-win64\chromedriver.exe"
opt = Options()
opt.add_argument("--headless=new")
driver = webdriver.Chrome(options=opt,executable_path=path)
driver.get(f"https://leetcode.com/contest/weekly-contest-{354}/ranking")
print(driver.title)
