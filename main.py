# Telegram Uploader Bot v1.02,05
# Versi langsung jalan - dari link → upload ke chat

import os
import requests
import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message

API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")

app = Client("uploader_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("start"))
async def start(client, message: Message):
    await message.reply("🤖 Halo! Kirimkan link direct download ke bot ini, dan aku akan mengunggahnya ke Telegram untukmu.")

@app.on_message(filters.text & filters.private)
async def handle_link(client, message: Message):
    url = message.text.strip()
    if not url.startswith("http"):
        await message.reply("❌ Link tidak valid.")
        return

    msg = await message.reply("🚀 Sedang mengunduh file...")

    try:
        filename = url.split("/")[-1].split("?")[0] or "downloaded_file"
        response = requests.get(url, stream=True, timeout=60)

        if response.status_code != 200:
            await msg.edit("❌ Gagal mengunduh file.")
            return

        with open(filename, "wb") as f:
            for chunk in response.iter_content(chunk_size=1024*1024):
                if chunk:
                    f.write(chunk)

        await msg.edit("📤 Mengunggah ke Telegram...")
        await message.reply_document(filename)
        os.remove(filename)

    except Exception as e:
        await msg.edit(f"⚠️ Terjadi error:\n`{str(e)}`")

app.run()
