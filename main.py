import os
import logging
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# ====== СЕРВЕР ДЛЯ RENDER (Health Check) ======
class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is alive!")

def run_health_server():
    # Render передает порт в переменной окружения PORT
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', port), HealthCheckHandler)
    server.serve_forever()

# ====== НАСТРОЙКИ ======
[cite_start]TOKEN = os.environ.get("TOKEN") [cite: 1]
[cite_start]ADMIN_LINK = "https://t.me/gogact" [cite: 1]
[cite_start]REVIEWS_LINK = "https://t.me/gogact" [cite: 1]

[cite_start]LOGO_URL = "https://i.imgur.com/8wKYVxZ.jpeg" [cite: 1]
[cite_start]CITY_CHOICE_URL = "https://i.imgur.com/8wKYVxZ.jpeg" [cite: 1]

# ====== ТОВАРЫ ======
PRODUCTS = {
    [cite_start]"Печерський": [{"name": "🔥 ПРЕМІУМ ТОВАР 1", "price": 899}, {"name": "🔥 ПРЕМІУМ ТОВАР 2", "price": 999}], [cite: 2]
    [cite_start]"Шевченківський": [{"name": "🔥 ПРЕМІУМ ТОВАР 1", "price": 899}, {"name": "🔥 ПРЕМІУМ ТОВАР 2", "price": 999}, {"name": "🔥 ПРЕМІУМ ТОВАР 3", "price": 999}], [cite: 2]
    [cite_start]"Подільський": [{"name": "🔥 ПРЕМІУМ ТОВАР 1", "price": 899}], [cite: 2]
    [cite_start]"Оболонський": [{"name": "🔥 ПРЕМІУМ ТОВАР 1", "price": 899}], [cite: 2]
    [cite_start]"Київський": [{"name": "🔥 ТОВАР", "price": 850}], [cite: 2]
    [cite_start]"Салтівський": [{"name": "🔥 ТОВАР", "price": 800}], [cite: 2]
    [cite_start]"Приморський": [{"name": "🔥 ТОВАР", "price": 900}], [cite: 2]
    [cite_start]"Малиновський": [{"name": "🔥 ТОВАР", "price": 870}], [cite: 2]
    [cite_start]"Соборний": [{"name": "🔥 ТОВАР", "price": 880}], [cite: 2]
    [cite_start]"Центральний": [{"name": "🔥 ТОВАР", "price": 860}], [cite: 2]
    [cite_start]"Чечелівський": [{"name": "🔥 ТОВАР", "price": 890}], [cite: 2]
    [cite_start]"Галицький": [{"name": "🔥 ТОВАР", "price": 840}], [cite: 2]
    [cite_start]"Франківський": [{"name": "🔥 ТОВАР", "price": 830}], [cite: 3]
    [cite_start]"Олександрівський": [{"name": "🔥 ТОВАР", "price": 810}], [cite: 3]
    [cite_start]"Комунарський": [{"name": "🔥 ТОВАР", "price": 820}], [cite: 3]
    [cite_start]"Металургійний": [{"name": "🔥 ТОВАР", "price": 800}], [cite: 3]
    [cite_start]"Довгинцівський": [{"name": "🔥 ТОВАР", "price": 805}], [cite: 3]
    [cite_start]"Заводський": [{"name": "🔥 ТОВАР", "price": 815}], [cite: 3]
    [cite_start]"Замостянський": [{"name": "🔥 ТОВАР", "price": 820}], [cite: 3]
    [cite_start]"Ленінський": [{"name": "🔥 ТОВАР", "price": 830}], [cite: 3]
    [cite_start]"Зарічний": [{"name": "🔥 ТОВАР", "price": 810}], [cite: 3]
    [cite_start]"Богунський": [{"name": "🔥 ТОВАР", "price": 800}], [cite: 3]
    [cite_start]"Соснівський": [{"name": "🔥 ТОВАР", "price": 805}], [cite: 3]
}

# ====== ГОРОДА И РАЙОНЫ ======
[cite_start]ALL_CITIES = {} [cite: 4]

