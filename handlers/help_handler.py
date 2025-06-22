# handlers/help_handler.py

async def handle_help(client, message):
    await message.reply(
        "🆘 *Bantuan Penggunaan Bot*\n\n"
        "`/start` - Perkenalan bot\n"
        "`/help` - Menampilkan bantuan ini\n\n"
        "*Download File:*\n"
        `/drl` - Download dari direct download link\n`
        `/gd` - Download dari Google Drive\n\n`
        *Download Video:*\n`
        `/drlvideo` - Kirim video dari direct link (streamable)\n`
        `/gdvideo` - Kirim video dari Google Drive (streamable)\n\n`
        *Catatan:* Semua perintah akan diikuti oleh permintaan link secara otomatis.",
        quote=True
    )
