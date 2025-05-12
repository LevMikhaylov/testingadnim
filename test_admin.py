from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

class OpenCartAdminPanelTest:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.driver.get("https://demo.opencart.com/admin/")
        self.login()

    def login(self):
        username = self.driver.find_element(By.NAME, "username")
        password = self.driver.find_element(By.NAME, "password")
        username.send_keys("demo")  
        password.send_keys("demo") 
        password.send_keys(Keys.RETURN)
        time.sleep(2)  # Ждем загрузки страницы

    def create_category(self):
        self.driver.find_element(By.LINK_TEXT, "Catalog").click()
        self.driver.find_element(By.LINK_TEXT, "Categories").click()
        self.driver.find_element(By.LINK_TEXT, "Add New").click()

        self.driver.find_element(By.NAME, "name[1]").send_keys("Devices")  # Название категории
        self.driver.find_element(By.NAME, "description[1]").send_keys("Devices category description")  # Описание категории

        self.driver.find_element(By.CSS_SELECTOR, "button[data-original-title='Save']").click()
        time.sleep(2)

    def add_product(self, product_name, product_description, product_model):
        self.driver.find_element(By.LINK_TEXT, "Catalog").click()
        self.driver.find_element(By.LINK_TEXT, "Products").click()
        self.driver.find_element(By.LINK_TEXT, "Add New").click()

        self.driver.find_element(By.NAME, "name[1]").send_keys(product_name)
        self.driver.find_element(By.NAME, "description[1]").send_keys(product_description)
        self.driver.find_element(By.NAME, "model").send_keys(product_model)

        # Выбор категории
        self.driver.find_element(By.LINK_TEXT, "Data").click()
        self.driver.find_element(By.NAME, "category[]").send_keys("Devices")  
        time.sleep(1)
        self.driver.find_element(By.NAME, "category[]").send_keys(Keys.RETURN)

        self.driver.find_element(By.CSS_SELECTOR, "button[data-original-title='Save']").click()
        time.sleep(2)

    def search_product(self, product_name):
        self.driver.get("https://demo.opencart.com/") 
        search_box = self.driver.find_element(By.NAME, "search")
        search_box.send_keys(product_name)
        search_box.send_keys(Keys.RETURN)
        time.sleep(2)

        assert product_name in self.driver.page_source, f"{product_name} не найден на главной странице"

    def delete_product(self, product_name):
        self.driver.find_element(By.LINK_TEXT, "Catalog").click()
        self.driver.find_element(By.LINK_TEXT, "Products").click()

        # Поиск продукта для удаления
        search_box = self.driver.find_element(By.NAME, "filter_name")
        search_box.send_keys(product_name)
        search_box.send_keys(Keys.RETURN)
        time.sleep(2)

        self.driver.find_element(By.CSS_SELECTOR, "input[type='checkbox']").click()  # Выбираем продукт
        self.driver.find_element(By.CSS_SELECTOR, "button[data-original-title='Delete']").click()
        self.driver.switch_to.alert.accept()  # Подтверждение удаления
        time.sleep(2)

    def run_tests(self):
        self.create_category()
        self.add_product("Mouse 1", "Description for Mouse 1", "Model 1")
        self.add_product("Mouse 2", "Description for Mouse 2", "Model 2")
        self.add_product("Keyboard 1", "Description for Keyboard 1", "Model 3")
        self.add_product("Keyboard 2", "Description for Keyboard 2", "Model 4")

        self.search_product("Mouse 1")
        self.search_product("Mouse 2")
        self.search_product("Keyboard 1")
        self.search_product("Keyboard 2")

        self.delete_product("Mouse 1")
        self.delete_product("Keyboard 1")

        # Проверка оставшихся товаров
        self.search_product("Mouse 2")
        self.search_product("Keyboard 2")

    def close(self):
        self.driver.quit()

if __name__ == "__main__":
    test = OpenCartAdminPanelTest()
    try:
        test.run_tests()
    finally:
        test.close()
