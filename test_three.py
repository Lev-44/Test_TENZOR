from selenium import webdriver
from selenium.webdriver.common.by import By
import pytest
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import requests
import time
import logging

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
# Создаем обработник для записи в файл
file_handler = logging.FileHandler('test3.log', mode='w')
file_handler.setLevel(logging.DEBUG)
file_formatter = logging.Formatter('%(asctime)s - '
                                   '%(name)s - %(levelname)s - '
                                   '%(message)s')
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.debug("This is a harmless debug Message")

# Опции для Chrome
chromeOptions = Options()
prefs = {"download.default_directory": r"C:\Python_progect_sobes\TEST_Project"}
chromeOptions.add_experimental_option("prefs", prefs)


class SbisPage:
    def __init__(self, browser):
        self.browser = browser
        self.link = "https://sbis.ru/"
        self.footer_xpath_to_file = ('//*[@id="container"]/div[2]/'
                                     'div[1]/div[3]/div[3]/ul/li[9]/a')
        self.for_windows = ('/html/body/div[1]/div[2]/'
                            'div[1]/div/div[1]/div/div/'
                            'div/div[2]/div/div[1]/div/div/'
                            'div[1]/div/div[1]/div[1]/div/div/span')
        self.download_step = 'sbis_ru-DownloadNew-loadLink'
        self.download_dir = 'C:\\Python_progect_sobes\\TEST_Project'
        self.file_path = ('C:\\Python_progect_sobes\\'
                          'TEST_Project\\sbisplugin-setup-web.exe')
        self.url_path = ('https://update.sbis.ru/'
                         'Sbis3Plugin/master/win32/'
                         'sbisplugin-setup-web.exe')

    def open(self):
        self.browser.get(self.link)

    def click_button_to_local(self):
        local_ver = WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, self.footer_xpath_to_file))
        )
        self.browser.execute_script(
            "arguments[0].scrollIntoView(true);", local_ver)
        local_ver.click()

    def selected_element(self):

        element = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.XPATH, self.for_windows)))
        if element.is_enabled():
            print("Элемент -windows- выбран")
        else:
            print("Элемент не выбран")

    def wait_for_download(self):
        filename = 'sbisplugin-setup-web.exe'
        while True:
            time.sleep(6)
            if filename in os.listdir(self.download_dir):
                print(f"Файл '{filename}' успешно загружен.")
                break  # Выходим из цикла, если файл найден

    def click_button_download(self):

        download = WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, self.download_step)))
        download.click()
        WebDriverWait(chrome_browser, 10)

    def get_local_file_size(file_path):
        return os.path.getsize(file_path)

    def get_file_size_from_url(self):
        response = requests.head(self.url_path, allow_redirects=True)
        WebDriverWait(chrome_browser, 10)
        response.raise_for_status()
        if response.status_code == 200:
            # Получаем размер файла из заголовков
            return int(response.headers.get('Content-Length'))
        else:
            raise Exception(f"Не удалось получить информацию о файле:"
                            f" {response.status_code}")

    def get_file_size(self):
        return os.path.getsize(self.file_path)


@pytest.fixture(scope="module")
def chrome_browser():
    browser = (webdriver.Chrome
               (service=ChromeService
                (ChromeDriverManager().install()),
                options=chromeOptions)
               )
    browser.maximize_window()
    yield browser
    browser.quit()


def test_download(chrome_browser):
    page = SbisPage(chrome_browser)
    page.open()
    page.click_button_to_local()
    page.selected_element()
    page.click_button_download()
    page.wait_for_download()
    WebDriverWait(chrome_browser, 50)
    # Проверка размера файла
    local_file_size = page.get_file_size()
    download_file_size = page.get_file_size_from_url()
    assert download_file_size == local_file_size, \
        "Размеры файлов не совпадают!"
    print('Размеры файлов совпадают!!!')
    # Удаление файла после проверки
    WebDriverWait(chrome_browser, 50)
    os.remove('C:\\Python_progect_sobes'
              '\\TEST_Project'
              '\\sbisplugin-setup-web.exe')
    logger.info('TEST IS END AND VERY WELL')
