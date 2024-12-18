
from  selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import time


class SbisContactsPage:
    def __init__(self, browser):
        self.browser = browser
        self.link = "https://sbis.ru/contacts/"
        self.clients_button_xpath = '//*[@id="contacts_clients"]/div[1]/div/div/div[2]/div/a'
        self.sila_people ='//*[@id="container"]/div[1]/div/div[5]/div/div/div[1]/div/p[1]'
        self.anchor_xpath_to_pic = '//*[@id="container"]/div[1]/div/div[5]/div/div/div[1]/div/p[4]/a'
        self.pic_xpath_prefix = 'html/body/div[1]/div/div/div/div[2]/div[1]/div[2]/div[1]/div/div/div[1]/div/div[4]/div[2]/div '
        self.anchor_xpath_to_region = '//*[@id="container"]/div[1]/div/div[3]/div[2]/div[1]/div/div[2]/span/span'
        self.region_button_xpath = '//*[@id="popup"]/div[2]/div/div/div/div/div[2]/div/ul/li[{region_id}]/span/span'
        self.region_partners = 'city-id-2'


    def open(self):
        self.browser.get(self.link)

    def click_clients_button(self):
        self.browser.find_element(By.XPATH, self.clients_button_xpath).click()
        self.browser.switch_to.window(self.browser.window_handles[1])
    def displayed_element(self):
        element = self.browser.find_element(By.XPATH, self. sila_people)
        if element.is_displayed():
            print("Элемент -сила в людях- видим")
        else:
            print("Элемент не видим")

    def click_anchor_to_pic(self):
        anchor = self.browser.find_element(By.XPATH, self.anchor_xpath_to_pic)
        self.browser.execute_script("arguments[0].scrollIntoView(true);", anchor)
        anchor.click()

    def get_pic_size(self, index):
        pic_xpath = f'{self.pic_xpath_prefix}[{index}]/a/div[1]/div'
        WebDriverWait(self.browser, 10)  # Ждем до 10 секунд
        pic_size = self.browser.find_element(By.XPATH, pic_xpath).size
        return pic_size['height'], pic_size['width']


    def click_anchor_to_region(self):
        anchor = self.browser.find_element(By.XPATH, self.anchor_xpath_to_region)
        self.browser.execute_script("arguments[0].click()", anchor)
        # WebDriverWait(self.browser, 10).until(EC.element_to_be_clickable(anchor)).click()
        # anchor.click()
        time.sleep(5)

    def select_region(self, region_id):
        region_button_xpath = self.region_button_xpath.format(region_id=region_id)
        self.browser.find_element(By.XPATH, region_button_xpath).click()
        time.sleep(5)

    def get_current_url(self):
        return self.browser.current_url

    def get_partners(self):
        region_partner=self.browser.find_element(By.ID, self.region_partners)
        return region_partner



