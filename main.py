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
        option = driver.find_element(By.CSS_SELECTOR, f"div[title='{value}']")
        if not option:
            return
        option.click()
        time.sleep(2)
        #input.send_keys(Keys.ENTER)

    ##################################Выбор элемента по индексу
    # def selection_index(label, index, driver):
    #
    #     input_field = get_input_by_label(driver, '.filtersEditorForm', label)
    #
    #     input_field.click()
    #     time.sleep(1)
    #
    #     type_object_dropdown = driver.find_element(By.CSS_SELECTOR,
    #                                                '.ant-select-dropdown:not(.ant-select-dropdown-hidden)')
    #
    #     # Получаем значения полученного списка селекта
    #     options = type_object_dropdown.find_elements(By.CSS_SELECTOR, '.ant-select-item-option')
    #
    #     # Выбираем второй элемент в списке 'Тип объекта'
    #     options[index].click()


    #ВВОДИМ ЗНАЧЕНИЯ В ПОЛЕ АДРЕС
    def process_address_field():
        try:
            print("Обрабатываем поле: Адрес")

            # Селектор для поля адреса
            address_selector = "body > div:nth-child(4) > div > div.ant-drawer-content-wrapper > div > div > div > form > div > div:nth-child(3)"
            address_input_selector = "body > div:nth-child(4) > div > div.ant-drawer-content-wrapper > div > div > div > form > div > div:nth-child(3) > div.ant-col.ant-col-14.ant-form-item-control > div > div > div > div.searchableSelectPopup > div.searchableSelectPopupInsider > div.searchBox.Адрес > input"
            address_list_selector = "body > div:nth-child(4) > div > div.ant-drawer-content-wrapper > div > div > div > form > div > div:nth-child(3) > div.ant-col.ant-col-14.ant-form-item-control > div > div > div > div.searchableSelectPopup > div.searchableSelectPopupInsider > div.searchBox.Адрес > ul"
            address_value = "10-я Парковая ул., вл.3-7"

            # Кликаем на поле адреса
            address_field = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, address_selector))
            )
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", address_field)
            time.sleep(0.5)
            address_field.click()
            time.sleep(1.5)

            # Вводим адрес
            address_input = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, address_input_selector))
            )
            address_input.clear()
            time.sleep(0.3)
            address_input.send_keys(address_value)
            time.sleep(3)

            # Выбираем из списка
            address_list = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, address_list_selector))
            )
            address_items = address_list.find_elements(By.TAG_NAME, "li")

            if address_items:
                first_item = address_items[1]
                first_item.click()
                time.sleep(0.5)

                # Закрываем список
                #actions = ActionChains(driver)
                #actions.send_keys(Keys.ESCAPE).perform()
                print("Адрес заполнен")
                return True
            else:
                print("Список адресов пуст")
                return False
        except Exception as e:
            print(f"Ошибка: {e}")
            return False


    # ВВОД ЗНАЧЕНИЙ В ФИЛЬТР
    # filtersEditorForm идентификатор формы ищем в детулз from
    filter_form_css_selector = '.filtersEditorForm'
    fill_select_by_label(driver, filter_form_css_selector, 'Марка ПУ', 'SA-94')
    ActionChains(driver).send_keys(Keys.ESCAPE ).perform()

    #ЗАПУСК(вызов) ФУНКЦИИ ВВОД АДРЕСА
    process_address_field()

    #ActionChains(driver).send_keys(Keys.TAB).perform()
    fill_select_by_label(driver, filter_form_css_selector, 'АО', 'ВАО')
    fill_select_by_label(driver, filter_form_css_selector, 'Район', 'м.о. Измайлово')
    fill_select_by_label(driver, filter_form_css_selector, 'Филиал', '04')
    fill_select_by_label(driver, filter_form_css_selector, 'Предприятие', '03')

    #ActionChains(driver).send_keys(Keys.TAB).perform()

    #################################Вызов функции заполнение селекта Тип объекта
    selection_index('Тип объекта', 2, driver)



    fill_select_by_label(driver, filter_form_css_selector, 'Тип ПУ', 'Теплосчетчик')
    fill_select_by_label(driver, filter_form_css_selector, 'Тип ТУ', 'ТЭ')

    ActionChains(driver).send_keys(Keys.TAB).perform()

    #Находим поле "Номер ТП"
    heatPointNumber = wait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR,
             "body > div:nth-child(4) > div > div.ant-drawer-content-wrapper > div > div > div > form > div > div:nth-child(11) > div.ant-col.ant-col-14.ant-form-item-control > div > div > span")
        )
    )

    # Кликаем по полю "Номер ТП"
    heatPointNumber.click()

    #Вводим номер тп 20-06-0604/008 в поле "Номер ТП"
    heatPointNumber = heatPointNumber.find_element(By.TAG_NAME, "input")
    heatPointNumber.clear()
    heatPointNumber.send_keys("20-06-0604/008")
    time.sleep(2)


    #Выбираем значение поля "БП" (строки 160-173)
    # Ищем поле ввода "БП" (1-й аргумент)
    input_field = get_input_by_label(driver, filter_form_css_selector, 'БП')

    input_field.click()
    time.sleep(1)

    # Ищем выпадающий список селекта "БП"
    # consumerTypeCode - переменная
    consumerTypeCode = driver.find_element(By.CSS_SELECTOR, '.ant-select-dropdown:not(.ant-select-dropdown-hidden)')

    # Получаем значения полученного списка селекта
    options = consumerTypeCode.find_elements(By.CSS_SELECTOR, '.ant-select-item-option')

    #Выбираем первый элемент в списке 'БП'
    options[1].click()

    fill_select_by_label(driver, filter_form_css_selector, 'Тип учёта ПУ на ТП', 'Технологический')
    ActionChains(driver).send_keys(Keys.TAB).perform()

    #Находим поле "Номер ГИС ЖКХ (ЦО/ТЭ)"
    numberGisTe = wait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR,
             "body > div:nth-child(4) > div > div.ant-drawer-content-wrapper > div > div > div > form > div > div:nth-child(15) > div.ant-col.ant-col-14.ant-form-item-control > div > div > span")
        )
    )
    # Кликаем по полю "Номер ГИС ЖКХ (ЦО/ТЭ)"
    numberGisTe.click()

    #Вводим номер 834 в поле "Номер ГИС ЖКХ (ЦО/ТЭ)"
    numberGisTe = numberGisTe.find_element(By.TAG_NAME, "input")
    numberGisTe.clear()
    numberGisTe.send_keys("834")
    time.sleep(1)

    #Находим поле "Номер ГИС ЖКХ (ГВС)"
    numberGisGvs = wait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR,
             "body > div:nth-child(4) > div > div.ant-drawer-content-wrapper > div > div > div > form > div > div:nth-child(16) > div.ant-col.ant-col-14.ant-form-item-control > div > div > span")
        )
    )
    # Кликаем по полю "Номер ГИС ЖКХ (ЦО/ТЭ)"
    numberGisGvs.click()

    #Вводим номер 835 в поле "Номер ГИС ЖКХ (ГВС)"
    numberGisGvs = numberGisGvs.find_element(By.TAG_NAME, "input")
    numberGisGvs.clear()
    numberGisGvs.send_keys("835")
    time.sleep(1)

    fill_select_by_label(driver, filter_form_css_selector, 'Прибор МВК', 'Нет')


    # Ищем поле ввода "Виртуальный" (1-й аргумент)
    input_field = get_input_by_label(driver, filter_form_css_selector, 'Виртуальный')

    input_field.click()
    time.sleep(1)

    # Ищем выпадающий список селекта "Виртуальный"
    # signVirtual - переменная
    signVirtual = driver.find_element(By.CSS_SELECTOR, '.ant-select-dropdown:not(.ant-select-dropdown-hidden)')

    # Получаем значения полученного списка селекта "Виртуальный"
    options = signVirtual.find_elements(By.CSS_SELECTOR, '.ant-select-item-option')

    #Выбираем первый элемент в списке 'Виртуальный'
    options[1].click()


    #Ищем поле ввода "Сальдирующий" (1-й аргумент)
    input_field = get_input_by_label(driver, filter_form_css_selector, 'Сальдирующий')

    input_field.click()
    time.sleep(1)

    # Ищем выпадающий список селекта "Сальдирующий"
    # signSaldo - переменная
    signSaldo = driver.find_element(By.CSS_SELECTOR, '.ant-select-dropdown:not(.ant-select-dropdown-hidden)')

    # Получаем значения полученного списка селекта "Сальдирующий"
    options = signSaldo.find_elements(By.CSS_SELECTOR, '.ant-select-item-option')

    #Выбираем первый элемент в списке "Сальдирующий"
    options[1].click()


    # КЛИКАЕМ ПО СИНЕЙ ГАЛКЕ для применения выбранных значений в селектах фильтра
    apply_button = wait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR,
            "div.filterHeaderRow > div.filterOperations > button:nth-child(1)")
        )
    )
    print(apply_button)
    apply_button.click()

    input()
    #ActionChains(driver).send_keys(Keys.ENTER).perform()

    filter_field_new = wait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR,
            "#root > section > section > div > div.mib-profile-control > div.mib-header-right-extra > div > div:nth-child(4) > span > button")
        )
    )
    time.sleep(2)
    filter_field_new.click()

except Exception as e:
    print(f"✗ Произошла ошибка: {e}")

input('Нажми Enter для закрытия браузера')
driver.quit()
