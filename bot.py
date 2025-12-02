from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

from api.google_places import search_places, get_photo_url
from config import TELEGRAM_TOKEN

async def start(update: Update, _context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привіт! Я бот для пошуку місць за допомогою Google Places API.\n"
        "Напиши мені які цікаві місця ти хочеш знайти.\n"
        "Приклад: Кафе у Києві біля метро Васильківська"
    )

async def find(update: Update, _context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text.strip()

    await update.message.reply_text("Шукаю...")

    results = search_places(query)
    if not results:
        await update.message.reply_text("Нічого не знайдено.")
        return

    for place in results[:5]:
        text = format_place(place)
        photos = place.get("photos", [])

        if photos:
            photo_name = photos[0]["name"]  # перше фото
            photo_url = get_photo_url(photo_name)

            await update.message.reply_photo(
                photo=photo_url,
                caption=text,
                parse_mode="HTML"
            )

            continue

        await update.message.reply_text(text, parse_mode="HTML", disable_web_page_preview=False)

def format_place(place):
    name = place.get("displayName", {}).get("text", "Без назви")
    address = place.get("formattedAddress", "—")
    rating = place.get("rating", "—")
    maps_url = place.get("googleMapsUri", "")

    text = (
        f"🏙 <b>{name}</b>\n"
        f"⭐ Рейтинг: {rating}\n"
        f"📍 {address}\n"
    )

    if maps_url:
        text += f"🔗 <a href=\"{maps_url}\">Переглянути на мапі</a>\n"

    return text

def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, find))

    print("Бот запущено...")
    app.run_polling()

if __name__ == "__main__":
    main()