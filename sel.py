from selenium import webdriver  # Импортируем модуль selenium для управления браузером
from selenium.webdriver.common.by import By  # Импортируем класс By для поиска элементов
from selenium.webdriver.common.keys import Keys  # Импортируем Keys для нажатия клавиш
import time  # Импортируем модуль time для пауз

browser = webdriver.Firefox()  # Создаем объект браузера Firefox
browser.get("https://ru.wikipedia.org/wiki/Заглавная_страница")  # Открываем главную страницу Википедии
time.sleep(3)  # Ждем 3 секунды, чтобы страница успела загрузиться

search_box = browser.find_element(By.CLASS_NAME, "vector-search-box-input")  # Находим поле поиска по имени класса
request = input("Введите запрос: ")  # Спрашиваем у пользователя поисковый запрос
search_box.clear()  # Очищаем поле поиска
search_box.send_keys(request)  # Вводим запрос в поле поиска
search_box.send_keys(Keys.RETURN)  # Нажимаем Enter для отправки запроса

time.sleep(5)  # Ждем 5 секунд, чтобы загрузились результаты поиска

# ===== ПЕРВОЕ МЕНЮ: ВЫБОР СТАТЬИ ИЗ РЕЗУЛЬТАТОВ ПОИСКА =====
while True:  # Запускаем бесконечный цикл для выбора статьи или выхода
    print("\n=== МЕНЮ 1 ===")  # Печатаем заголовок меню
    print("1. Выбрать статью из списка")  # Первый вариант действия
    print("2. Выйти из программы")  # Второй вариант действия
    choice = input("Выберите действие (1-2): ")  # Считываем выбор пользователя

    if choice == "2":  # Если пользователь выбрал 2
        print("Пока!")  # Пишем прощальное сообщение
        browser.quit()  # Закрываем браузер
        exit()  # Завершаем программу

    # Находим все элементы li с результатами поиска
    li_elements = browser.find_elements(
        By.CSS_SELECTOR,
        "li.mw-search-result.mw-search-result-ns-0.searchresult-with-quickview"
    )  # Ищем все результаты поиска по CSS-селектору

    if li_elements and choice == "1":  # Если результаты есть и пользователь выбрал пункт 1
        print("\nДоступные статьи:")  # Печатаем заголовок списка статей

        for i, li_elem in enumerate(li_elements):  # Перебираем все элементы списка результатов
            try:
                # Ищем элемент с атрибутом data-prefixedtext внутри li
                prefixed_elem = li_elem.find_element(By.CSS_SELECTOR, "[data-prefixedtext]")  # Находим элемент с атрибутом
                title = prefixed_elem.get_attribute("data-prefixedtext")  # Читаем значение атрибута data-prefixedtext
                print(f"{i}: {title}")  # Печатаем номер и название статьи
            except:  # Если что-то пошло не так
                print(f"{i}: Название не найдено")  # Сообщаем, что название не найдено

        num = int(input(f"Выберите номер статьи (0-{len(li_elements) - 1}): "))  # Спрашиваем номер статьи у пользователя

        try:
            link = li_elements[num].find_element(By.TAG_NAME, "a")  # Находим ссылку <a> внутри выбранного элемента li
            link.click()  # Кликаем по ссылке, чтобы перейти на страницу статьи
            print("Переход на страницу статьи...")  # Сообщаем о переходе
            time.sleep(5)  # Ждем 5 секунд, чтобы статья успела загрузиться
        except Exception as e:  # Если произошла ошибка
            print(f"Ошибка клика: {e}")  # Печатаем сообщение об ошибке
            continue  # Переходим к следующей итерации цикла

        # ===== ВТОРОЕ МЕНЮ: ДЕЙСТВИЯ ВНУТРИ ОДНОЙ СТАТЬИ =====
        while True:  # Запускаем цикл для работы с открытой статьей
            print("\n=== МЕНЮ 2 (СТАТЬЯ) ===")  # Заголовок второго меню
            print("1. Листать параграфы статьи")  # Первый вариант действия
            print("2. Перейти к содержанию")  # Второй вариант действия
            print("3. Вернуться к выбору статьи из поиска")  # Третий вариант — вернуться назад
            inner_choice = input("Выберите действие (1-3): ")  # Считываем выбор пользователя

            if inner_choice == "3":  # Если пользователь выбрал вернуться назад
                break  # Выходим из второго меню и возвращаемся к списку статей

            if inner_choice == "1":  # Если пользователь хочет листать параграфы
                paragraphs = browser.find_elements(By.TAG_NAME, "p")  # Находим все параграфы <p> на странице
                print(f"Найдено параграфов: {len(paragraphs)}")  # Печатаем количество параграфов

                for paragraph in paragraphs:  # Перебираем параграфы
                    text = paragraph.text.strip()  # Берем текст параграфа
                    if not text:  # Если текст пустой, просто пропускаем
                        continue  # Переходим к следующему параграфу
                    print("\n------------------------")  # Линия разделитель
                    print(text)  # Печатаем текст параграфа
                    cmd = input(
                        "Enter — следующий, q — выйти из просмотра параграфов: ")  # Спрашиваем, что делать дальше
                    if cmd.lower() == "q":  # Если ввели q (или Q)
                        break  # Выходим из цикла for и возвращаемся в меню

            if inner_choice == "2":  # Если пользователь хочет перейти по содержанию
                # Ищем пункты оглавления уровня 1
                toc_items = browser.find_elements(
                    By.CSS_SELECTOR,
                    "li.toclevel-1"  # все пункты первого уровня содержания
                )

                if not toc_items:
                    print("Содержание не найдено.")
                    continue

                contents = []  # сюда сложим (якорь, текст пункта)

                print("\nСодержание статьи:")
                for i, li in enumerate(toc_items):
                    try:
                        a_tag = li.find_element(By.TAG_NAME, "a")  # находим ссылку внутри li
                        href = a_tag.get_attribute("href")  # полный href вида '...#Биография'
                        text = a_tag.text.strip()  # текст пункта содержания
                        if not href or "#" not in href:
                            continue
                        anchor = href.split("#", 1)[1]  # достаем часть после #, например 'Биография'
                        contents.append((anchor, text))  # сохраняем якорь и текст
                        print(f"{len(contents) - 1}: {text}")  # печатаем номер и текст пункта
                    except:
                        continue

                if not contents:
                    print("Пункты содержания не найдены.")
                    continue

                num_toc = int(input(f"Выберите номер пункта содержания (0-{len(contents) - 1}): "))
                chosen_li = toc_items[num_toc]  # берем тот же li, из которого показывали текст
                print(f"Переход к разделу: {contents[num_toc][1]}")  # печатаем текст выбранного пункта

                try:
                    a_tag = chosen_li.find_element(By.TAG_NAME, "a")  # находим ссылку внутри li
                    a_tag.click()  # кликаем по ссылке оглавления
                    time.sleep(2)  # даем странице прокрутиться
                except:
                    print("Не удалось перейти к разделу (ошибка клика).")

browser.quit()  # Закрываем браузер
