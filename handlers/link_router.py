import os, time
from handlers.state_manager import get_state, clear_state
from utility.status_format import format_status
from utility.gdrive_utils import download_gdrive

async def handle_link_input(client, message):
    chat_id = message.chat.id
    state = get_state(chat_id)

    # Jika tidak ada state aktif atau bukan sedang menunggu link
    if not state or state.get("step") != "awaiting_link":
        return await message.reply(
            "❗ Silakan gunakan perintah terlebih dahulu:\n"
            "/gd — untuk Google Drive\n"
            "/drl — untuk direct download link",
            quote=True
        )

    mode = state["mode"]
    url = message.text.strip()

    # Tangani perintah berdasarkan mode
    if mode == "gd":
        await process_gdrive(client, message, url)

    # Bisa ditambahkan: elif mode == "drl", "mega", dll
    else:
        await message.reply("⚠️ Mode tidak dikenali.")

    # Bersihkan state setelah selesai
    clear_state(chat_id)


async def process_gdrive(client, message, url):
    msg = await message.reply("☁️ Mengunduh dari Google Drive...")

    start_time = time.time()
    downloaded_path = download_gdrive(url)

    if not downloaded_path or not os.path.exists(downloaded_path):
        return await msg.edit(
            "⚠️ Yah, sepertinya aku tidak bisa mengunduh file dari link itu.\n\n"
            "Coba pastikan:\n"
            "🔗 Link valid dan bisa diakses publik\n"
            "📁 File tidak dibatasi oleh pemilik"
        )

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
        caption="✅ File berhasil diunggah dari Google Drive.",
        progress=upload_progress
    )

    os.remove(filename)
