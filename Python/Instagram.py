from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from re import findall
from time import sleep

def initialize_driver(url):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options)
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
    info = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, "//li[@class='xl565be x1m39q7l x1uw6ca5 x2pgyrj']"))
    )
    for element in info:
        with open("Number of followers and followings.txt", "a", encoding="utf-8") as a:
            a.write(element.text + "\n")

def get_follow(driver, name_text, path):
    follow_button = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, path))
    )
    follow_button[0].click()
    sleep(2)
    slider = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "body > div.x1n2onr6.xzkaem6 > div.x9f619.x1n2onr6.x1ja2u2z > div > div.x1uvtmcs.x4k7w5x.x1h91t0o.x1beo9mf.xaigb6o.x12ejxvf.x3igimt.xarpa2k.xedcshv.x1lytzrv.x1t2pt76.x7ja8zs.x1n2onr6.x1qrby5j.x1jfb8zj > div > div > div > div > div.x7r02ix.xf1ldfh.x131esax.xdajt7p.xxfnqb6.xb88tzc.xw2csxc.x1odjw0f.x5fp0pe > div > div > div._aano"))
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
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "body > div.x1n2onr6.xzkaem6 > div.x9f619.x1n2onr6.x1ja2u2z > div > div.x1uvtmcs.x4k7w5x.x1h91t0o.x1beo9mf.xaigb6o.x12ejxvf.x3igimt.xarpa2k.xedcshv.x1lytzrv.x1t2pt76.x7ja8zs.x1n2onr6.x1qrby5j.x1jfb8zj > div > div > div > div > div.x7r02ix.xf1ldfh.x131esax.xdajt7p.xxfnqb6.xb88tzc.xw2csxc.x1odjw0f.x5fp0pe > div > div > div._aano"))
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

def get_posts(driver):
    list_posts = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, "//div[@class='x1lliihq x1n2onr6 xh8yej3 x4gyw5p x2pgyrj xbkimgs xfllauq xh8taat xo2y696']"))
    )
    for post in list_posts:
        post.click()
        image_src = post.find_element(By.XPATH, "//img[@class='x5yr21d xu96u03 x10l6tqk x13vifvy x87ps6o xh8yej3']")
        video_elements = post.find_elements(By.XPATH, "//video[@class='x1lliihq x5yr21d xh8yej3']")
        time = WebDriverWait(post, 10).until(
            EC.presence_of_element_located((By.XPATH, "//time"))
        )
        tim = time.text
        likes = post.find_element(By.XPATH, "//span[@class='x193iq5w xeuugli x1fj9vlw x13faqbe x1vvkbs xt0psk2 x1i0vuye xvs91rp x1s688f x5n08af x10wh9bi x1wdrske x8viiok x18hxmgj']")
        digits = findall(r'\d+', likes.text)
        like = ''.join(digits)
        close_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[@class='x160vmok x10l6tqk x1eu8d0j x1vjfegm']"))
        )
        close_button.click()
        with open("Posts.txt", "a", encoding="utf-8") as a:
            if video_elements:
                a.write("src: " + video_elements[0].get_attribute("src") + "\n" + "Likes: " + like + "\n" + "Time: " + tim + "\n")
            else:
                a.write("src: " + image_src.get_attribute(
                    "src") + "\n" + "Likes: " + like + "\n" + "Time: " + tim + "\n")
        sleep(3)


if __name__ == '__main__':
    driver = initialize_driver('https://www.instagram.com')
    login(driver, "dek6779@gmail.com", "p9753131")
    sleep(3)
    search(driver, "sefsis_")
    sleep(3)
    get_posts(driver)
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