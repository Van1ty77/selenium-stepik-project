Selenium Test Automation
Проект автоматизации тестирования интернет-магазина.

Технологии
  -Python 3

  -Selenium

  -PyTest

  -Page Object Pattern

Установка
  Установите зависимости:

    bash
    pip install -r requirements.txt
    Установите ChromeDriver

Структура проекта
  pages/ - классы страниц

  tests/ - тесты

  conftest.py - настройки тестов

Запуск тестов
  bash
  # Все тесты
  pytest tests/

  # Тесты главной страницы
  pytest tests/test_main_page.py

  # Тесты страницы товара
  pytest tests/test_product_page.py
Что тестируется
  Добавление товаров в корзину

  Регистрация пользователей

  Проверка корзины

  Навигация по сайту
