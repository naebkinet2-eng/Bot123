import os
import logging
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# ====== СЕРВЕР ДЛЯ RENDER (Health Check) ======
# Этот блок нужен, чтобы Render не выключал бота
class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is alive!")

def run_health_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', port), HealthCheckHandler)
    server.serve_forever()

# ====== НАСТРОЙКИ ======
TOKEN = os.environ.get("TOKEN")
ADMIN_LINK = "https://t.me/gogact"
REVIEWS_LINK = "https://t.me/gogact"

LOGO_URL = "https://i.imgur.com/8wKYVxZ.jpeg"
CITY_CHOICE_URL = "https://i.imgur.com/8wKYVxZ.jpeg"

# ====== ТОВАРЫ ======
PRODUCTS = {
    "Печерський": [{"name": "🔥 ПРЕМІУМ ТОВАР 1", "price": 899}, {"name": "🔥 ПРЕМІУМ ТОВАР 2", "price": 999}],
    "Шевченківський": [{"name": "🔥 ПРЕМІУМ ТОВАР 1", "price": 899}, {"name": "🔥 ПРЕМІУМ ТОВАР 2", "price": 999}, {"name": "🔥 ПРЕМІУМ ТОВАР 3", "price": 999}],
    "Подільський": [{"name": "🔥 ПРЕМІУМ ТОВАР 1", "price": 899}],
    "Оболонський": [{"name": "🔥 ПРЕМІУМ ТОВАР 1", "price": 899}],
    "Київський": [{"name": "🔥 ТОВАР", "price": 850}],
    "Салтівський": [{"name": "🔥 ТОВАР", "price": 800}],
    "Приморський": [{"name": "🔥 ТОВАР", "price": 900}],
    "Малиновський": [{"name": "🔥 ТОВАР", "price": 870}],
    "Соборний": [{"name": "🔥 ТОВАР", "price": 880}],
    "Центральний": [{"name": "🔥 ТОВАР", "price": 860}],
    "Чечелівський": [{"name": "🔥 ТОВАР", "price": 890}],
    "Галицький": [{"name": "🔥 ТОВАР", "price": 840}],
    "Франківський": [{"name": "🔥 ТОВАР", "price": 830}],
    "Олександрівський": [{"name": "🔥 ТОВАР", "price": 810}],
    "Комунарський": [{"name": "🔥 ТОВАР", "price": 820}],
    "Металургійний": [{"name": "🔥 ТОВАР", "price": 800}],
    "Довгинцівський": [{"name": "🔥 ТОВАР", "price": 805}],
    "Заводський": [{"name": "🔥 ТОВАР", "price": 815}],
    "Замостянський": [{"name": "🔥 ТОВАР", "price": 820}],
    "Ленінський": [{"name": "🔥 ТОВАР", "price": 830}],
    "Зарічний": [{"name": "🔥 ТОВАР", "price": 810}],
    "Богунський": [{"name": "🔥 ТОВАР", "price": 800}],
    "Соснівський": [{"name": "🔥 ТОВАР", "price": 805}],
}

# ====== ГОРОДА И РАЙОНЫ ======
ALL_CITIES = {}

LARGE_CITIES = {
    "Київ": ["Печерський", "Шевченківський", "Подільський", "Оболонський"],
    "Харків": ["Шевченківський", "Київський", "Салтівський"],
    "Одеса": ["Приморський", "Київський", "Малиновський"],
    "Дніпро": ["Соборний", "Центральний", "Чечелівський"],
    "Львів": ["Галицький", "Франківський", "Шевченківський"],
}

MEDIUM_CITIES = {
    "Запоріжжя": ["Олександрівський", "Комунарський"],
    "Кривий Ріг": ["Металургійний", "Довгинцівський"],
    "Миколаїв": ["Центральний", "Заводський"],
    "Вінниця": ["Замостянський", "Ленінський"],
    "Полтава": ["Шевченківський", "Київський"],
}

SMALL_CITIES = {
    "Чернігів": ["Деснянський"],
    "Черкаси": ["Соснівський"],
    "Житомир": ["Богунський"],
    "Суми": ["Зарічний"],
    "Хмельницький": ["Центральний"],
}

ALL_CITIES.update(LARGE_CITIES)
ALL_CITIES.update(MEDIUM_CITIES)
ALL_CITIES.update(SMALL_CITIES)

# Логирование
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

