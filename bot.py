import os, threading, time
from http.server import HTTPServer, BaseHTTPRequestHandler
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBAPP_URL = os.getenv("WEBAPP_URL", "https://ostrye-ai.vercel.app")

class H(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")
    def log_message(self,*a): return

def run_h():
    HTTPServer(("0.0.0.0", int(os.environ.get("PORT",10000))), H).serve_forever()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    kb=[[InlineKeyboardButton("🌐 ОТКРЫТЬ AI", web_app=WebAppInfo(url=WEBAPP_URL))]]
    await update.message.reply_text("OSTRYE - Кидай фото!", reply_markup=InlineKeyboardMarkup(kb))

async def photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Фото получил!")

def main():
    threading.Thread(target=run_h, daemon=True).start()
    if not BOT_TOKEN:
        while True: time.sleep(3600)
    app=Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.PHOTO, photo))
    app.run_polling()

if __name__=="__main__":
    main()
