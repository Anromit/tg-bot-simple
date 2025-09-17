import os
from dotenv import load_dotenv
import telebot
load_dotenv()
TOKEN = os.getenv("TOKEN")
if not TOKEN:
 raise RuntimeError("В .env нет TOKEN")
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
 bot.reply_to(message, "Привет! Я твой первый бот! Напиши /help")
 
 
@bot.message_handler(commands=['help'])
def help_cmd(message):
 bot.reply_to(message, "/start - начать\n/help - помощь\n/about - что я умею\n/ping - могу отбить мяч")
 
 
@bot.message_handler(commands=['about'])
def about(message):
 bot.reply_to(message, "Умный и простой в использовании бот, созданный для помощи в повседневных задачах. Автор бота — Анастасия.")


@bot.message_handler(commands=['ping'])
def ping(message):
    bot.reply_to(message, "понг...")
    
 
if __name__ == "__main__":
 bot.infinity_polling(skip_pending=True)

