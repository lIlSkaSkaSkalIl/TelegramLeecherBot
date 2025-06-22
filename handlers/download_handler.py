from utility.status_format import format_status
import os, time, requests

async def process_link(client, message):
    url = message.text.strip()
    if not url.startswith("http"):
        await message.reply("❌ Link tidak valid.")
        return

    msg = await message.reply("🔄 Memulai proses...")
    try:
        filename, total = await download_file(url, msg)
        await msg.edit("📤 Mengunggah ke Telegram...")
        await upload_file(client, message, msg, filename)
        os.remove(filename)

    except Exception as e:
        await msg.edit(f"⚠️ Error:\n`{e}`")


async def download_file(url, msg):
    filename = url.split("/")[-1].split("?")[0] or "downloaded_file"
    r = requests.get(url, stream=True, timeout=60)
    if r.status_code != 200:
        raise Exception("Gagal mengunduh.")

    total = int(r.headers.get("content-length", 0))
    downloaded = 0
    start = time.time()
    last = start

    with open(filename, "wb") as f:
        for chunk in r.iter_content(1024 * 1024):
            if chunk:
                f.write(chunk)
                downloaded += len(chunk)
                now = time.time()
                if now - last > 5 or downloaded == total:
                    await msg.edit(format_status("📥 Mengunduh", filename, downloaded, total, now - start))
                    last = now

    return filename, total


async def upload_file(client, message, msg, filename):
    start = time.time()

    async def progress(current, total):
        now = time.time()
        if now - progress.last > 5 or current == total:
            status = format_status("📤 Mengunggah", filename, current, total, now - start)
            try:
                await msg.edit(status)
            except:
                pass
            progress.last = now

    progress.last = 0

    await client.send_document(
        chat_id=message.chat.id,
        document=filename,
        caption="✅ File berhasil diunggah.",
        progress=progress
    )
