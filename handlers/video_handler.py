# handlers/video_handler.py

from handlers.state_manager import set_state

async def handle_drlvideo(client, message):
    chat_id = message.chat.id
    set_state(chat_id, "drlvideo")

    await message.reply(
        "📽️ Kirimkan link video direct kamu.\n\n"
        "Contoh:\n"
        "`https://example.com/video.mp4`\n"
        "`https://example.com/video.ts`\n"
        "`https://example.com/stream.m3u8`",
        quote=True
    )
