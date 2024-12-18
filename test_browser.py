import logging
import time
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# Создаем обработник для записи в файл
file_handler = logging.FileHandler('test.log', mode='w')
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

# Тестовые сообщения
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

    def test_pic_sizes(self, browser):
        logger.info('ZAPUSK TESTA ')
        page = SbisContactsPage(browser)
        page.open()
        page.click_clients_button()
        time.sleep(3)
        page.displayed_element()
        page.click_anchor_to_pic()
        current_url = browser.current_url
        assert current_url == 'https://tensor.ru/about',f'Ожидался URL: https://tensor.ru/abou, но был: {current_url}'



        pic1_height, pic1_width = page.get_pic_size(1)
        pic2_height, pic2_width = page.get_pic_size(2)
        pic3_height, pic3_width = page.get_pic_size(3)
        pic4_height, pic4_width = page.get_pic_size(4)

        assert pic1_width == pic2_width == pic3_width == pic4_width, 'ширина фото разная'
        assert pic1_height == pic2_height == pic3_height == pic4_height, 'высота фото разная'

        logger.info('TEST IS END AND VERY WELL')

