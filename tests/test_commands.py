import pytest
from unittest.mock import Mock, patch


class TestNoteEdit:
    """Тесты для команды /note_edit"""

    def setup_method(self):
        """Настройка перед каждым тестом"""
        self.user_id = 12345
        self.chat_id = 67890

        # Создаем mock-объект сообщения
        self.message = Mock()
        self.message.from_user.id = self.user_id
        self.message.chat.id = self.chat_id

    @patch('main.update_note')
    @patch('main.list_notes')
    @patch('main.bot.reply_to')
    def test_note_edit_success(self, mock_reply, mock_list_notes, mock_update_note, main_module):
        """Тест успешного редактирования заметки"""
        main = main_module

        # Настраиваем моки
        mock_update_note.return_value = True
        mock_list_notes.return_value = [{'id': 1, 'text': 'Старый текст'}]

        # Устанавливаем текст сообщения
        self.message.text = "/note_edit 1 Новый текст заметки"

        # Вызываем тестируемую функцию
        main.note_edit(self.message)

        # Проверяем вызовы
        mock_update_note.assert_called_once_with(self.user_id, 1, "Новый текст заметки")
        mock_reply.assert_called_once_with(
            self.message,
            "✏️ Заметка #1 изменена на: Новый текст заметки\n"
            "📊 Статистика: 1/50 заметок"
        )

    @patch('main.bot.reply_to')
    def test_note_edit_insufficient_arguments(self, mock_reply, main_module):
        """Тест редактирования с недостаточным количеством аргументов"""
        main = main_module

        # Устанавливаем текст сообщения с недостаточными аргументами
        self.message.text = "/note_edit 1"

        # Вызываем тестируемую функцию
        main.note_edit(self.message)

        # Проверяем вызовы
        mock_reply.assert_called_once_with(
            self.message,
            "Ошибка: Используйте /note_edit <id> <новый текст>"
        )

    @patch('main.bot.reply_to')
    def test_note_edit_invalid_id(self, mock_reply, main_module):
        """Тест редактирования с нечисловым ID"""
        main = main_module

        # Устанавливаем текст сообщения с нечисловым ID
        self.message.text = "/note_edit abc Новый текст"

        # Вызываем тестируемую функцию
        main.note_edit(self.message)

        # Проверяем вызовы
        mock_reply.assert_called_once_with(
            self.message,
            "Ошибка: ID должен быть числом."
        )

    @patch('main.update_note')
    @patch('main.bot.reply_to')
    def test_note_edit_note_not_found(self, mock_reply, mock_update_note, main_module):
        """Тест редактирования несуществующей заметки"""
        main = main_module

        # Настраиваем моки
        mock_update_note.return_value = False

        # Устанавливаем текст сообщения
        self.message.text = "/note_edit 999 Новый текст"

        # Вызываем тестируемую функцию
        main.note_edit(self.message)

        # Проверяем вызовы
        mock_update_note.assert_called_once_with(self.user_id, 999, "Новый текст")
        mock_reply.assert_called_once_with(
            self.message,
            "Ошибка: Заметка #999 не найдена или у вас нет прав для её изменения."
        )


