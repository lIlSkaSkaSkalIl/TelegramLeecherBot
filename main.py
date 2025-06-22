# Telegram Uploader Bot v1.02,06
# Versi langsung jalan - dari link → upload ke chat

from pyrogram import Client, filters
from handlers.gdrive_handler import handle_gdrive
from handlers.link_router import handle_link_input
import os

API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")

app = Client("uploader_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply(
        "👋 Halo!\n\n"
        "Saya adalah bot pengunggah file.\n\n"
        "Gunakan perintah berikut:\n"
        "📁 `/gd` — untuk mengunggah dari Google Drive\n"
        "🌐 `/drl` — untuk mengunggah dari direct download link\n\n"
        "Kirim salah satu perintah di atas lalu kirimkan linknya.",
        quote=True
    )

@app.on_message(filters.command("gd"))
async def gdrive(client, message):
    await handle_gdrive(client, message)

@app.on_message(filters.text & filters.private)
async def handle_text(client, message):
    await handle_link_input(client, message)

app.run()
