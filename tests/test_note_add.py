import pytest
from unittest.mock import Mock, patch
import sys
import os

# Добавляем путь к проекту для импорта модулей
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestNoteAdd:
    """Тесты для команды /note_add"""

    def setup_method(self):
        """Настройка перед каждым тестом"""
        self.user_id = 12345
        self.chat_id = 67890

        # Создаем mock-объект сообщения
        self.message = Mock()
        self.message.from_user.id = self.user_id
        self.message.chat.id = self.chat_id

    @patch('main.list_notes')
    @patch('main.add_note')
    @patch('main.bot.reply_to')
    def test_note_add_success(self, mock_reply, mock_add_note, mock_list_notes, main_module):
        """Тест успешного добавления заметки"""
        main = main_module

        # Настраиваем моки
        mock_list_notes.return_value = []  # Пустой список заметок
        mock_add_note.return_value = 1  # ID новой заметки

        # Устанавливаем текст сообщения
        self.message.text = "/note_add Тестовая заметка"

        # Вызываем тестируемую функцию
        main.note_add(self.message)

        # Проверяем вызовы
        mock_list_notes.assert_called_once_with(self.user_id)
        mock_add_note.assert_called_once_with(self.user_id, "Тестовая заметка")
        mock_reply.assert_called_once_with(
            self.message,
            "✅ Заметка #1 добавлена: Тестовая заметка\n"
            "📊 Статистика: 1/50 заметок"
        )

    @patch('main.list_notes')
    @patch('main.add_note')
    @patch('main.bot.reply_to')
    def test_note_add_empty_text(self, mock_reply, mock_add_note, mock_list_notes, main_module):
        """Тест добавления заметки с пустым текстом"""
        main = main_module

        # Настраиваем моки
        mock_list_notes.return_value = []

        # Устанавливаем текст сообщения без содержимого
        self.message.text = "/note_add"

        # Вызываем тестируемую функцию
        main.note_add(self.message)

        # Проверяем вызовы
        mock_list_notes.assert_called_once_with(self.user_id)
        mock_add_note.assert_not_called()
        mock_reply.assert_called_once_with(
            self.message,
            "Ошибка: Укажите текст заметки."
        )

    @patch('main.list_notes')
    @patch('main.add_note')
    @patch('main.bot.reply_to')
    def test_note_add_with_extra_spaces(self, mock_reply, mock_add_note, mock_list_notes, main_module):
        """Тест добавления заметки с лишними пробелами"""
        main = main_module

        # Настраиваем моки
        mock_list_notes.return_value = []
        mock_add_note.return_value = 2

        # Устанавливаем текст с лишними пробелами
        self.message.text = "/note_add   Заметка с пробелами   "

        # Вызываем тестируемую функцию
        main.note_add(self.message)

        # Проверяем вызовы
        mock_add_note.assert_called_once_with(self.user_id, "Заметка с пробелами")
        mock_reply.assert_called_once_with(
            self.message,
            "✅ Заметка #2 добавлена: Заметка с пробелами\n"
            "📊 Статистика: 1/50 заметок"
        )

    @patch('main.list_notes')
    @patch('main.add_note')
    @patch('main.bot.reply_to')
    def test_note_add_limit_reached(self, mock_reply, mock_add_note, mock_list_notes, main_module):
        """Тест попытки добавления заметки при достижении лимита"""
        main = main_module

        # Создаем mock-заметки (максимальное количество)
        mock_notes = [Mock() for _ in range(50)]

        # Настраиваем моки
        mock_list_notes.return_value = mock_notes

        # Устанавливаем текст сообщения
        self.message.text = "/note_add Новая заметка"

        # Вызываем тестируемую функцию
        main.note_add(self.message)

        # Проверяем вызовы
        mock_list_notes.assert_called_once_with(self.user_id)
        mock_add_note.assert_not_called()
        mock_reply.assert_called_once_with(
            self.message,
            "❌ Достигнут лимит заметок! Максимум 50 заметок на пользователя.\n"
            "У вас уже 50 заметок. Удалите некоторые заметки чтобы добавить новые."
        )

    @patch('main.list_notes')
    @patch('main.add_note')
    @patch('main.bot.reply_to')
    def test_note_add_near_limit(self, mock_reply, mock_add_note, mock_list_notes, main_module):
        """Тест добавления заметки когда接近 лимита"""
        main = main_module

        # Создаем mock-заметки (на одну меньше лимита)
        mock_notes = [Mock() for _ in range(49)]

        # Настраиваем моки
        mock_list_notes.return_value = mock_notes
        mock_add_note.return_value = 50

        # Устанавливаем текст сообщения
        self.message.text = "/note_add Последняя заметка"

        # Вызываем тестируемую функцию
        main.note_add(self.message)

        # Проверяем вызовы
        mock_add_note.assert_called_once_with(self.user_id, "Последняя заметка")
        mock_reply.assert_called_once_with(
            self.message,
            "✅ Заметка #50 добавлена: Последняя заметка\n"
            "📊 Статистика: 50/50 заметок"
        )

    @patch('main.list_notes')
    @patch('main.add_note')
    @patch('main.bot.reply_to')
    def test_note_add_with_special_characters(self, mock_reply, mock_add_note, mock_list_notes, main_module):
        """Тест добавления заметки со специальными символами"""
        main = main_module

        # Настраиваем моки
        mock_list_notes.return_value = []
        mock_add_note.return_value = 3

        # Устанавливаем текст со специальными символами
        special_text = "Заметка с 🚀 эмодзи и #хештегом!"
        self.message.text = f"/note_add {special_text}"

        # Вызываем тестируемую функцию
        main.note_add(self.message)

        # Проверяем вызовы
        mock_add_note.assert_called_once_with(self.user_id, special_text)
        mock_reply.assert_called_once_with(
            self.message,
            f"✅ Заметка #3 добавлена: {special_text}\n"
            "📊 Статистика: 1/50 заметок"
        )

    @patch('main.list_notes')
    @patch('main.add_note')
    @patch('main.bot.reply_to')
    def test_note_add_multiple_words(self, mock_reply, mock_add_note, mock_list_notes, main_module):
        """Тест добавления заметки с несколькими словами"""
        main = main_module

        # Настраиваем моки
        mock_list_notes.return_value = []
        mock_add_note.return_value = 4

        # Устанавливаем текст с несколькими словами
        multi_word_text = "Это тестовая заметка с несколькими словами для проверки функциональности"
        self.message.text = f"/note_add {multi_word_text}"

        # Вызываем тестируемую функцию
        main.note_add(self.message)

        # Проверяем вызовы
        mock_add_note.assert_called_once_with(self.user_id, multi_word_text)
        mock_reply.assert_called_once_with(
            self.message,
            f"✅ Заметка #4 добавлена: {multi_word_text}\n"
            "📊 Статистика: 1/50 заметок"
        )