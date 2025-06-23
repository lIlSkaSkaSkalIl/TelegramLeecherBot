import os, time, requests
from handlers.state_manager import get_state, clear_state
from utility.status_format import format_status
from utility.gdrive_utils import download_gdrive
from utility.video_utils import is_video, smart_convert_to_mp4
from utils.state import user_state  # ✅ Diperlukan agar tidak bentrok dengan /m3u8

async def handle_link_input(client, message):
    chat_id = message.chat.id

    # ✅ Jangan proses jika user sedang dalam mode /m3u8
    if user_state.get(chat_id) == "awaiting_m3u8_link":
        return

    state = get_state(chat_id)

    if not state or state.get("step") != "awaiting_link":
        return await message.reply(
            "❗ Silakan gunakan perintah terlebih dahulu:\n"
            "/gd — Google Drive\n"
            "/drl — Direct download link\n"
            "/drlvideo — Video dari direct link\n"
            "/gdvideo — Video dari Google Drive",
            quote=True
        )

    mode = state["mode"]
    url = message.text.strip()

    if mode == "gd":
        await process_gdrive(client, message, url)
    elif mode == "drl":
        await process_direct(client, message, url)
    elif mode == "drlvideo":
        await process_video(client, message, url)
    elif mode == "gdvideo":
        await process_gdrive_video(client, message, url)
    else:
        await message.reply("⚠️ Mode tidak dikenali.")

    clear_state(chat_id)

# === Direct Download Handler ===
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
            caption="✅ Berhasil diunggah dari direct link.",
            progress=upload_progress
        )

        os.remove(filename)

    except Exception as e:
        await msg.edit(f"⚠️ Terjadi kesalahan:\n`{e}`")

# === Google Drive (Dokumen) ===
async def process_gdrive(client, message, url):
    msg = await message.reply("☁️ Mengunduh dari Google Drive...")

    start_time = time.time()
    downloaded_path = download_gdrive(url)

    if not downloaded_path or not os.path.exists(downloaded_path):
        return await msg.edit(
            "⚠️ Yah, sepertinya aku tidak bisa mengunduh file dari link itu.\n\n"
            "🔗 Link mungkin tidak valid atau tidak publik."
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

# === Direct Video Handler ===
async def process_video(client, message, url):
    filename = url.split("/")[-1].split("?")[0] or "video_input"
    msg = await message.reply("📥 Mengunduh video...")

    try:
        r = requests.get(url, stream=True, timeout=60)
        if r.status_code != 200:
            return await msg.edit("❌ Gagal mengunduh video dari link.")

        with open(filename, "wb") as f:
            for chunk in r.iter_content(1024 * 1024):
                if chunk:
                    f.write(chunk)

        if not is_video(filename):
            return await msg.edit(
                "⚠️ File ini bukan video yang bisa diputar.\n"
                "Gunakan `/drl` jika ingin kirim sebagai dokumen."
            )

        await msg.edit("⚙️ Memeriksa codec dan mengonversi jika diperlukan...\n⏳ Harap tunggu...")
        convert_time = smart_convert_to_mp4(filename)
        if filename != "converted_output.mp4":
            os.remove(filename)
        filename = "converted_output.mp4"

        await msg.edit(f"✅ Selesai dalam {convert_time:.2f} detik!\n📤 Mengunggah ke Telegram...")

        start = time.time()
        async def progress(current, total):
            if time.time() - progress.last > 5 or current == total:
                await msg.edit(f"📤 Mengunggah... {current * 100 // total}%")
                progress.last = time.time()
        progress.last = 0

        await client.send_video(
            chat_id=message.chat.id,
            video=filename,
            caption="✅ Video berhasil dikirim 🎬",
            supports_streaming=True,
            progress=progress
        )
        os.remove(filename)

    except Exception as e:
        await msg.edit(f"❌ Gagal memproses video:\n`{e}`")

# === GDrive Video Handler ===
async def process_gdrive_video(client, message, url):
    msg = await message.reply("📥 Mengunduh video dari Google Drive...")
    start = time.time()

    downloaded_path = download_gdrive(url)
    if not downloaded_path or not os.path.exists(downloaded_path):
        return await msg.edit(
            "❌ Gagal mengunduh dari Google Drive.\n"
            "🔗 Pastikan link valid dan file bisa diakses publik."
        )

    filename = downloaded_path
    if not is_video(filename):
        return await msg.edit(
            "⚠️ File ini bukan video yang bisa diputar.\n"
            "Gunakan `/gd` untuk unggah sebagai dokumen biasa."
        )

    await msg.edit("⚙️ Memeriksa codec dan mengonversi jika diperlukan...\n⏳ Harap tunggu...")
    convert_time = smart_convert_to_mp4(filename)
    if filename != "converted_output.mp4":
        os.remove(filename)
    filename = "converted_output.mp4"

    await msg.edit(f"✅ Selesai dalam {convert_time:.2f} detik!\n📤 Mengunggah video ke Telegram...")

    async def progress(current, total):
        now = time.time()
        if now - progress.last > 5 or current == total:
            await msg.edit(f"📤 Mengunggah... {current * 100 // total}%")
            progress.last = now
    progress.last = 0

    await client.send_video(
        chat_id=message.chat.id,
        video=filename,
        caption="✅ Video berhasil dikirim 🎬",
        supports_streaming=True,
        progress=progress
    )

    os.remove(filename)
