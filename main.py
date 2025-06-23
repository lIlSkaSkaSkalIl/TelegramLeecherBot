# Telegram Uploader Bot v1.02,07
# Termasuk fitur: /m3u8 (dua langkah)

from pyrogram import Client, filters
from pyrogram.types import Message
from config import API_ID, API_HASH, BOT_TOKEN

# Import semua handler
from handlers.gdrive_handler import handle_gdrive
from handlers.direct_handler import handle_direct
from handlers.video_handler import handle_drlvideo
from handlers.gdvideo_handler import handle_gdvideo
from handlers.link_router import handle_link_input
from handlers.start_handler import handle_start
from handlers.help_handler import handle_help
from handlers import m3u8_handler  # ✅ Wajib import untuk aktifkan handler m3u8

app = Client("uploader-bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("start"))
async def start(client, message: Message):
    await handle_start(client, message)

@app.on_message(filters.command("help"))
async def help_command(client, message: Message):
    await handle_help(client, message)

@app.on_message(filters.command("gd"))
async def gdrive(client, message: Message):
    await handle_gdrive(client, message)

@app.on_message(filters.command("drl"))
async def direct(client, message: Message):
    await handle_direct(client, message)

@app.on_message(filters.command("drlvideo"))
async def drlvideo(client, message: Message):
    await handle_drlvideo(client, message)

@app.on_message(filters.command("gdvideo"))
async def gdvideo(client, message: Message):
    await handle_gdvideo(client, message)

# m3u8 handler berjalan otomatis saat user kirim /m3u8 dan balasan link — tidak perlu didaftarkan lagi di sini
# Handler itu sudah aktif melalui import `from handlers import m3u8_handler`

@app.on_message(filters.text & ~filters.command([
    "start", "help", "gd", "drl", "drlvideo", "gdvideo", "m3u8"
]))
async def link_input(client, message: Message):
    await handle_link_input(client, message)

if __name__ == "__main__":
    print("✅ Bot siap berjalan!")
    app.run()
