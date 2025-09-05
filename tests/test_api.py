import sys
import os
# Добавляем корневую папку в путь для импорта
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import requests
import allure
import pytest
from config import KINOPOISK_API_KEY, KINOPOISK_API_URL

@allure.epic("API Tests")
@allure.feature("Поиск фильмов")
class TestKinopoiskAPI:

    @pytest.fixture(autouse=True)
    def setup_api(self):
        """Фикстура для настройки API-запросов"""
        self.headers = {"X-API-KEY": KINOPOISK_API_KEY}
        self.base_url = KINOPOISK_API_URL
        yield

    @pytest.mark.api
    @allure.title("Поиск фильма по ID")
    def test_search_movie_by_id(self):
        with allure.step("Отправка GET-запроса для поиска по ID"):
            result = requests.get(
                f"{self.base_url}/movie?page=1&limit=1&id=5304403",
                headers=self.headers
            )
        assert result.status_code == 200

    @pytest.mark.api
    @allure.title("Поиск фильма по названию")
    def test_search_movie_by_name(self):
        with allure.step("Отправка GET-запроса для поиска по названию"):
            result = requests.get(
                f"{self.base_url}/movie/search?page=1&limit=1&query=Брат",
                headers=self.headers
            )
        assert result.status_code == 200

    @pytest.mark.api
    @allure.title("Поиск фильма по жанру")
    def test_search_movie_by_genre(self):
        with allure.step("Отправка GET-запроса для поиска по жанру"):
            result = requests.get(
                f"{self.base_url}/movie?page=1&limit=1&year=2023&genres.name=криминал",
                headers=self.headers
            )
        assert result.status_code == 200

    @pytest.mark.api
    @allure.title("Поиск фильма по рейтингу")
    def test_search_movie_by_rating(self):
        with allure.step("Отправка GET-запроса для поиска по рейтингу"):
            result = requests.get(
                f"{self.base_url}/movie?page=1&limit=1&rating.imdb=8-10",
                headers=self.headers
            )
        assert result.status_code == 200

    @pytest.mark.api
    @allure.title("Поиск фильма по возрастному ограничению")
    def test_search_movie_by_age_rating(self):
        with allure.step("Отправка GET-запроса для поиска по возрастному ограничению"):
            result = requests.get(
                f"{self.base_url}/movie?page=1&limit=1&ageRating=18",
                headers=self.headers
            )
        assert result.status_code == 200