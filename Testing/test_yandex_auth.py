from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pytest
from read_data import load_testing_data

# Формат файла json 4 значения:
# "ИМЯ ПОЛЬЗОВАТЕЛЯ",
# "ПАРОЛЬ",
# 1 - проверка логина, 2 - проверка пароля,
# "Ожидаенмый ответ на странице"
TEST_FILE = 'data/auth.json'


class TestYandexAuth:

    def setup(self):
        self.driver = webdriver.Chrome()

    @pytest.mark.parametrize('login, pswd, type_auth, expect_result', load_testing_data(TEST_FILE))
    def test_yandex_auth(self, login, pswd, type_auth, expect_result):

        # Загрузка страницы авторизации
        self.driver.get("https://passport.yandex.ru/auth?retpath=https%3A%2F%2Fpassport.yandex.ru%2Fprofile&noreturn=1")

        # Проверка на действительный заголовок страницы
        assert "Авторизация" in self.driver.title

        # Ввод данных в поле ЛОГИН
        elem = self.driver.find_element_by_name("login")
        elem.send_keys(login)
        elem.send_keys(Keys.RETURN)

        if type_auth == 1:
            # Проверка на правильность ввода Логина
            assert expect_result not in self.driver.page_source

        else:

            # Ввод данных в поле ПАРОЛЬ и проверка на правильность ввода
            elem = self.driver.switch_to.active_element
            elem.send_keys(pswd)
            elem.send_keys(Keys.RETURN)

            if type_auth == 2:
                assert expect_result not in self.driver.page_source

    def teardown(self):
        self.driver.close()
        self.driver.quit()