LARGE_CITIES = {
    [cite_start]"Київ": ["Печерський", "Шевченківський", "Подільський", "Оболонський"], [cite: 4]
    [cite_start]"Харків": ["Шевченківський", "Київський", "Салтівський"], [cite: 4]
    [cite_start]"Одеса": ["Приморський", "Київський", "Малиновський"], [cite: 4]
    [cite_start]"Дніпро": ["Соборний", "Центральний", "Чечелівський"], [cite: 4]
    [cite_start]"Львів": ["Галицький", "Франківський", "Шевченківський"], [cite: 4]
}

MEDIUM_CITIES = {
    [cite_start]"Запоріжжя": ["Олександрівський", "Комунарський"], [cite: 4]
    [cite_start]"Кривий Ріг": ["Металургійний", "Довгинцівський"], [cite: 4]
    [cite_start]"Миколаїв": ["Центральний", "Заводський"], [cite: 4]
    [cite_start]"Вінниця": ["Замостянський", "Ленінський"], [cite: 4]
    [cite_start]"Полтава": ["Шевченківський", "Київський"], [cite: 4]
}

SMALL_CITIES = {
    [cite_start]"Чернігів": ["Деснянський"], [cite: 5]
    [cite_start]"Черкаси": ["Соснівський"], [cite: 5]
    [cite_start]"Житомир": ["Богунський"], [cite: 5]
    [cite_start]"Суми": ["Зарічний"], [cite: 5]
    [cite_start]"Хмельницький": ["Центральний"], [cite: 5]
}

[cite_start]ALL_CITIES.update(LARGE_CITIES) [cite: 5]
[cite_start]ALL_CITIES.update(MEDIUM_CITIES) [cite: 5]
[cite_start]ALL_CITIES.update(SMALL_CITIES) [cite: 5]

[cite_start]logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO) [cite: 5]

async def send_main_menu(message, context: ContextTypes.DEFAULT_TYPE):
    keyboard = InlineKeyboardMarkup([
        [cite_start][InlineKeyboardButton("🛒 КУПИТИ ЗАРАЗ!", callback_data="buy")], [cite: 6]
        [
            [cite_start]InlineKeyboardButton("⭐ ВІДГУКИ КЛІЄНТІВ", url=REVIEWS_LINK), [cite: 6]
            [cite_start]InlineKeyboardButton("📞 ЗВ'ЯЗОК З НАМИ", url=ADMIN_LINK) [cite: 6]
        ]
    ])
    await message.reply_photo(
        photo=LOGO_URL,
        [cite_start]caption="🎉 *ЛАСКАВО ПРОСИМО ДО НАШОГО МАГАЗИНУ!*\n\n🔥 Найкращі товари\n⚡ Швидка доставка\n💯 Гарантія якості", [cite: 6]
        reply_markup=keyboard,
        parse_mode=ParseMode.MARKDOWN
    )

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    [cite_start]await send_main_menu(update.message, context) [cite: 7]

