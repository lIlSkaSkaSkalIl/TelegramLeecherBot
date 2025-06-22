import os, time, requests
from handlers.state_manager import get_state, clear_state
from utility.status_format import format_status
from utility.gdrive_utils import download_gdrive

async def handle_link_input(client, message):
    chat_id = message.chat.id
    state = get_state(chat_id)

    # Jika tidak sedang menunggu link, arahkan ke perintah
    if not state or state.get("step") != "awaiting_link":
        return await message.reply(
            "❗ Silakan gunakan perintah dibawah ini, untuk menggunakan botnya:\n\n"
            "/gd — untuk Google Drive\n"
            "/drl — untuk direct download link",
            quote=True
        )

    mode = state["mode"]
    url = message.text.strip()

    if mode == "gd":
        await process_gdrive(client, message, url)
    elif mode == "drl":
        await process_direct(client, message, url)
    else:
        await message.reply("⚠️ Mode tidak dikenali.")

    clear_state(chat_id)

# 🔽 Google Drive Handler
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

# 🔽 Direct Link Handler
async def process_direct(client, message, url):
    msg = await message.reply("🌐 Mengunduh dari direct link...")

    try:
        filename = url.split("/")[-1].split("?")[0] or "downloaded_file"
        r = requests.get(url, stream=True, timeout=60)
        if r.status_code != 200:
            return await msg.edit("❌ Gagal mengunduh file dari link.")

        total = int(r.headers.get("content-length", 0))
        done, start, last = 0, time.time(), 0

        with open(filename, "wb") as f:
            for chunk in r.iter_content(1024 * 1024):
                if chunk:
                    f.write(chunk)
                    done += len(chunk)
                    now = time.time()
                    if now - last > 5 or done == total:
                        await msg.edit(format_status("📥 Mengunduh", filename, done, total, now - start))
                        last = now

        await msg.edit("📤 Mengunggah ke Telegram...")

        async def upload_progress(current, total):
            now = time.time()
            if now - upload_progress.last_update > 5 or current == total:
                try:
                    await msg.edit(format_status("📤 Mengunggah", filename, current, total, now - start))
                    upload_progress.last_update = now
                except:
                    pass

        upload_progress.last_update = 0

        await client.send_document(
            chat_id=message.chat.id,
            document=filename,
            caption="✅ File berhasil diunggah dari direct link.",
            progress=upload_progress
        )

        os.remove(filename)

    except Exception as e:
        await msg.edit(f"⚠️ Terjadi kesalahan:\n`{e}`")
