import requests, os
import logging
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time, glaza_data, bs4, sys


logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level = logging.INFO,
                    filename = 'bot.log'
                    )


def auth():
    browser.get('http://glaza.info/board/0-0-0-0-1')

    login = browser.find_element_by_name('user')
    password = browser.find_element_by_name('password')

    login.send_keys(user)
    password.send_keys(passw)

    browser.find_element_by_name('sbm').click()
    time.sleep(10)
    logging.info('Авторизуемся')


def send_ad():
    logging.info('Выставляем объявление')
    browser.get('http://glaza.info/board/0-0-0-0-1')
    #time.sleep(10)

    # Кликаем на выбор категории
    cat_xpath = '//input[@class="x-selectable u-comboedit u-comboeditimg"]'
    cat = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, cat_xpath)))
    cat.click()

    # Выбираем категорию "Для детей - разное"
    browser.find_element_by_id(category).click()

    # Продам
    WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.CLASS_NAME, 'manFlFlt3')))
    select = Select(browser.find_element_by_class_name('manFlFlt3'))
    try:
        select.select_by_value(type_of_ad)
    except ElementClickInterceptedException:
        time.sleep(5)
        select.select_by_value(type_of_ad)

    # Телефон
    phone_number = browser.find_element_by_class_name('manFlPhone')
    phone_number.send_keys(phone)

    # Заголовок
    title = browser.find_element_by_class_name('manFlTitle')
    title.send_keys(headline)

    # Регион
    region = Select(browser.find_element_by_class_name('manFlFlt2'))
    region.select_by_value(region_)

    # Текст объявления
    main_text = browser.find_element_by_xpath('//textarea[@class="manFl"]')
    main_text.send_keys(message)

    # Добавляем картинки
    if len(list_of_pictures) > 1:
        plus_img = browser.find_element_by_xpath('//div[@id="iplus"]/input[@class="button"]')
        for i in range(len(list_of_pictures) - 1):
            plus_img.click()

    for picture in list_of_pictures:
        image = browser.find_element_by_xpath(f'//input[@id="fln{list_of_pictures.index(picture) + 1}"]')
        if sys.platform != 'linux':
            path_to_img = os.getcwd() + '\\images\\' + picture
        else:
            path_to_img = os.getcwd() + '/images/' + picture
        # path_to_img = 'C:\\tmp\\smartwatch\\' + picture

        image.send_keys(path_to_img)

    # Цена
    cena = browser.find_element_by_class_name('manFlOth1')
    cena.send_keys(price)

    # Где публиковать
    # where_to_publish = Select(browser.find_element_by_class_name('manFlFlt1'))
    # where_to_publish.select_by_value('1')

    # Контактное лицо
    contact = browser.find_element_by_class_name('manFlaName')
    contact.send_keys(name_of_advertiser)

    # Мозырь
    sity_ad = browser.find_element_by_class_name('manFlOth2')
    sity_ad.send_keys(sity)

    # Отправляем объявление
    send_ad = browser.find_element_by_xpath('//center/input[@class="manFlSbm"]')
    send_ad.click()

    WebDriverWait(browser, 40).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'myWinSuccess')))
    logging.info('Выставили объявление')



def delete_old_ad():
    logging.info('Удаляем объявления')
    while True:
        browser.get('http://glaza.info/board/0-0-91938-0-17')

        try:
            element_to_hover_over = browser.find_element_by_class_name('u-mpanel-toggle')

            button_to_click = browser.find_element_by_xpath('//li[@class="u-mpanel-del"]/a')

            actions_to_hover = ActionChains(browser)

            WebDriverWait(browser, 3).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'u-mpanel-toggle')))

            actions_to_hover.move_to_element(element_to_hover_over)

            WebDriverWait(browser, 3).until(
                EC.presence_of_element_located((By.XPATH, '//li[@class="u-mpanel-del"]/a')))

            actions_to_hover.click(button_to_click)
            actions_to_hover.perform()


        except NoSuchElementException:
            break

        # Клик на кнопку "ОК" в диалоговом окне
        try:
            WebDriverWait(browser, 5).until(EC.alert_is_present(), 'Waiting for alert timed out')

            alert = browser.switch_to.alert
            alert.accept()
            print("Удалил объявление")

        except TimeoutException:
            print("Глюканул")


def check_if_send_ad():
    resp = requests.get('http://glaza.info/board/0-0-91938-0-17')
    soup = bs4.BeautifulSoup(resp.text, 'lxml')
    list_count_of_ads = soup.find_all('div', class_='board-date')
    count_of_ads = len(list_count_of_ads)

    return count_of_ads


if sys.platform != 'linux':
    geckodriver = r'D:\install\programming\python3\selenium\geckodriver.exe'
    options = webdriver.FirefoxOptions()
    options.headless = True
    browser = webdriver.Firefox(executable_path=geckodriver, options=options)
else:
    options = webdriver.FirefoxOptions()
    options.headless = True
    browser = webdriver.Firefox(options=options)
    logging.info('Запускаем драйвер')


for ad_data in glaza_data.data:

    headline = ad_data.get('headline')
    message = ad_data.get('message')
    list_of_pictures = ad_data.get('list_of_pictures')
    phone = ad_data.get('phone')
    price = ad_data.get('price')
    name_of_advertiser = ad_data.get('name_of_advertiser')
    user = ad_data.get('user')
    passw = ad_data.get('passw')
    sity = ad_data.get('sity')

    category = ad_data.get('category')
    type_of_ad = ad_data.get('type_of_ad')
    region_ = ad_data.get('region')

    while True:

        if glaza_data.data.index(ad_data) == 0:
            logging.info('Запуск скрипта')
            auth()
            delete_old_ad()
        send_ad()
        if check_if_send_ad() > 0:
            break
        else:
            continue

browser.quit()
