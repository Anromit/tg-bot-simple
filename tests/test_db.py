import pytest


def test_character_upsert(db_module):
    """Тест UPSERT для персонажей - проверка, что у пользователя может быть только один персонаж"""
    db = db_module

    # Получаем список всех персонажей
    characters = db.list_characters()
    assert len(characters) > 0, "В базе должны быть персонажи"

    # Выбираем первого персонажа
    first_character = characters[0]
    first_id = first_character['id']

    # Тестовый ID пользователя
    user_id = 123

    # Устанавливаем первого персонажа для пользователя
    db.set_user_character(user_id, first_id)

    # Проверяем, что get_user_character возвращает именно этого персонажа
    result = db.get_user_character(user_id)
    assert result['id'] == first_id

    # Выбираем другого персонажа (не того же самого)
    second_character = None
    for char in characters:
        if char['id'] != first_id:
            second_character = char
            break

    assert second_character is not None, "Должен быть хотя бы один другой персонаж"
    second_id = second_character['id']

    # Устанавливаем другого персонажа для того же пользователя
    db.set_user_character(user_id, second_id)

    # Проверяем, что теперь у пользователя другой персонаж
    result = db.get_user_character(user_id)
    assert result['id'] == second_id

    # Проверяем, что запись обновилась, а не создалась новая
    with db._connect() as conn:
        count = conn.execute(
            'SELECT COUNT(*) FROM user_character WHERE telegram_user_id = ?',
            (user_id,)
        ).fetchone()[0]
        assert count == 1, "Должна быть ровно одна запись для пользователя"


def test_active_model_constraint(db_module):
    """Тест условия 'ровно одна активная модель'"""
    db = db_module

    # Получаем список всех моделей
    models = db.list_models()
    assert len(models) >= 2, "В базе должно быть хотя бы 2 модели"

    # Берем две разные модели
    model_a = models[0]
    model_b = models[1]
    id_a = model_a['id']
    id_b = model_b['id']

    # Устанавливаем первую модель как активную
    db.set_active_model(id_a)
    active_model = db.get_active_model()
    assert active_model['id'] == id_a

    # Устанавливаем вторую модель как активную
    db.set_active_model(id_b)
    active_model = db.get_active_model()
    assert active_model['id'] == id_b

    # Проверяем, что в базе ровно одна активная модель
    with db._connect() as conn:
        count = conn.execute(
            'SELECT COUNT(*) FROM models WHERE active = 1'
        ).fetchone()[0]
        assert count == 1, "Должна быть ровно одна активная модель"


def test_set_active_model_rejects_unknown_id(db_module):
    """Тест, что set_active_model отвергает неизвестный ID модели"""
    db = db_module

    # Берём гарантированно несуществующий ID
    unknown_id = 999999

    # Проверяем, что функция выбрасывает исключение
    with pytest.raises(ValueError) as excinfo:
        db.set_active_model(unknown_id)

    # Проверяем сообщение об ошибке из db.py:
    assert "Неизвестный ID модели" in str(excinfo.value)


def test_set_user_character_rejects_unknown_character(db_module):
    """Тест, что set_user_character отвергает неизвестный ID персонажа"""
    db = db_module

    # Берём несуществующий ID персонажа
    unknown_character_id = 999999
    user_id = 123

    # Проверяем, что функция выбрасывает исключение
    with pytest.raises(ValueError) as excinfo:
        db.set_user_character(user_id, unknown_character_id)

    # Проверяем сообщение об ошибке
    assert "Неизвестный ID персонажа" in str(excinfo.value)


def test_get_user_character_nonexistent(db_module):
    """Тест получения персонажа для несуществующего пользователя"""
    db = db_module

    result = db.get_user_character(999999)

    # Функция возвращает дефолтного персонажа, а не None
    assert result is not None, "Для несуществующего пользователя должен возвращаться дефолтный персонаж"
    assert 'id' in result
    assert 'name' in result
    # В вашей БД у персонажей есть только id и name


def test_list_characters_structure(db_module):
    """Тест структуры данных персонажей"""
    db = db_module

    characters = db.list_characters()
    assert isinstance(characters, list)

    # Проверяем структуру данных персонажа
    if len(characters) > 0:
        character = characters[0]
        assert 'id' in character
        assert 'name' in character
        # В вашей БД у персонажей только id и name, нет prompt или description


