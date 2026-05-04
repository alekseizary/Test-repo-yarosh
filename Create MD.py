from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import time

# Данные для авторизации
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


    # Находим МЕНЮ ДЕЙСТВИЕ. Объявляю переменную = menu_action
    menu_action = wait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR,
             "#root > section > section > div > div.ant-space.ant-space-horizontal.ant-space-align-center > div > div > div > button > div > div:nth-child(1) > span > svg")
        )
    )

    #Кликаем по Меню Действие (вызов функции)
    menu_action.click()

    #Находим кнопку "Создать", указываем селектор кнопки "создать"
    create = wait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR,
             "html > div > div > div > ul > li:nth-child(1)")
        )
    )
    # Кликаем по кнопке "Создать"
    create.click()


except Exception as e:
    print(f"✗ Произошла ошибка: {e}")

input('Нажми Enter для закрытия браузера')
driver.quit()