import pytest


def test_build_message_include_character_and_rules(db_module, main_module, monkeypatch):
    db = db_module
    main = main_module

    # код пользователя и организация персонажа
    uid = 42001
    characters = db.list_characters()
    target = characters[0]
    db.set_user_character(uid, target['id'])

    msgs = main.build_messages(uid, "Что такое API?")
    assert msgs[0]['role'] == "system"
    sys = msgs[0]['content']

    # проверяем, что system содержит имя персонажа и слова «Формат» или «Правила»
    assert target['name'] in sys
    assert "Формат" in sys or "Правила" in sys
    assert msgs[1]['role'] == "user"
    assert "Что такое API?" in msgs[1]['content']


def test_build_message_use_default_character_when_not_set(db_module, main_module):
    db = db_module
    main = main_module

    uid = 5000
    question = "Success vs. wdfyjm o cefe"

    # здесь мы не вызываем set_user_character
    msgs = main.build_messages(uid, question)

    assert msgs[0]['role'] == 'system'
    sys_txt = msgs[0]['content']

    # персонаж по умолчанию - один из characters в БД
    characters = db.list_characters()
    assert characters, 'Список персонажей пуст - проверь schema в db.py'
    names = {c['name'] for c in characters}

    # в system-тексте должно быть имя какого-то персонажа
    assert any(name in sys_txt for name in names), "system должен содержать имя хоть какого-то персонажа"

    assert msgs[1]['role'] == 'user'
    assert question in msgs[1]['content']


def test_build_messages_for_character_pure_function(main_module):
    main = main_module

    character = {
        'id': 123,
        'name': 'Тестовый персонаж',
        'prompt': 'Отвечай коротко и по делу.',
    }

    question = "Что такое интеграционный тест?"

    msgs = main.build_messages_for_character(character, question)

    assert isinstance(msgs, list)
    assert msgs[0]['role'] == 'system'
    assert 'Тестовый персонаж' in msgs[0]['content']
    assert 'Отвечай коротко и по делу.' in msgs[0]['content']
    assert msgs[1]['role'] == 'user'
    assert question in msgs[1]['content']