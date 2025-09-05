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
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.implicitly_wait(BROWSER_IMPLICIT_WAIT)
        self.driver.get(KINOPOISK_UI_URL)
        yield
        self.driver.quit()

    @pytest.mark.ui
    @allure.title("Проверка ограничения доступа для неавторизованных пользователей")
    def test_authorization_requirement(self):
        search_input = self.driver.find_element(By.NAME, "kp_query")
        search_input.send_keys("Брат")
        search_button = self.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
        search_button.click()

        film_link = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '[href*="/film/41519"]'))
        )
        film_link.click()

        watch_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-test-id="Offer"]'))
        )
        watch_button.click()

        auth_message = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, '.WelcomePage-tagline'))
        )
        assert "Войдите или зарегистрируйтесь" in auth_message.text

    @pytest.mark.ui
    @allure.title("Просмотр информации о фильме")
    def test_movie_information_display(self):
        search_input = self.driver.find_element(By.NAME, "kp_query")
        search_input.send_keys("Брат")
        search_button = self.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
        search_button.click()

        film_link = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '[href*="/film/41519"]'))
        )
        film_link.click()

        page_title = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.TAG_NAME, 'h1'))
        )
        assert "Брат" in page_title.text

    @pytest.mark.ui
    @allure.title("Поиск фильма по кириллическому названию")
    def test_search_by_cyrillic_name(self):
        search_input = self.driver.find_element(By.NAME, "kp_query")
        search_input.send_keys("Брат")
        search_button = self.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
        search_button.click()

        results_text = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, '.search_results_topText'))
        )
        assert "Брат" in results_text.text

    @pytest.mark.ui
    @allure.title("Поиск фильма по латинскому названию")
    def test_search_by_latin_name(self):
        search_input = self.driver.find_element(By.NAME, "kp_query")
        search_input.send_keys("Brat")
        search_button = self.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
        search_button.click()

        results_text = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, '.search_results_topText'))
        )
        assert "Brat" in results_text.text

    @pytest.mark.ui
    @allure.title("Поиск с пустым запросом")
    def test_search_with_empty_query(self):
        search_input = self.driver.find_element(By.NAME, "kp_query")
        search_input.send_keys("")
        search_button = self.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
        search_button.click()

        search_element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, 'search'))
        )
        assert search_element.is_displayed()
