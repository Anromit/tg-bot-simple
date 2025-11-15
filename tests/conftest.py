import pytest
import sys
import os

# Добавляем корневую директорию в путь Python
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


@pytest.fixture
def db_module():
    """Фикстура для модуля базы данных"""
    import db
    return db


@pytest.fixture
def main_module():
    """Фикстура для основного модуля"""
    import main
    return main


@pytest.fixture
def openrouter_module():
    """Фикстура для модуля OpenRouter"""
    import openrouter_client
    return openrouter_client


@pytest.fixture
def tmp_db_path(tmp_path):
    """Фикстура для временного пути к базе данных"""
    return tmp_path / "test.db"