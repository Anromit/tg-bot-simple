import pytest
from unittest.mock import Mock, patch


class TestHelpCmd:
    """Тесты для команды /help"""

    def setup_method(self):
        """Настройка перед каждым тестом"""
        self.user_id = 12345
        self.chat_id = 67890

        # Создаем mock-объект сообщения
        self.message = Mock()
        self.message.from_user.id = self.user_id
        self.message.chat.id = self.chat_id

    @patch('main.bot.reply_to')
    def test_help_cmd_contains_all_commands(self, mock_reply, main_module):
        """Тест, что help содержит все основные команды"""
        main = main_module

        # Устанавливаем текст сообщения
        self.message.text = "/help"

        # Вызываем тестируемую функцию
        main.help_cmd(self.message)

        # Проверяем, что функция reply_to была вызвана
        mock_reply.assert_called_once()

        # Получаем переданный текст ответа
        called_args = mock_reply.call_args
        help_text = called_args[0][1]  # Второй аргумент - текст ответа

        # Проверяем наличие основных команд в help тексте
        assert "Доступные команды:" in help_text
        assert "/note_add" in help_text
        assert "/note_list" in help_text
        assert "/note_find" in help_text
        assert "/note_edit" in help_text
        assert "/note_del" in help_text
        assert "/note_count" in help_text
        assert "/note_export" in help_text
        assert "/note_stats" in help_text
        assert "/models" in help_text
        assert "/model" in help_text
        assert "/ask" in help_text
        assert "/ask_model" in help_text
        assert "/characters" in help_text
        assert "/character" in help_text
        assert "/whoami" in help_text

    @patch('main.bot.reply_to')
    def test_help_cmd_contains_limit_info(self, mock_reply, main_module):
        """Тест, что help содержит информацию о лимите заметок"""
        main = main_module

        # Устанавливаем текст сообщения
        self.message.text = "/help"

        # Вызываем тестируемую функцию
        main.help_cmd(self.message)

        # Получаем переданный текст ответа
        called_args = mock_reply.call_args
        help_text = called_args[0][1]

        # Проверяем наличие информации о лимите
        assert "Лимит: 50 заметок на пользователя" in help_text
        assert "максимум 50" in help_text

    @patch('main.bot.reply_to')
    def test_help_cmd_contains_emoji_and_formatting(self, mock_reply, main_module):
        """Тест, что help содержит эмодзи и корректное форматирование"""
        main = main_module

        # Устанавливаем текст сообщения
        self.message.text = "/help"

        # Вызываем тестируемую функцию
        main.help_cmd(self.message)

        # Получаем переданный текст ответа
        called_args = mock_reply.call_args
        help_text = called_args[0][1]

        # Проверяем наличие эмодзи
        assert "📝" in help_text

        # Проверяем структуру (должны быть переносы строк)
        assert "\n" in help_text

    @patch('main.bot.reply_to')
    def test_help_cmd_called_with_correct_message(self, mock_reply, main_module):
        """Тест, что функция вызывается с правильным сообщением"""
        main = main_module

        # Устанавливаем текст сообщения
        self.message.text = "/help"

        # Вызываем тестируемую функцию
        main.help_cmd(self.message)

        # Проверяем, что reply_to вызван с правильным сообщением
        mock_reply.assert_called_once_with(self.message, Mock())

    @patch('main.bot.reply_to')
    def test_help_cmd_structure(self, mock_reply, main_module):
        """Тест структуры help сообщения"""
        main = main_module

        # Устанавливаем текст сообщения
        self.message.text = "/help"

        # Вызываем тестируемую функцию
        main.help_cmd(self.message)

        # Получаем переданный текст ответа
        called_args = mock_reply.call_args
        help_text = called_args[0][1]

        # Проверяем базовую структуру
        lines = help_text.split('\n')
        assert len(lines) > 5  # Должно быть несколько строк

        # Проверяем, что команды идут с описанием
        command_lines = [line for line in lines if line.strip().startswith('/')]
        assert len(command_lines) > 10  # Должно быть много команд

    @patch('main.bot.reply_to')
    def test_help_cmd_with_different_message_content(self, mock_reply, main_module):
        """Тест, что функция работает независимо от содержания сообщения"""
        main = main_module

        # Пробуем разные варианты текста сообщения
        test_messages = [
            "/help",
            "/help ",
            "/help   ",
            "/help some extra text"
        ]

        for msg_text in test_messages:
            self.message.text = msg_text
            mock_reply.reset_mock()

            # Вызываем тестируемую функцию
            main.help_cmd(self.message)

            # Проверяем, что ответ был отправлен
            mock_reply.assert_called_once()

            # Проверяем, что ответ содержит основные команды
            called_args = mock_reply.call_args
            help_text = called_args[0][1]
            assert "/note_add" in help_text