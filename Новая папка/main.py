import os
from dotenv import load_dotenv
import telebot
from telebot import types
from typing import List
import logging
import requests

# Настройка прокси (раскомментируйте если нужно)
# from telebot import apihelper
# apihelper.proxy = {'https': 'socks5://user:pass@host:port'}

load_dotenv()
TOKEN = os.getenv("TOKEN")

if not TOKEN:
    raise RuntimeError("В .env нет TOKEN")

bot = telebot.TeleBot(TOKEN)
def parse_ints_from_text(text: str) -> List[int]:
    """Выделяет из текста целые числа: нормализует запятые, игнорирует токены-команды."""
    text = text.replace(",", " ")
    tokens = [tok for tok in text.split() if not tok.startswith("/")]
    return [int(tok) for tok in tokens if is_int_token(tok)]

def is_int_token(t: str) -> bool:
    """Проверка токена на целое число (с поддержкой знака минус)."""
    if not t:
        return False
    t = t.strip()
    if t in {"-", ""}:
        return False
    return t.lstrip("-").isdigit()




def fetch_weather_moscow_open_meteo() -> str:
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": 55.7558,
        "longitude": 37.6173,
        "current": "temperature_2m",
        "timezone": "Europe/Moscow"
    }
    try:
        r = requests.get(url, params=params, timeout=5)
        r.raise_for_status()
        t = r.json()["current"]["temperature_2m"]
        return f"Москва: сейчас {round(t)}°C"
    except Exception:
        return "Не удалось получить погоду."
        
        
@bot.message_handler(func=lambda m: m.text == "Weather")
def  Weather(message):
    
 bot.reply_to(message, fetch_weather_moscow_open_meteo())
        
        






@bot.message_handler(commands=["start", "help"])
def start_help(m: types.Message) -> None:
    bot.send_message(
        m.chat.id,
        "Привет! Доступно: /about, /confirm, /ping, /hide, /show \n"
        "Или воспользуйтесь кнопками ниже.",
        reply_markup=make_main_kb()
    )


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
    
    
    
@bot.message_handler(func=lambda m: m.text == "hide")
def hide_kb(m):
    rm = types.ReplyKeyboardRemove()
    
    bot.send_message(m.chat.id,"Спрятал клаву, хочешь покажу? /show", reply_markup=rm)  
    
@bot.message_handler(commands=['hide'])
def hide_kb(m):
    rm = types.ReplyKeyboardRemove()
    
    bot.send_message(m.chat.id,"Спрятал клаву", reply_markup=rm)  
    
#дз2
@bot.message_handler(commands=['show'])
def show_keyboard(message):
    main_kb = make_main_kb()
    bot.send_message(message.chat.id, "Показал клавиатуру:", reply_markup=main_kb)   
    
    
    
@bot.message_handler(commands=["confirm"])
def confirm_cmd(m: types.Message) -> None:
    kb = types.InlineKeyboardMarkup()
    kb.add(
        types.InlineKeyboardButton("Майонез", callback_data="confirm:M"),
        types.InlineKeyboardButton("Кетчуп", callback_data="confirm:K"),
        types.InlineKeyboardButton("Горчица", callback_data="confirm:G")
    )
    bot.send_message(m.chat.id, "Какой соус к пельменям ты любишь?", reply_markup=kb)



@bot.callback_query_handler(func=lambda c: c.data and c.data.startswith("confirm:"))
def on_confirm(c: types.CallbackQuery) -> None:
    choice = c.data.split(":", 1)[1]
    bot.answer_callback_query(c.id, "Все любят кушать!")
    # Уберём inline-кнопки у исходного сообщения
    bot.edit_message_reply_markup(c.message.chat.id, c.message.message_id, reply_markup=None)
    bot.send_message(c.message.chat.id, "Главное не сметана!" if choice == "M" else "Окей, ты странный!")


@bot.message_handler(func=lambda m: m.text == "Сумма")
def kb_sum(m: types.Message) -> None:
    bot.send_message(m.chat.id, "Введите числа через пробел или запятую:")
    bot.register_next_step_handler(m, on_sum_numbers)
    logging.info(f"/sum от {m.from_user.first_name}{m.from_user.id}:{m.text}")
def on_sum_numbers(m: types.Message) -> None:
    nums = parse_ints_from_text(m.text)
    #logging.info("KB-sum next step from id=%s text=%r -> %r", m.from_user.id if m.from_user else "?", m.text, nums)
    if not nums:
        bot.reply_to(m, "Не вижу чисел. Пример: 2 3 10")
    else:
        bot.reply_to(m, f"Сумма: {sum(nums)}")
        
       
   
       
       
       
       
       
       
       
     
       
       
       
#дз 2       
@bot.message_handler(func=lambda m: m.text == "Max")
def kb_max(m: types.Message) -> None:
    bot.send_message(m.chat.id, "Введите числа через пробел или запятую:")
    bot.register_next_step_handler(m, on_max_numbers)
    
def on_max_numbers(m: types.Message) -> None:
    nums = parse_ints_from_text(m.text)
    
    if not nums:
        bot.reply_to(m, "Не вижу чисел. Пример: 2 3 10")
    else:
        bot.reply_to(m, f"Максимум: {max(nums)}")
        



logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s-%(levelname)s-%(message)s"
)





def make_main_kb()->types.ReplyKeyboardMarkup:
    kb=types.ReplyKeyboardMarkup(resize_keyboard = True)
    kb.row("/about","Сумма","Max")
    kb.row("/help","Weather","hide")
    return kb
    
        
   
    
    
    
    
 
if __name__ == "__main__":
    import time
    while True:
        try:
            bot.infinity_polling(timeout=10, long_polling_timeout=5)
        except Exception as e:
            print("Ошибка polling")
            time.sleep(5)

