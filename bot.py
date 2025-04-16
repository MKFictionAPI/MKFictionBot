import sqlite3
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, ContextTypes

def init_db():
    conn = sqlite3.connect("kartasheva.db")
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS settings (user_id TEXT, theme TEXT DEFAULT 'light', PRIMARY KEY (user_id))")
    conn.commit()
    conn.close()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    channel_id = "-1002203758947"
    try:
        member = await context.bot.get_chat_member(channel_id, user_id)
        if member.status in ["member", "administrator", "creator"]:
            await update.message.reply_text("🖤 Добро пожаловать в мир Марии Карташевой! Напиши /read, чтобы открыть читалку!")
        else:
            await update.message.reply_text("Подпишись на Читательский клуб Марии Карташевой, чтобы читать.")
    except:
        await update.message.reply_text("Ошибка. Убедись, что ты в канале.")

async def read_book(update: Update, context: ContextTypes.DEFAULT_TYPE):
    base_url = "https://mkfictionapi.github.io/mkfiction"
    keyboard = [[InlineKeyboardButton("Открыть читалку", web_app=WebAppInfo(url=base_url))]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Нажми, чтобы читать:", reply_markup=reply_markup)

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update and update.message:
        await update.message.reply_text("Ой, что-то пошло не так... Попробуй снова или напиши /start.")
    print(f"Ошибка: {context.error}")

def main():
    app = Application.builder().token("7706583055:AAEllWzqSkP6WS1R1QgQSuBXc-0IFknZylw").build()  # Замени на свой токен
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("read", read_book))
    app.add_error_handler(error_handler)
    app.run_polling()

if __name__ == "__main__":
    main()