class TestNoteDel:
    """Тесты для команды /note_del"""

    def setup_method(self):
        """Настройка перед каждым тестом"""
        self.user_id = 12345
        self.chat_id = 67890

        # Создаем mock-объект сообщения
        self.message = Mock()
        self.message.from_user.id = self.user_id
        self.message.chat.id = self.chat_id

    @patch('main.delete_note')
    @patch('main.list_notes')
    @patch('main.bot.reply_to')
    def test_note_del_success(self, mock_reply, mock_list_notes, mock_delete_note, main_module):
        """Тест успешного удаления заметки"""
        main = main_module

        # Настраиваем моки
        mock_delete_note.return_value = True
        mock_list_notes.return_value = [{'id': 2, 'text': 'Текст заметки'}]

        # Устанавливаем текст сообщения
        self.message.text = "/note_del 1"

        # Вызываем тестируемую функцию
        main.note_del(self.message)

        # Проверяем вызовы
        mock_delete_note.assert_called_once_with(self.user_id, 1)
        mock_reply.assert_called_once_with(
            self.message,
            "🗑️ Заметка #1 удалена.\n"
            "📊 Статистика: 1/50 заметок"
        )

    @patch('main.bot.reply_to')
    def test_note_del_no_id(self, mock_reply, main_module):
        """Тест удаления без указания ID"""
        main = main_module

        # Устанавливаем текст сообщения без ID
        self.message.text = "/note_del"

        # Вызываем тестируемую функцию
        main.note_del(self.message)

        # Проверяем вызовы
        mock_reply.assert_called_once_with(
            self.message,
            "Ошибка: Укажите ID заметки для удаления."
        )

    @patch('main.bot.reply_to')
    def test_note_del_invalid_id(self, mock_reply, main_module):
        """Тест удаления с нечисловым ID"""
        main = main_module

        # Устанавливаем текст сообщения с нечисловым ID
        self.message.text = "/note_del abc"

        # Вызываем тестируемую функцию
        main.note_del(self.message)

        # Проверяем вызовы
        mock_reply.assert_called_once_with(
            self.message,
            "Ошибка: ID должен быть числом."
        )

    @patch('main.delete_note')
    @patch('main.bot.reply_to')
    def test_note_del_note_not_found(self, mock_reply, mock_delete_note, main_module):
        """Тест удаления несуществующей заметки"""
        main = main_module

        # Настраиваем моки
        mock_delete_note.return_value = False

        # Устанавливаем текст сообщения
        self.message.text = "/note_del 999"

        # Вызываем тестируемую функцию
        main.note_del(self.message)

        # Проверяем вызовы
        mock_delete_note.assert_called_once_with(self.user_id, 999)
        mock_reply.assert_called_once_with(
            self.message,
            "Ошибка: Заметка #999 не найдена или у вас нет прав для её удаления."
        )


class TestNoteCount:
    """Тесты для команды /note_count"""

    def setup_method(self):
        """Настройка перед каждым тестом"""
        self.user_id = 12345
        self.chat_id = 67890

        # Создаем mock-объект сообщения
        self.message = Mock()
        self.message.from_user.id = self.user_id
        self.message.chat.id = self.chat_id

    @patch('main.list_notes')
    @patch('main.bot.reply_to')
    def test_note_count_empty(self, mock_reply, mock_list_notes, main_module):
        """Тест подсчета пустого списка заметок"""
        main = main_module

        # Настраиваем моки
        mock_list_notes.return_value = []

        # Устанавливаем текст сообщения
        self.message.text = "/note_count"

        # Вызываем тестируемую функцию
        main.note_count(self.message)

        # Проверяем вызовы
        mock_list_notes.assert_called_once_with(self.user_id)
        mock_reply.assert_called_once_with(
            self.message,
            "📊 Статистика заметок:\n"
            "• Всего заметок: 0\n"
            "• Лимит: 50\n"
            "• Свободно: 50\n"
            "✅ Есть свободное место"
        )

    @patch('main.list_notes')
    @patch('main.bot.reply_to')
    def test_note_count_half_full(self, mock_reply, mock_list_notes, main_module):
        """Тест подсчета при заполнении половины лимита"""
        main = main_module

        # Настраиваем моки (25 заметок)
        mock_list_notes.return_value = [Mock() for _ in range(25)]

        # Устанавливаем текст сообщения
        self.message.text = "/note_count"

        # Вызываем тестируемую функцию
        main.note_count(self.message)

        # Проверяем вызовы
        mock_reply.assert_called_once_with(
            self.message,
            "📊 Статистика заметок:\n"
            "• Всего заметок: 25\n"
            "• Лимит: 50\n"
            "• Свободно: 25\n"
            "✅ Есть свободное место"
        )

    @patch('main.list_notes')
    @patch('main.bot.reply_to')
    def test_note_count_near_limit(self, mock_reply, mock_list_notes, main_module):
        """Тест подсчета при приближении к лимиту (80%)"""
        main = main_module

        # Настраиваем моки (40 заметок - 80% от лимита)
        mock_list_notes.return_value = [Mock() for _ in range(40)]

        # Устанавливаем текст сообщения
        self.message.text = "/note_count"

        # Вызываем тестируемую функцию
        main.note_count(self.message)

        # Проверяем вызовы
        mock_reply.assert_called_once_with(
            self.message,
            "📊 Статистика заметок:\n"
            "• Всего заметок: 40\n"
            "• Лимит: 50\n"
            "• Свободно: 10\n"
            "⚠️ Лимит почти достигнут!"
        )

    @patch('main.list_notes')
    @patch('main.bot.reply_to')
    def test_note_count_limit_reached(self, mock_reply, mock_list_notes, main_module):
        """Тест подсчета при достижении лимита"""
        main = main_module

        # Настраиваем моки (50 заметок - лимит)
        mock_list_notes.return_value = [Mock() for _ in range(50)]

        # Устанавливаем текст сообщения
        self.message.text = "/note_count"

        # Вызываем тестируемую функцию
        main.note_count(self.message)

        # Проверяем вызовы
        mock_reply.assert_called_once_with(
            self.message,
            "📊 Статистика заметок:\n"
            "• Всего заметок: 50\n"
            "• Лимит: 50\n"
            "• Свободно: 0\n"
            "❌ Лимит достигнут!"
        )