async def send_main_menu(message, context: ContextTypes.DEFAULT_TYPE):
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🛒 КУПИТИ ЗАРАЗ!", callback_data="buy")],
        [
            InlineKeyboardButton("⭐ ВІДГУКИ КЛІЄНТІВ", url=REVIEWS_LINK),
            InlineKeyboardButton("📞 ЗВ'ЯЗОК З НАМИ", url=ADMIN_LINK)
        ]
    ])
    await message.reply_photo(
        photo=LOGO_URL,
        caption="🎉 *ЛАСКАВО ПРОСИМО ДО НАШОГО МАГАЗИНУ!*\n\n🔥 Найкращі товари\n⚡ Швидка доставка\n💯 Гарантія якості",
        reply_markup=keyboard,
        parse_mode=ParseMode.MARKDOWN
    )

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_main_menu(update.message, context)

def get_city_keyboard():
    keyboard = [[InlineKeyboardButton(f"🏙️ {city}", callback_data=f"city_{city}")] for city in ALL_CITIES.keys()]
    keyboard.append([InlineKeyboardButton("🏠 ГОЛОВНЕ МЕНЮ", callback_data="menu")])
    return InlineKeyboardMarkup(keyboard)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data
    await query.answer()

    if data == "menu":
        await query.message.delete()
        await send_main_menu(query.message, context)
        return

    if data == "buy":
        await query.message.delete()
        await query.message.reply_photo(
            photo=CITY_CHOICE_URL,
            caption="🌆 *ОБЕРІТЬ ВАШЕ МІСТО*",
            reply_markup=get_city_keyboard(),
            parse_mode=ParseMode.MARKDOWN
        )
        return

    if data.startswith("city_"):
        city = data[len("city_"):]
        if city not in ALL_CITIES:
            await query.message.reply_text("❌ Невідоме місто.")
            return
        districts = ALL_CITIES[city]
        keyboard = [[InlineKeyboardButton(f"📍 {district}", callback_data=f"district_{district}")] for district in districts]
        keyboard.append([InlineKeyboardButton("🏠 ГОЛОВНЕ МЕНЮ", callback_data="menu")])
        await query.message.delete()
        await query.message.reply_text(f"🏙️ *{city}*\n\nОберіть район:", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode=ParseMode.MARKDOWN)
        return

    if data.startswith("district_"):
        district = data[len("district_"):]
        products = PRODUCTS.get(district, [])
        if not products:
            await query.message.reply_text("❌ Товари відсутні в цьому районі.")
            return
        keyboard = [[InlineKeyboardButton(f"{p['name']} | від {p['price']}₴", callback_data=f"product_{district}_{i}")] for i, p in enumerate(products)]
        keyboard.append([InlineKeyboardButton("🏠 ГОЛОВНЕ МЕНЮ", callback_data="menu")])
        await query.message.delete()
        await query.message.reply_text(f"🛍️ *Доступні товари в {district}*", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode=ParseMode.MARKDOWN)
        return

    if data.startswith("product_"):
        parts = data.split("_")
        if len(parts) < 3:
            await query.message.reply_text("❌ Помилка вибору товару.")
            return
        _, district, idx = parts
        idx = int(idx)
        product = PRODUCTS[district][idx]
        keyboard = [
            [InlineKeyboardButton("💳 ОПЛАТА КАРТОЮ", callback_data=f"pay_card_{district}_{idx}")],
            [InlineKeyboardButton("🌐 ОПЛАТА КРИПТОЮ", callback_data=f"pay_crypto_{district}_{idx}")],
            [InlineKeyboardButton("🏠 ГОЛОВНЕ МЕНЮ", callback_data="menu")]
        ]
        await query.message.delete()
        await query.message.reply_text(f"💎 *{product['name']}*\n💰 Ціна: {product['price']}₴\n\nОберіть спосіб оплати:", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode=ParseMode.MARKDOWN)
        return

    if data.startswith("pay_card_") or data.startswith("pay_crypto_"):
        parts = data.split("_")
        if len(parts) < 3:
            await query.message.reply_text("❌ Помилка оплати.")
            return
        _, _, district, idx = parts 
        idx = int(idx)
        product = PRODUCTS[district][idx]
        method = "💳 карткою" if data.startswith("pay_card_") else "🌐 криптовалютою"
        await query.message.delete()
        await query.message.reply_text(f"{method} за *{product['name']}* ({product['price']}₴).\n\nЗв'яжіться з менеджером: {ADMIN_LINK}", parse_mode=ParseMode.MARKDOWN)
        return

# ====== ЗАПУСК ======
if __name__ == "__main__":
    # Запуск Health Check сервера для Render
    threading.Thread(target=run_health_server, daemon=True).start()
    
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    logging.info("Бот запущен...")
    app.run_polling()
