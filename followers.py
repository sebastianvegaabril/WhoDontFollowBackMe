from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time, urllib.request
import requests
import pyautogui

chrome_options = Options()
chrome_options.add_argument('--log-level=1')

driver = webdriver.Chrome(options=chrome_options)

screen_width, screen_height = pyautogui.size()

new_width = int(screen_width * 0.20)

driver.set_window_size(new_width, screen_height)
print(" --------------------------------------------------------------------------------------------------------------------------------")
print("| Please note that you can use a fake account to register, it is not necessary to use the same account that you want to analyze. |")
print("| I didn't put any error message yet, if it doesn't work, please confirm that the credentials are correct and try again.         |")
print(" --------------------------------------------------------------------------------------------------------------------------------")
time.sleep(3)
usernameInput = input("Enter your username:")
passwordInput = input("Enter your password:")
accountToAnalyze = input("Enter the account you want to analyze:")

driver.get("https://www.instagram.com/")

time.sleep(5)
username=driver.find_element(By.NAME, "username")
password=driver.find_element(By.NAME, "password")
username.clear()
password.clear()
username.send_keys(usernameInput)
password.send_keys(passwordInput)
time.sleep(5)
login = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
login.click()

time.sleep(10)
notnow = driver.find_element(By.XPATH, "//div[@tabindex='0']").click()
time.sleep(10)
notnow2 = driver.find_element(By.XPATH, "//button[contains(text(), 'Not Now')]").click() ## anda

time.sleep(5)
driver.get(f"https://www.instagram.com/{accountToAnalyze}")

time.sleep(5)
following = driver.find_element(By.XPATH, f"//a[@href='/{accountToAnalyze}/following/']").click()
time.sleep(5)

divToScroll = driver.find_element(By.XPATH, '/html/body/div[7]/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[4]')
match = False
while not match:
    last_scroll_height = driver.execute_script("return arguments[0].scrollHeight;", divToScroll)
    driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight;", divToScroll)
    time.sleep(3)
    new_scroll_height = driver.execute_script("return arguments[0].scrollHeight;", divToScroll)
    if last_scroll_height == new_scroll_height:
        match = True

container = driver.find_element(By.XPATH, '/html/body/div[7]/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[4]/div[1]/div')
links = container.find_elements(By.XPATH, './/a')

followedAccounts = []
for link in links:
    account = link.get_attribute('href')
    followedAccounts.append(account)

time.sleep(5)
closeButton = driver.find_element(By.XPATH, "/html/body/div[7]/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[1]/div/div[3]/div/button").click()
time.sleep(5)
followers = driver.find_element(By.XPATH, f"//a[@href='/{accountToAnalyze}/followers/']").click()
time.sleep(5)

divToScrollFollowers = driver.find_element(By.XPATH, '/html/body/div[7]/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]')
matchFollowers = False
while not matchFollowers:
    last_scroll_height_Followers = driver.execute_script("return arguments[0].scrollHeight;", divToScrollFollowers)
    driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight;", divToScrollFollowers)
    time.sleep(3)
    new_scroll_height_Followers = driver.execute_script("return arguments[0].scrollHeight;", divToScrollFollowers)
    if last_scroll_height_Followers == new_scroll_height_Followers:
        matchFollowers = True
        
containerfollowers = driver.find_element(By.XPATH, '/html/body/div[7]/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]')
linksfollowers = containerfollowers.find_elements(By.XPATH, './/a')

followersAccounts = []
for link in linksfollowers:
    account = link.get_attribute('href')
    followersAccounts.append(account)

dontFollowMe = []
for followed in followedAccounts:
    if(not(followersAccounts.__contains__(followed))):
        dontFollowMe.append(followed)

uniqueDontFollowMe = list(set(dontFollowMe))

total_width = 63

print(" ---------------------------------------------------------------")
print("|              Accounts that don't follow you back              |")
print(" ---------------------------------------------------------------")
for account in uniqueDontFollowMe:
    print(f"|  {account.ljust(total_width - 2)}|")
print(" ---------------------------------------------------------------")