from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

browser = webdriver.Firefox()
browser.get("https://ru.wikipedia.org/wiki/Заглавная_страница")
time.sleep(3)

search_box = browser.find_element(By.CLASS_NAME, "vector-search-box-input")
request = input("Введите запрос: ")
search_box.clear()  # Очистите поле перед вводом
search_box.send_keys(request)
search_box.send_keys(Keys.RETURN)

time.sleep(5)  # Ждем загрузки результатов

browser.quit()