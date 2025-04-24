import os
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
    ConversationHandler
)
from dotenv import load_dotenv
import asyncio

# Cargar variables desde .env
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

REPORTE = 1

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    botones = [
        [KeyboardButton("📸 Enviar foto"), KeyboardButton("📝 Escribir reporte")]
    ]
    await update.message.reply_text(
        "🚨 ¡Bienvenido a Alerta Vecinal CABA! "
        "Para hacer un reporte, por favor, seleccioná una opción.",
        reply_markup=ReplyKeyboardMarkup(botones, resize_keyboard=True)
    )

async def reporte(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🚨 Escribí la descripción del robo o incidente ocurrido.")
    return REPORTE

async def recibir_reporte(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reporte = update.message.text
    chat_id = "-1002688551031"
    await context.bot.send_message(chat_id=chat_id, text=f"🚨 Nuevo reporte recibido:\n{reporte}")
    await update.message.reply_text(f"📝 Reporte recibido: {reporte}. Gracias por tu colaboración.")
    return ConversationHandler.END

async def recibir_foto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = "-1002688551031"
    photo = update.message.photo[-1].file_id
    await context.bot.send_photo(chat_id=chat_id, photo=photo, caption="🚨 Nuevo reporte con foto recibido.")
    await update.message.reply_text("📷 Foto recibida. ¡Gracias por tu reporte!")
    return ConversationHandler.END

async def cancelar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Operación cancelada.")
    return ConversationHandler.END

def run():
    # Esta función no usa asyncio.run()
    app = ApplicationBuilder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.TEXT & filters.Regex("📝 Escribir reporte"), reporte)],
        states={REPORTE: [MessageHandler(filters.TEXT & ~filters.COMMAND, recibir_reporte)]},
        fallbacks=[CommandHandler("cancel", cancelar)],
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(conv_handler)
    app.add_handler(MessageHandler(filters.PHOTO, recibir_foto))

    print("Bot funcionando...")
    # Esto inicia el polling directamente, evitando conflictos de loop
    app.run_polling()

if __name__ == "__main__":
    run()
