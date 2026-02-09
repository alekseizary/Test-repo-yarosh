from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import time

    # Учётные данные пользователя для dev стенда
URL = 'http://10.5.121.74/login'
USERNAME = 'predbill'
PASSWORD = 'predbill'

    # Настройка браузера Chrome
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
    # Открыть браузер в максимальном размере, если раскоментить то откроется в мах размере
    #driver.maximize_window()
wait = WebDriverWait(driver, 60)

    # Вход в систему predbilling
try:
    driver.get(URL)

    username_field = wait.until(EC.presence_of_element_located((By.ID, "normal_login_username")))
    username_field.send_keys(USERNAME)

    password_field = driver.find_element(By.ID, "normal_login_password")
    password_field.send_keys(PASSWORD)

    driver.find_element(By.CSS_SELECTOR, '.ant-btn.ant-btn-primary.w-100.mb-s').click()

    # Проверка входа - ждем изменения URL
    wait.until_not(EC.url_contains('login'))
    print("✓ Пользователь успешно авторизован в системе predbill (URL изменился)")

    # Переходим в раздел Приборы учета по прямой ссылке из URL
    driver.get('http://10.5.121.74/predbilling/meteringDevicesPredBill')
    print("✓ Открыт раздел Приборы учета")

    # Ждем загрузки страницы и находим поле поиска "Поиск по номеру прибора учета"
    search_field = wait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR,
             "#root > section > section > div > div.mib-profile-control > div.mib-header-right-extra > div > div:nth-child(1) > form > div > div > span")
        )
    )

    # Кликаем по полю поиска "Поиск по номеру прибора учета"
    search_field.click()

    # Вводим серийный номер 198 ПУ в селект "Поиск по номеру прибора учета"
    search_input = search_field.find_element(By.TAG_NAME, "input")
    search_input.clear()
    search_input.send_keys("198")
    time.sleep(2)

    # Нажимаем Enter для поиска значения
    search_input.send_keys(Keys.ENTER)
    print("✓ Введен поисковый запрос '198' и выполнен поиск по sn ПУ")
    time.sleep(6)


    # Находим компонент ФИЛЬТР
    filter_field = wait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR,
            "#root > section > section > div > div.mib-profile-control > div.mib-header-right-extra > div > div:nth-child(4) > span > button")
        )
    )
    # Кликаем компонент фильтр
    filter_field.click()

    # Находим селект "Марка ПУ" Фильтра
    # вводим Марку ПУ
    def wait_to_click(wait, elementSelector):
        element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, elementSelector)))
        if not element:
            return
        element.click()
    def get_input_by_label(driver, elementSelector, label):
        label = driver.find_element(By.CSS_SELECTOR, f'{elementSelector} label[title="{label}"]')
        if not label:
            return
        input_id = label.get_attribute('for')
        input = driver.find_element(By.ID, input_id)
        if not input:
            return
        return input

    def fill_select_by_label(driver, elementSelector, label, value):
        input = get_input_by_label(driver, elementSelector, label)
        if not input:
            return
        input.send_keys(value)
        time.sleep(1)
        option = driver.find_element(By.CSS_SELECTOR, f"{elementSelector} div[title='{value}']")
        if not option:
            return
        option.click()
        time.sleep(2)
        #input.send_keys(Keys.ENTER)

    # Вводим серийный номер 198 ПУ в селект "Поиск по номеру прибора учета"
    # filtersEditorForm идентификатор формы ищем в детулз from
    filter_form_css_selector = '.filtersEditorForm'
    fill_select_by_label(driver, filter_form_css_selector, 'Марка ПУ', 'SA-94')
    ActionChains(driver).send_keys(Keys.TAB).perform()
    fill_select_by_label(driver, filter_form_css_selector, 'АО', 'ВАО')
    ActionChains(driver).send_keys(Keys.TAB).perform()
    fill_select_by_label(driver, filter_form_css_selector, 'Район', 'м.о. Измайлово')


except Exception as e:
    print(f"✗ Произошла ошибка: {e}")

input('Нажми Enter для закрытия браузера')
driver.quit()
