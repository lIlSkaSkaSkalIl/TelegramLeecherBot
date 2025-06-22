from handlers.state_manager import set_state

async def handle_video(client, message):
    chat_id = message.chat.id
    set_state(chat_id, "video")

    await message.reply(
        "🎞️ Kirimkan link video kamu.\n\n"
        "Contoh:\n"
        "`https://example.com/video.mp4`\n"
        "`https://example.com/stream.m3u8`\n"
        "`https://example.com/video.ts`",
        quote=True
    )
