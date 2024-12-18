import logging
import time
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager


logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# Создаем обработник для записи в файл
file_handler = logging.FileHandler('test.logo', mode='w')
file_handler.setLevel(logging.DEBUG)
file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(file_formatter)

# Создаем обработник для вывода в консоль
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(console_formatter)

# Добавляем обработчики к логгеру
logger.addHandler(file_handler)
logger.addHandler(console_handler)

# Тестовые сообщения логгера
logger.debug("This is a harmless debug Message")
logger.info("This is just an information")
logger.warning("It is a Warning. Please make changes")
logger.error("You are trying to divide by zero")
logger.critical("Internet is down")



@pytest.fixture(scope="module")# Определяем фикстуру для браузера с областью действия "module"
def browser():
    browser = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))#созд экземпляр браузера Chrome
    yield browser#морозимся и возвр браузер
    browser.quit()#все закр после теста

from page.sbis_contacts import SbisContactsPage
class TestSbisContactsPage:

    def test_region_navigation(self, browser):
        logger.info('ZAPUSK TESTA ')
        page = SbisContactsPage(browser)
        page.open()
        now_partners44 = page.get_partners()
        logger.info(' TEST ')
        # Проверяем, что элемент найден
        if now_partners44:
            # Получаем текст элемента
            element_text = now_partners44.text
            print(f"Текст элемента: {element_text}")
            assert element_text == 'Кострома'
        current_url_44reg = page.get_current_url()
        assert current_url_44reg == 'https://sbis.ru/contacts/44-kostromskaya-oblast?tab=clients'
        time.sleep(5)
        page.click_anchor_to_region()

        time.sleep(3)
        page.select_region(43)
        time.sleep(3)
        now_partners41 = page.get_partners()
        if now_partners41:
            # Получаем текст элемента
            element_text = now_partners41.text
            print(f"Текст элемента: {element_text}")
            assert element_text == "Петропавловск-Камчатский"
        current_url_41reg = page.get_current_url()
        assert current_url_41reg == 'https://sbis.ru/contacts/41-kamchatskij-kraj?tab=clients'

        logger.info('TEST IS END AND VERY WELL')