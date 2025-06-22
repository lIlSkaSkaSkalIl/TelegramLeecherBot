# handlers/direct_handler.py

from handlers.state_manager import set_state

async def handle_direct(client, message):
    chat_id = message.chat.id
    set_state(chat_id, "drl")

    await message.reply(
        "📥 Silakan kirimkan link direct download kamu.\n\n"
        "Contoh:\n"
        "`https://example.com/file.zip`",
        quote=True
    )
