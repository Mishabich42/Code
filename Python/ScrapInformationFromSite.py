from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException

def initialize_driver(url):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    return driver

def getImages(driver):
    try:
        images = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, "img"))
        )
        unique_images = set()
        for img in images:
            try:
                src = img.get_attribute("src")
                if src:
                    unique_images.add(src)
            except StaleElementReferenceException:
                pass

        with open("images.txt", "w", encoding="utf-8") as a:
            for src in unique_images:
                a.write(src + "\n")
    except:
        print("Error in getting images.")

def getText(driver):
    try:
        body = driver.find_element(By.TAG_NAME, 'body')
        text = body.text
        with open("visible_text.txt", "w", encoding="utf-8") as file:
            file.write(text)
    except:
        print("Error in getting text.")

def getHTML(driver):
    try:
        page_text = driver.page_source
        with open("HTML.txt", "w", encoding="utf-8") as file:
            file.write(page_text)
    except:
        print("Error in getting HTML.")

def getHREF(driver):
    try:
        links = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//a[@href]"))
        )
        unique_href = set()
        for link in links:
            href = link.get_attribute("href")
            if href:
                unique_href.add(href)
        with open("href.txt", "w", encoding="utf-8") as a:
            for href in unique_href:
                a.write(href + "\n")
    except:
        print("Error in getting HREF.")

if __name__ == '__main__':
    url = input("Enter the URL: ")
    try:
        driver = initialize_driver(url)
        getHTML(driver)
        getImages(driver)
        getText(driver)
        getHREF(driver)
    except:
        print("Error occurred.")
    finally:
        driver.quit()
