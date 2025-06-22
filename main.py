# Telegram Uploader Bot v1.02,02,+01
# Menarik konfigurasi dari environment (aman untuk publikasi)

import os
from pyrogram import Client, filters
from pyrogram.types import Message
import asyncio

API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")

app = Client("uploader_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("start"))
async def start(client, message: Message):
    await message.reply("🤖 Bot aktif! Kirimkan direct link untuk mengunduh dan mengunggah ke Telegram.")

@app.on_message(filters.text & filters.private)
async def handle_link(client, message: Message):
    url = message.text.strip()
    if not url.startswith("http"):
        await message.reply("❌ Link tidak valid.")
        return
    await message.reply("🚀 Sedang mengunduh... (placeholder)")
    await asyncio.sleep(2)
    await message.reply_document("sample.txt")  # Simulasi upload

app.run()
