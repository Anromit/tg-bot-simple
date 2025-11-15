import responses
import pytest
import os
import requests  # Добавляем импорт requests


@responses.activate
def test_chat_once_success(openrouter_module, monkeypatch):
    """Проверка успешного сценария использования клиента"""
    openrouter = openrouter_module

    # Устанавливаем тестовый API ключ
    monkeypatch.setenv("OPENROUTER_API_KEY", "test-api-key")

    # Задаем URL OpenRouter'а
    url = "https://openrouter.ai/api/v1/chat/completions"

    # Через responses.add регистрируем фейковый HTTP-ответ
    responses.add(
        responses.POST,
        url,
        json={
            "choices": [
                {
                    "message": {
                        "content": "Тестовый ответ от ИИ"
                    }
                }
            ]
        },
        status=200
    )

    # Вызываем chat_once() и проверяем результат
    messages = [{"role": "user", "content": "Тестовый вопрос"}]
    text, response_time = openrouter.chat_once(messages, model="test-model")

    # Проверяем соответствие контракту
    assert text == "Тестовый ответ от ИИ"
    assert isinstance(response_time, int)
    assert response_time >= 0


@responses.activate
def test_chat_once_401_error(openrouter_module, monkeypatch):
    """Тестируем обработку ошибки HTTP 401 (Unauthorized)"""
    openrouter = openrouter_module

    # Устанавливаем тестовый API ключ
    monkeypatch.setenv("OPENROUTER_API_KEY", "test-api-key")

    url = "https://openrouter.ai/api/v1/chat/completions"

    # Регистрируем ответ (status=401)
    responses.add(
        responses.POST,
        url,
        status=401
    )

    # Вызываем chat_once() и проверяем результат
    messages = [{"role": "user", "content": "Тестовый вопрос"}]

    with pytest.raises(openrouter.OpenRouterError) as exc_info:
        openrouter.chat_once(messages, model="test-model")

    # Проверяем соответствие контракту
    error_str = str(exc_info.value)
    assert "401" in error_str
    assert "Ключ OpenRouter отклонён" in error_str


@responses.activate
def test_chat_once_429_error(openrouter_module, monkeypatch):
    """Тестируем обработку ошибки HTTP 429 (Too Many Requests)"""
    openrouter = openrouter_module

    # Устанавливаем тестовый API ключ
    monkeypatch.setenv("OPENROUTER_API_KEY", "test-api-key")

    url = "https://openrouter.ai/api/v1/chat/completions"

    # Регистрируем ответ (status=429)
    responses.add(
        responses.POST,
        url,
        status=429
    )

    # Вызываем chat_once() и проверяем результат
    messages = [{"role": "user", "content": "Тестовый вопрос"}]

    with pytest.raises(openrouter.OpenRouterError) as exc_info:
        openrouter.chat_once(messages, model="test-model")

    # Проверяем соответствие контракту
    error_str = str(exc_info.value)
    assert "429" in error_str
    assert "Превышены лимиты" in error_str


@responses.activate
def test_chat_once_500_error(openrouter_module, monkeypatch):
    """Тестируем обработку ошибки HTTP 5xx (Server Error)"""
    openrouter = openrouter_module

    # Устанавливаем тестовый API ключ
    monkeypatch.setenv("OPENROUTER_API_KEY", "test-api-key")

    url = "https://openrouter.ai/api/v1/chat/completions"

    # Регистрируем ответ (status=500)
    responses.add(
        responses.POST,
        url,
        status=500
    )

    # Вызываем chat_once() и проверяем результат
    messages = [{"role": "user", "content": "Тестовый вопрос"}]

    with pytest.raises(openrouter.OpenRouterError) as exc_info:
        openrouter.chat_once(messages, model="test-model")

    # Проверяем соответствие контракту
    error_str = str(exc_info.value)
    assert "500" in error_str
    assert "Внутренняя ошибка сервера" in error_str


@responses.activate
def test_chat_once_connection_error(openrouter_module, monkeypatch):
    """Тестируем обработку сетевых ошибок"""
    openrouter = openrouter_module

    # Устанавливаем тестовый API ключ
    monkeypatch.setenv("OPENROUTER_API_KEY", "test-api-key")

    url = "https://openrouter.ai/api/v1/chat/completions"

    # Регистрируем ConnectionError
    responses.add(
        responses.POST,
        url,
        body=requests.exceptions.ConnectionError("Connection failed")
    )

    # Вызываем chat_once() и проверяем результат
    messages = [{"role": "user", "content": "Тестовый вопрос"}]

    with pytest.raises(openrouter.OpenRouterError) as exc_info:
        openrouter.chat_once(messages, model="test-model")

    # Проверяем соответствие контракту
    error_str = str(exc_info.value)
    assert "503" in error_str
    assert "Ошибка подключения" in error_str


@responses.activate
def test_chat_once_timeout_error(openrouter_module, monkeypatch):
    """Тестируем обработку таймаута"""
    openrouter = openrouter_module

    # Устанавливаем тестовый API ключ
    monkeypatch.setenv("OPENROUTER_API_KEY", "test-api-key")

    url = "https://openrouter.ai/api/v1/chat/completions"

    # Регистрируем Timeout
    responses.add(
        responses.POST,
        url,
        body=requests.exceptions.Timeout("Request timeout")
    )

    # Вызываем chat_once() и проверяем результат
    messages = [{"role": "user", "content": "Тестовый вопрос"}]

    with pytest.raises(openrouter.OpenRouterError) as exc_info:
        openrouter.chat_once(messages, model="test-model")

    # Проверяем соответствие контракту
    error_str = str(exc_info.value)
    assert "408" in error_str
    assert "Таймаут запроса" in error_str


@responses.activate
def test_chat_once_invalid_response(openrouter_module, monkeypatch):
    """Тестируем обработку некорректного ответа от API"""
    openrouter = openrouter_module

    # Устанавливаем тестовый API ключ
    monkeypatch.setenv("OPENROUTER_API_KEY", "test-api-key")

    url = "https://openrouter.ai/api/v1/chat/completions"

    # Регистрируем ответ с некорректной структурой
    responses.add(
        responses.POST,
        url,
        json={
            "invalid": "structure"  # Нет поля "choices"
        },
        status=200
    )

    # Вызываем chat_once() и проверяем результат
    messages = [{"role": "user", "content": "Тестовый вопрос"}]

    with pytest.raises(openrouter.OpenRouterError) as exc_info:
        openrouter.chat_once(messages, model="test-model")

    # Проверяем соответствие контракту
    error_str = str(exc_info.value)
    assert "500" in error_str
    assert "Неожиданная структура ответа" in error_str


def test_chat_once_no_api_key(openrouter_module, monkeypatch):
    """Тестируем обработку отсутствия API ключа"""
    openrouter = openrouter_module

    # Убираем API ключ
    monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)

    # Вызываем chat_once() и проверяем результат
    messages = [{"role": "user", "content": "Тестовый вопрос"}]

    with pytest.raises(openrouter.OpenRouterError) as exc_info:
        openrouter.chat_once(messages, model="test-model")

    # Проверяем соответствие контракту
    error_str = str(exc_info.value)
    # Исправляем проверку для нового формата ошибки
    assert "[401]" in error_str
    assert "Отсутствует OPENROUTER_API_KEY" in error_str