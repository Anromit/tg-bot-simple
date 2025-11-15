import pytest


def validate_formatted_answer(
        text: str,
        min_points: int = 3,
        max_points: int = 5,
        max_intro_words: int = 12
) -> bool:
    """
    Простая эвристика: есть короткое вступление (первая строка),
    есть 3-5 нумерованных пунктов, и есть короткий финальный вывод.
    """
    POINT_PREFIXES = (
        "1", "2", "3", "4", "5", "6",
        "1.", "2.", "3.", "4.", "5.", "6.", "7.",
        "1)", "2)", "3)", "4)", "5)", "6)", "7)", "8)",
        "1", "2", "3", "4", "5", "6", "7", "8"
    )

    # 1) Разбить текст на непустые строки
    lines = [l.strip() for l in text.strip().splitlines() if l.strip()]
    if len(lines) < 3:
        return False

    # 2) Вступление: первая строка, не слишком длинная
    intro_words = len(lines[0].split())
    if intro_words == 0 or intro_words > max_intro_words:
        return False

    # 3) Пункты: строки между первой и последней, начинающиеся с префиксов
    points = [ln for ln in lines[1:-1] if ln.startswith(POINT_PREFIXES)]
    if not (min_points <= len(points) <= max_points):
        return False

    # 4) Вывод: последняя строка, не слишком длинная (<= 20 слов)
    return len(lines[-1].split()) <= 20


def test_valid_format():
    """Один валидный пример"""
    text = """
    Хороший вопрос! Вот основные моменты:

    1. Первый важный пункт с объяснением
    2. Второй существенный момент  
    3. Третий ключевой аспект
    4. Четвертое наблюдение

    Вот такие выводы можно сделать.
    """
    assert validate_formatted_answer(text) is True


def test_no_points():
    """Нет пунктов"""
    text = """
    Рассмотрим этот вопрос.

    Просто текст без нумерации.

    Короткий вывод.
    """
    assert validate_formatted_answer(text) is False


def test_long_introduction():
    """Длинное вступление"""
    text = """
    Это очень очень очень очень очень очень длинное вступление которое точно превышает лимит в двенадцать слов
    1. Первый пункт
    2. Второй пункт
    3. Третий пункт
    Короткий вывод.
    """
    assert validate_formatted_answer(text) is False


def test_few_points():
    """Мало пунктов"""
    text = """
    Вступление.
    1. Только один пункт
    Вывод.
    """
    assert validate_formatted_answer(text) is False


def test_many_points():
    """Слишком много пунктов"""
    text = """
    Вступление.
    1. Пункт 1
    2. Пункт 2  
    3. Пункт 3
    4. Пункт 4
    5. Пункт 5
    6. Пункт 6
    7. Пункт 7
    Вывод.
    """
    assert validate_formatted_answer(text) is False


def test_long_conclusion():
    """Длинный вывод"""
    text = """
    Вступление.
    1. Пункт 1
    2. Пункт 2
    3. Пункт 3
    Это очень очень очень очень очень очень очень очень очень очень очень очень очень очень очень очень очень очень очень очень длинный вывод который точно превышает лимит в двадцать слов и поэтому должен быть отвергнут валидатором.
    """
    assert validate_formatted_answer(text) is False