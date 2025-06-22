# handlers/gdvideo_handler.py

from handlers.state_manager import set_state

async def handle_gdvideo(client, message):
    chat_id = message.chat.id
    set_state(chat_id, "gdvideo")

    await message.reply(
        "🎥 Kirimkan link Google Drive video kamu.\n\n"
        "Contoh:\n"
        "`https://drive.google.com/file/d/FILE_ID/view?usp=sharing`",
        quote=True
    )
