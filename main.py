from pyrogram import Client, filters
from pyrogram.types import Message
from config import API_ID, API_HASH, BOT_TOKEN

from utils.state import user_state
from utility.video_utils import download_m3u8_video
import os

app = Client("uploader-bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Step 1: Terima perintah /m3u8 dan minta user mengirimkan link
@app.on_message(filters.command("m3u8") & filters.private)
async def m3u8_step_one(client, message: Message):
    await message.reply_text(
        "🎬 Silakan kirimkan link `.m3u8` Anda.\n\nContoh:\n`https://example.com/video/stream.m3u8`"
    )
    user_state[message.from_user.id] = "awaiting_m3u8_link"

# Step 2: Tangani teks biasa yang berisi link .m3u8
@app.on_message(filters.text & filters.private)
async def m3u8_step_two(client, message: Message):
    user_id = message.from_user.id

    # Abaikan jika user tidak dalam mode /m3u8
    if user_state.get(user_id) != "awaiting_m3u8_link":
        return

    m3u8_url = message.text.strip()

    # Validasi sederhana link m3u8
    if not m3u8_url.startswith("http") or ".m3u8" not in m3u8_url:
        await message.reply_text("❌ Link tidak valid. Pastikan itu adalah link `.m3u8`.")
        return

    await message.reply_text("⏳ Sedang mendownload video...")

    output_file = f"{user_id}_m3u8.mp4"
    status_msg = await message.reply_text("📥 Mulai mengunduh...")

    success = await download_m3u8_video(m3u8_url, output_file, status_msg, client)

    if not success or not os.path.exists(output_file):
        await status_msg.edit("❌ Gagal mendownload video.")
    else:
        await status_msg.edit("✅ Berhasil! Mengirimkan ke Telegram...")
        await client.send_video(chat_id=message.chat.id, video=output_file, caption="🎉 Selesai!")
        os.remove(output_file)

    # Hapus state setelah selesai
    user_state.pop(user_id, None)

if __name__ == "__main__":
    print("🎬 Bot siap berjalan hanya dengan /m3u8!")
    app.run()
