import os, time
from utility.gdrive_utils import download_gdrive
from utility.status_format import format_status

async def handle_gdrive(client, message):
    parts = message.text.strip().split(maxsplit=1)
    if len(parts) < 2:
        return await message.reply("⚠️ Gunakan format: `/gd <link_google_drive>`", quote=True)

    url = parts[1].strip()
    msg = await message.reply("☁️ Mengunduh dari Google Drive...")

    start_time = time.time()
    downloaded_path = download_gdrive(url)

    if not downloaded_path or not os.path.exists(downloaded_path):
        return await msg.edit("❌ Gagal mengunduh dari Google Drive.")

    filename = downloaded_path
    await msg.edit("📤 Mengunggah ke Telegram...")

    async def upload_progress(current, total):
        now = time.time()
        if now - upload_progress.last_update > 5 or current == total:
            try:
                await msg.edit(format_status("📤 Mengunggah", filename, current, total, now - start_time))
                upload_progress.last_update = now
            except:
                pass

    upload_progress.last_update = 0

    await client.send_document(
        chat_id=message.chat.id,
        document=filename,
        caption="✅ Berhasil diunggah.",
        progress=upload_progress
    )

    os.remove(filename)