def test_list_models_structure(db_module):
    """Тест структуры данных моделей"""
    db = db_module

    models = db.list_models()
    assert isinstance(models, list)

    # Проверяем структуру данных модели
    if len(models) > 0:
        model = models[0]
        assert 'id' in model
        assert 'key' in model
        assert 'label' in model
        assert 'active' in model


def test_get_user_character_fails_back_to_default(db_module):
    """Тест, что get_user_character возвращает дефолтного персонажа при отсутствии записи"""
    db = db_module

    # Берём пользователя, для которого мы точно ничего не записывали
    uid = 100001

    # Вызов без предварительного set_user_character
    ch = db.get_user_character(uid)

    # Ожидаем: нам вернётся существующий персонаж из таблицы characters
    all_chars = db.list_characters()
    assert all_chars, "Список персонажей пуст – проверь schema в db.py"

    # Получаем все существующие ID персонажей
    ids = {c['id'] for c in all_chars}

    # Проверяем, что возвращенный персонаж существует в базе
    assert ch is not None, "get_user_character должен возвращать персонажа"
    assert ch['id'] in ids, 'get_user_character должен возвращать одного из существующих персонажей'

    # Проверяем структуру данных (только id и name)
    assert 'id' in ch
    assert 'name' in ch


def test_get_user_character_returns_consistent_character(db_module):
    """Тест, что get_user_character всегда возвращает одного и того же дефолтного персонажа"""
    db = db_module

    # Берём двух разных пользователей без установленных персонажей
    uid1 = 100002
    uid2 = 100003

    # Получаем персонажей для обоих пользователей
    ch1 = db.get_user_character(uid1)
    ch2 = db.get_user_character(uid2)

    # Ожидаем, что оба получат одного и того же дефолтного персонажа
    assert ch1 is not None, "Первый пользователь должен получить персонажа"
    assert ch2 is not None, "Второй пользователь должен получить персонажа"
    assert ch1['id'] == ch2['id'], "Оба пользователя должны получать одного и того же дефолтного персонажа"


def test_database_initial_state(db_module):
    """Тест начального состояния базы данных"""
    db = db_module

    # Проверяем, что есть хотя бы одна активная модель
    active_model = db.get_active_model()
    assert active_model is not None, "Должна быть хотя бы одна активная модель при инициализации"
    assert active_model['active'] == 1, "Активная модель должна иметь active=1"

    # Проверяем, что есть персонажи
    characters = db.list_characters()
    assert len(characters) > 0, "Должны быть персонажи при инициализации"

    # Проверяем, что есть модели
    models = db.list_models()
    assert len(models) > 0, "Должны быть модели при инициализации"


def test_character_basic_content(db_module):
    """Тест базового содержания персонажей"""
    db = db_module

    characters = db.list_characters()

    for character in characters:
        assert 'id' in character
        assert 'name' in character
        # Проверяем, что имя не пустое
        assert len(character['name']) > 0, f"Имя персонажа не должно быть пустым"
        # Проверяем, что ID является числом
        assert isinstance(character['id'], int), "ID персонажа должен быть числом"


def test_models_have_required_fields(db_module):
    """Тест наличия обязательных полей у моделей"""
    db = db_module

    models = db.list_models()

    for model in models:
        assert 'id' in model
        assert 'key' in model
        assert 'label' in model
        assert 'active' in model
        # Проверяем, что ключ и метка не пустые
        assert len(model['key']) > 0, "Ключ модели не должен быть пустым"
        assert len(model['label']) > 0, "Метка модели не должна быть пустой"
        # Проверяем, что active является булевым значением
        assert isinstance(model['active'], (bool, int)), "Active должен быть булевым значением или числом"


def test_character_uniqueness(db_module):
    """Тест уникальности персонажей"""
    db = db_module

    characters = db.list_characters()

    # Проверяем, что все ID уникальны
    ids = [char['id'] for char in characters]
    assert len(ids) == len(set(ids)), "Все ID персонажей должны быть уникальными"

    # Проверяем, что все имена уникальны
    names = [char['name'] for char in characters]
    assert len(names) == len(set(names)), "Все имена персонажей должны быть уникальными"


def test_model_uniqueness(db_module):
    """Тест уникальности моделей"""
    db = db_module

    models = db.list_models()

    # Проверяем, что все ID уникальны
    ids = [model['id'] for model in models]
    assert len(ids) == len(set(ids)), "Все ID моделей должны быть уникальными"

    # Проверяем, что все ключи уникальны
    keys = [model['key'] for model in models]
    assert len(keys) == len(set(keys)), "Все ключи моделей должны быть уникальными"