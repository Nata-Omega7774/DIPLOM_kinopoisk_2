import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import allure
import pytest
from config import KINOPOISK_UI_URL, BROWSER_IMPLICIT_WAIT


@allure.epic("UI Tests")
@allure.feature("Функциональность сайта Кинопоиск")
class TestKinopoiskUI:

    @pytest.fixture(autouse=True)
    def setup(self):
        """Фикстура для настройки браузера"""
        with allure.step("Инициализация браузера Chrome"):
            self.driver = webdriver.Chrome()
            self.driver.maximize_window()
            self.driver.implicitly_wait(BROWSER_IMPLICIT_WAIT)

        with allure.step("Открытие главной страницы Кинопоиска"):
            self.driver.get(KINOPOISK_UI_URL)

        yield

        with allure.step("Закрытие браузера"):
            self.driver.quit()

    @pytest.mark.ui
    @allure.title("Проверка ограничения доступа для неавторизованных пользователей")
    @allure.description("Попытка просмотра фильма без авторизации должна запрашивать вход")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_authorization_requirement(self):
        with allure.step("Вводим 'Брат' в поисковую строку"):
            search_input = self.driver.find_element(By.NAME, "kp_query")
            search_input.send_keys("Брат")

        with allure.step("Нажимаем кнопку поиска"):
            search_button = self.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
            search_button.click()

        with allure.step("Ожидаем загрузки результатов поиска"):
            film_link = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '[href*="/film/41519"]'))
            )

        with allure.step("Переходим на страницу фильма"):
            film_link.click()

        with allure.step("Нажимаем кнопку просмотра фильма"):
            watch_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-test-id="Offer"]'))
            )
            watch_button.click()

        with allure.step("Проверяем сообщение о необходимости авторизации"):
            auth_message = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, '.WelcomePage-tagline'))
            )
            assert "Войдите или зарегистрируйтесь" in auth_message.text

    @pytest.mark.ui
    @allure.title("Просмотр информации о фильме")
    @allure.description("Поиск и проверка отображения информации о фильме 'Брат'")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_movie_information_display(self):
        with allure.step("Вводим 'Брат' в поисковую строку"):
            search_input = self.driver.find_element(By.NAME, "kp_query")
            search_input.send_keys("Брат")

        with allure.step("Нажимаем кнопку поиска"):
            search_button = self.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
            search_button.click()

        with allure.step("Ожидаем загрузки результатов поиска"):
            film_link = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '[href*="/film/41519"]'))
            )

        with allure.step("Переходим на страницу фильма"):
            film_link.click()

        with allure.step("Проверяем отображение заголовка фильма"):
            page_title = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.TAG_NAME, 'h1'))
            )
            assert "Брат" in page_title.text

    @pytest.mark.ui
    @allure.title("Поиск фильма по кириллическому названию")
    @allure.description("Поиск фильма по названию на русском языке")
    @allure.severity(allure.severity_level.NORMAL)
    def test_search_by_cyrillic_name(self):
        with allure.step("Вводим кириллическое название 'Брат' в поисковую строку"):
            search_input = self.driver.find_element(By.NAME, "kp_query")
            search_input.send_keys("Брат")

        with allure.step("Нажимаем кнопку поиска"):
            search_button = self.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
            search_button.click()

        with allure.step("Проверяем результаты поиска"):
            results_text = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, '.search_results_topText'))
            )
            assert "Брат" in results_text.text

    @pytest.mark.ui
    @allure.title("Поиск фильма по латинскому названию")
    @allure.description("Поиск фильма по названию на английском языке")
    @allure.severity(allure.severity_level.NORMAL)
    def test_search_by_latin_name(self):
        with allure.step("Вводим латинское название 'Brat' в поисковую строку"):
            search_input = self.driver.find_element(By.NAME, "kp_query")
            search_input.send_keys("Brat")

        with allure.step("Нажимаем кнопку поиска"):
            search_button = self.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
            search_button.click()

        with allure.step("Проверяем результаты поиска"):
            results_text = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, '.search_results_topText'))
            )
            assert "Brat" in results_text.text

    @pytest.mark.ui
    @allure.title("Поиск с пустым запросом")
    @allure.description("Проверка поведения поиска при пустом запросе")
    @allure.severity(allure.severity_level.MINOR)
    def test_search_with_empty_query(self):
        with allure.step("Оставляем поисковую строку пустой"):
            search_input = self.driver.find_element(By.NAME, "kp_query")
            search_input.send_keys("")

        with allure.step("Нажимаем кнопку поиска"):
            search_button = self.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
            search_button.click()

        with allure.step("Проверяем отображение поисковой страницы"):
            search_element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, 'search'))
            )
            assert search_element.is_displayed()