class TestModels:
    """Тесты для команды /models"""

    def setup_method(self):
        """Настройка перед каждым тестом"""
        self.user_id = 12345
        self.chat_id = 67890

        # Создаем mock-объект сообщения
        self.message = Mock()
        self.message.from_user.id = self.user_id
        self.message.chat.id = self.chat_id

    @patch('main.list_models')
    @patch('main.bot.reply_to')
    def test_models_list_empty(self, mock_reply, mock_list_models, main_module):
        """Тест отображения пустого списка моделей"""
        main = main_module

        # Настраиваем моки
        mock_list_models.return_value = []

        # Устанавливаем текст сообщения
        self.message.text = "/models"

        # Вызываем тестируемую функцию
        main.cmd_models(self.message)

        # Проверяем вызовы
        mock_list_models.assert_called_once()
        mock_reply.assert_called_once_with(
            self.message,
            "Список моделей пуст"
        )

    @patch('main.list_models')
    @patch('main.bot.reply_to')
    def test_models_list_with_models(self, mock_reply, mock_list_models, main_module):
        """Тест отображения списка моделей"""
        main = main_module

        # Настраиваем моки
        mock_list_models.return_value = [
            {'id': 1, 'label': 'GPT-3.5', 'key': 'gpt-3.5-turbo', 'active': True},
            {'id': 2, 'label': 'GPT-4', 'key': 'gpt-4', 'active': False},
            {'id': 3, 'label': 'Claude', 'key': 'claude-2', 'active': False}
        ]

        # Устанавливаем текст сообщения
        self.message.text = "/models"

        # Вызываем тестируемую функцию
        main.cmd_models(self.message)

        # Проверяем вызовы
        mock_list_models.assert_called_once()

        # Получаем переданный текст ответа
        called_args = mock_reply.call_args
        response_text = called_args[0][1]

        # Проверяем содержание ответа
        assert "Доступные модели:" in response_text
        assert "* 1. GPT-3.5 [gpt-3.5-turbo]" in response_text
        assert " 2. GPT-4 [gpt-4]" in response_text
        assert " 3. Claude [claude-2]" in response_text
        assert "Активировать: /model <ID>" in response_text

    @patch('main.list_models')
    @patch('main.bot.reply_to')
    def test_models_command_formatting(self, mock_reply, mock_list_models, main_module):
        """Тест форматирования команды /models"""
        main = main_module

        # Настраиваем моки
        mock_list_models.return_value = [
            {'id': 1, 'label': 'Test Model', 'key': 'test-model', 'active': True}
        ]

        # Устанавливаем текст сообщения
        self.message.text = "/models"

        # Вызываем тестируемую функцию
        main.cmd_models(self.message)

        # Получаем переданный текст ответа
        called_args = mock_reply.call_args
        response_text = called_args[0][1]

        # Проверяем форматирование
        lines = response_text.split('\n')
        assert len(lines) >= 3  # Заголовок + модель + инструкция
        assert any('*' in line for line in lines)  # Должна быть активная модель с *