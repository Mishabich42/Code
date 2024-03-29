from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from time import sleep

def initialize_driver(url):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome()
    driver.get(url)
    return driver

def login(driver, gmail, password):
    Gmail_input = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, "//input[@name='username']"))
    )
    Gmail_input[0].send_keys(gmail)
    password_input = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, "//input[@name='password']"))
    )
    password_input[0].send_keys(password)
    password_input[0].send_keys(Keys.ENTER)

def search(driver, user_name):
    sleep(5)
    driver.execute_script(f"window.location.href = 'https://www.instagram.com/{user_name}/'")

def getInfo(driver):
    followers = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "section > main > div > header > section > ul > li:nth-child(2) > a > span > span"))
    )
    followings = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, "/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/div[2]/section/main/div/header/section/ul/li[3]/a/span/span"))
    )

    with open("Number of followers and followings.txt", "w", encoding="utf-8") as a:
        a.write("followers:" + followers[0].text + "\n" + "followings:" + followings[0].text)

def get_follow(driver, name_text, path):
    follow_button = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, path))
    )
    follow_button[0].click()
    sleep(2)
    slider = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR,
                                             "body > div.x1n2onr6.xzkaem6 > div.x9f619.x1n2onr6.x1ja2u2z > div > div.x1uvtmcs.x4k7w5x.x1h91t0o.x1beo9mf.xaigb6o.x12ejxvf.x3igimt.xarpa2k.xedcshv.x1lytzrv.x1t2pt76.x7ja8zs.x1n2onr6.x1qrby5j.x1jfb8zj > div > div > div > div > div.x7r02ix.xf1ldfh.x131esax.xdajt7p.xxfnqb6.xb88tzc.xw2csxc.x1odjw0f.x5fp0pe > div > div > div._aano"))
    )
    perv_height = driver.execute_script("return arguments[0].scrollHeight;", slider[0])
    processed_users = set()
    while True:
        sleep(4)
        driver.execute_script("arguments[0].scrollTop += 100000;", slider[0])
        sleep(2)
        new_height = driver.execute_script("return arguments[0].scrollHeight;", slider[0])
        if new_height == perv_height:
            break
        perv_height = new_height
        sleep(4)
        followers_list = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR,
                                                 "body > div.x1n2onr6.xzkaem6 > div.x9f619.x1n2onr6.x1ja2u2z > div > div.x1uvtmcs.x4k7w5x.x1h91t0o.x1beo9mf.xaigb6o.x12ejxvf.x3igimt.xarpa2k.xedcshv.x1lytzrv.x1t2pt76.x7ja8zs.x1n2onr6.x1qrby5j.x1jfb8zj > div > div > div > div > div.x7r02ix.xf1ldfh.x131esax.xdajt7p.xxfnqb6.xb88tzc.xw2csxc.x1odjw0f.x5fp0pe > div > div > div._aano"))
        )
        with open(f"{name_text}.txt", "a", encoding="utf-8") as a:
            for follower_info in followers_list:
                follower_names = follower_info.find_elements(By.XPATH, "//a[@role='link']/div/div/span")
                for name in follower_names:
                    username = name.text
                    if username not in processed_users:
                        a.write("url:https://www.instagram.com/" + username + "/" + "  username:" + username + "\n")
                        processed_users.add(username)
    close_button = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, "//button[@class='_abl-']"))
    )
    close_button[0].click()

if __name__ == '__main__':
    driver = initialize_driver('https://www.instagram.com')
    login(driver, "dek6779@gmail.com", "p9753131")
    sleep(3)
    search(driver, "sefsis_")
    sleep(3)
    getInfo(driver)
    sleep(3)
    get_follow(driver, "followings", "/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/div[2]/section/main/div/header/section/ul/li[3]/a/span/span")
    sleep(3)
    driver.refresh()
    sleep(3)
    get_follow(driver, "follower", "/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/div[2]/section/main/div/header/section/ul/li[2]/a/span/span")
    sleep(3)
    driver.refresh()
    sleep(3)