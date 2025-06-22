from handlers.state_manager import set_state

async def handle_gdrive(client, message):
    chat_id = message.chat.id

    # Simpan state bahwa user sedang dalam mode Google Drive
    set_state(chat_id, "gd")

    # Minta user untuk mengirimkan link GDrive selanjutnya
    await message.reply(
        "📥 Kirimkan link Google Drive kamu.\n\n"
        "Contoh:\n"
        "`https://drive.google.com/file/d/1A2B3C4D5E6F7G8H9/view?usp=sharing`",
        quote=True
    )
