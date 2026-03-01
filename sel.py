from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

browser = webdriver.Firefox()  # Создаем браузер Firefox
browser.get("https://ru.wikipedia.org/wiki/Заглавная_страница")  # Открываем главную страницу Википедии
time.sleep(3)  # Ждем 3 секунды загрузки страницы

search_box = browser.find_element(By.CLASS_NAME, "vector-search-box-input")  # Находим поле поиска
request = input("Введите запрос: ")  # Спрашиваем у пользователя запрос
search_box.clear()  # Очищаем поле поиска
search_box.send_keys(request)  # Вводим запрос в поле поиска
search_box.send_keys(Keys.RETURN)  # Нажимаем Enter для поиска

time.sleep(5)  # Ждем загрузки результатов поиска

while True:  # Запускаем бесконечный цикл для основного меню
    print("\n=== МЕНЮ ===")
    print("1. Перейти на связанную страницу")
    print("2. Выйти")
    choice = input("Выберите действие (1-2): ")  # Спрашиваем выбор у пользователя

    if choice == "2":  # Если пользователь выбрал 2 - выходим
        print("Пока!")
        break

    # Находим результаты поиска
    li_elements = browser.find_elements(By.CSS_SELECTOR,
                                        "li.mw-search-result.mw-search-result-ns-0.searchresult-with-quickview")

    if li_elements and choice == "1":  # Если есть результаты поиска И выбрано 1
        print("\nДоступные статьи:")

        for i, li_elem in enumerate(li_elements):  # Перебираем все найденные статьи
            try:
                # ИЩЕМ ЭЛЕМЕНТ С data-prefixedtext="НАЗВАНИЕ"
                prefixed_elem = li_elem.find_element(By.CSS_SELECTOR,
                                                     "[data-prefixedtext]")  # Находим элемент с атрибутом
                title = prefixed_elem.get_attribute("data-prefixedtext")  # Берем значение атрибута
                print(f"{i}: {title}")  # Показываем точное название из атрибута
            except:
                print(f"{i}: Название не найдено")  # Если атрибута нет

        num = int(input("Выберите номер статьи (0-{}): ".format(len(li_elements) - 1)))  # Спрашиваем номер статьи

        # КЛИКАЕМ ПО ССЫЛКЕ
        try:
            link = li_elements[num].find_element(By.TAG_NAME, "a")  # Берем ссылку из выбранного li
            link.click()  # Кликаем именно по ссылке
            print("Переход на страницу статьи...")
            time.sleep(5)  # Ждем загрузки статьи
        except Exception as e:
            print(f"Ошибка клика: {e}")
        continue  # Возвращаемся к основному меню

browser.quit()  # Закрываем браузер в самом конце
