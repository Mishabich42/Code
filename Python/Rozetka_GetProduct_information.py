from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sqlite3
from time import sleep

def sl3(seach):
    open(f"{seach}.sl3", "w", encoding="utf-8")
    table = sqlite3.connect(f"{seach}.sl3")
    cur = table.cursor()
    cur.execute("CREATE TABLE product(name TEXT, price TEXT, enable TEXT, url TEXT)")
    cur.close()


def Add_product(seach):
    driver = webdriver.Chrome()
    driver.get("https://rozetka.com.ua/ua/")
    print(driver.title)
    search = driver.find_element(By.NAME, "search")

    search.send_keys(seach)
    search.send_keys(Keys.RETURN)

    try:
        main = WebDriverWait(driver, 200).until(
            EC.presence_of_element_located((By.CLASS_NAME, "catalog"))
        )
        content = main.find_elements(By.CLASS_NAME, "goods-tile__inner")

        table = sqlite3.connect(f"{seach}.sl3")
        cur = table.cursor()

        sleep(10)

        for post in content:
            name = post.find_element(By.CLASS_NAME, "goods-tile__title").text
            price = post.find_element(By.CSS_SELECTOR, ".goods-tile__price-value").text
            enable = post.find_element(By.CLASS_NAME, "goods-tile__availability--available").text
            url = post.find_element(By.CLASS_NAME, "goods-tile__picture").get_attribute("href")

            cur.execute("INSERT INTO product (name, price, enable, url) VALUES (?, ?, ?, ?)",
                        (name, price, enable, url))

        table.commit()
        cur.close()
        print("Ok")
    finally:
        driver.quit()

def main():
    while True:
        seach = input("What you want:")
        sl3(seach)
        Add_product(seach)
        choise = input("Continue Yes/No?:")
        if choise.lower() == "no":
            print("Goodbye")
            break

if __name__ == "__main__":
    main()




