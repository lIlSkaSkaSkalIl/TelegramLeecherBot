# handlers/start_handler.py

async def handle_start(client, message):
    await message.reply(
        "👋 Halo! Saya adalah Telegram Uploader Bot.\n\n"
        "Saya bisa membantu kamu untuk:\n"
        "📥 Mengunduh file dari direct link & Google Drive\n"
        "🎥 Mengunggah video yang bisa langsung diputar di Telegram\n\n"
        "Gunakan perintah berikut untuk memulai:\n"
        "/drl - Unduh file dari direct link\n"
        "/gd - Unduh file dari Google Drive\n"
        "/drlvideo - Kirim video dari direct link\n"
        "/gdvideo - Kirim video dari Google Drive",
        quote=True
    )
