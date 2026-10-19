import os, logging, threading
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from http.server import HTTPServer, BaseHTTPRequestHandler

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBAPP_URL = os.getenv("WEBAPP_URL", "https://ostrye-ai.vercel.app")
logging.basicConfig(level=logging.INFO)

class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OSTRYE BOT LIVE")
    def log_message(self, format, *args): return

def run_health():
    port = int(os.environ.get("PORT", 10000))
    HTTPServer(("0.0.0.0", port), HealthHandler).serve_forever()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    kb = [[InlineKeyboardButton("🌐 ОТКРЫТЬ AI БОТ", web_app=WebAppInfo(url=WEBAPP_URL))]]
    await update.message.reply_text("✂️ OSTRYE NVR - Кидай фото анфас!", reply_markup=InlineKeyboardMarkup(kb))

async def photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📸 Фото получил! Анализирую...")

def main():
    threading.Thread(target=run_health, daemon=True).start()
    if not BOT_TOKEN:
        print("BOT_TOKEN missing")
        import time
        while True: time.sleep(3600)
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.PHOTO, photo))
    print("OSTRYE BOT STARTED")
    app.run_polling()

if __name__ == "__main__": main()