def get_city_keyboard():
    [cite_start]keyboard = [[InlineKeyboardButton(f"🏙️ {city}", callback_data=f"city_{city}")] for city in ALL_CITIES.keys()] [cite: 7]
    [cite_start]keyboard.append([InlineKeyboardButton("🏠 ГОЛОВНЕ МЕНЮ", callback_data="menu")]) [cite: 7]
    return InlineKeyboardMarkup(keyboard)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data
    [cite_start]await query.answer() [cite: 8]

    if data == "menu":
        [cite_start]await query.message.delete() [cite: 8]
        [cite_start]await send_main_menu(query.message, context) [cite: 8]
        return

    if data == "buy":
        [cite_start]await query.message.delete() [cite: 8]
        await query.message.reply_photo(
            photo=CITY_CHOICE_URL,
            [cite_start]caption="🌆 *ОБЕРІТЬ ВАШЕ МІСТО*", [cite: 8]
            reply_markup=get_city_keyboard(),
            parse_mode=ParseMode.MARKDOWN
        )
        return

    if data.startswith("city_"):
        [cite_start]city = data[len("city_"):] [cite: 9]
        if city not in ALL_CITIES:
            [cite_start]await query.message.reply_text("❌ Невідоме місто.") [cite: 9]
            return
        [cite_start]districts = ALL_CITIES[city] [cite: 9]
        [cite_start]keyboard = [[InlineKeyboardButton(f"📍 {district}", callback_data=f"district_{district}")] for district in districts] [cite: 9, 10]
        [cite_start]keyboard.append([InlineKeyboardButton("🏠 ГОЛОВНЕ МЕНЮ", callback_data="menu")]) [cite: 10]
        [cite_start]await query.message.delete() [cite: 10]
        [cite_start]await query.message.reply_text(f"🏙️ *{city}*\n\nОберіть район:", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode=ParseMode.MARKDOWN) [cite: 10]
        return

    if data.startswith("district_"):
        [cite_start]district = data[len("district_"):] [cite: 11]
        [cite_start]products = PRODUCTS.get(district, []) [cite: 11]
        if not products:
            [cite_start]await query.message.reply_text("❌ Товари відсутні в цьому районі.") [cite: 11]
            return
        [cite_start]keyboard = [[InlineKeyboardButton(f"{p['name']} | від {p['price']}₴", callback_data=f"product_{district}_{i}")] for i, p in enumerate(products)] [cite: 12]
        [cite_start]keyboard.append([InlineKeyboardButton("🏠 ГОЛОВНЕ МЕНЮ", callback_data="menu")]) [cite: 12]
        [cite_start]await query.message.delete() [cite: 12]
        [cite_start]await query.message.reply_text(f"🛍️ *Доступні товари в {district}*", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode=ParseMode.MARKDOWN) [cite: 12]
        return

    if data.startswith("product_"):
        [cite_start]parts = data.split("_") [cite: 13]
        if len(parts) < 3:
            [cite_start]await query.message.reply_text("❌ Помилка вибору товару.") [cite: 13]
            return
        [cite_start]_, district, idx = parts [cite: 13]
        [cite_start]idx = int(idx) [cite: 13]
        [cite_start]product = PRODUCTS[district][idx] [cite: 13]
        keyboard = [
            [cite_start][InlineKeyboardButton("💳 ОПЛАТА КАРТОЮ", callback_data=f"pay_card_{district}_{idx}")], [cite: 14]
            [cite_start][InlineKeyboardButton("🌐 ОПЛАТА КРИПТОЮ", callback_data=f"pay_crypto_{district}_{idx}")], [cite: 14]
            [cite_start][InlineKeyboardButton("🏠 ГОЛОВНЕ МЕНЮ", callback_data="menu")] [cite: 14]
        ]
        [cite_start]await query.message.delete() [cite: 14]
        [cite_start]await query.message.reply_text(f"💎 *{product['name']}*\n💰 Ціна: {product['price']}₴\n\nОберіть спосіб оплати:", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode=ParseMode.MARKDOWN) [cite: 14, 15]
        return

    if data.startswith("pay_card_") or data.startswith("pay_crypto_"):
        [cite_start]parts = data.split("_") [cite: 15]
        if len(parts) < 3:
            [cite_start]await query.message.reply_text("❌ Помилка оплати.") [cite: 15]
            return
        [cite_start]_, _, district, idx = parts # Исправлено количество частей для корректного распаковки [cite: 15]
        [cite_start]idx = int(idx) [cite: 16]
        [cite_start]product = PRODUCTS[district][idx] [cite: 16]
        [cite_start]method = "💳 карткою" if data.startswith("pay_card_") else "🌐 криптовалютою" [cite: 16]
        [cite_start]await query.message.delete() [cite: 16]
        [cite_start]await query.message.reply_text(f"{method} за *{product['name']}* ({product['price']}₴).\n\nЗв'яжіться з менеджером: {ADMIN_LINK}", parse_mode=ParseMode.MARKDOWN) [cite: 16, 17]
        return

# ====== ЗАПУСК ======
if __name__ == "__main__":
    # Запускаем фоновый сервер, чтобы Render не убивал процесс
    threading.Thread(target=run_health_server, daemon=True).start()
    
    [cite_start]app = ApplicationBuilder().token(TOKEN).build() [cite: 17]
    [cite_start]app.add_handler(CommandHandler("start", start)) [cite: 17]
    [cite_start]app.add_handler(CallbackQueryHandler(button_handler)) [cite: 17]
    [cite_start]logging.info("Бот запущен...") [cite: 17]
    [cite_start]app.run_polling() [cite: 17]
